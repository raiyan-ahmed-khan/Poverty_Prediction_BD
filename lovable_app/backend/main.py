from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
import json
import os

app = FastAPI(
    title="Bangladesh Poverty Prediction API",
    description="Predicts district poverty using satellite features",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Load model and data at startup ────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))

model    = joblib.load(os.path.join(BASE, "models/random_forest_final.pkl"))
scaler   = joblib.load(os.path.join(BASE, "models/scaler_final.pkl"))
features = joblib.load(os.path.join(BASE, "models/feature_cols.pkl"))
df       = pd.read_csv(os.path.join(BASE, "data/master_features.csv"))

with open(os.path.join(BASE, "data/model_info.json")) as f:
    model_info = json.load(f)

# ── Input schema ──────────────────────────────────────────────
class PredictionInput(BaseModel):
    ntl_mean:       float
    ndvi_mean:      float
    elevation_mean: float
    road_density:   float
    urban_fraction: float
    water_fraction: float

# ── Routes ────────────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "status": "ok",
        "model":  "Random Forest Poverty Predictor",
        "docs":   "/docs"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "districts": len(df)}

@app.post("/predict")
def predict(inp: PredictionInput):
    # Build full feature vector using medians for non-slider features
    input_dict = {f: float(df[f].median()) for f in features}
    input_dict.update(inp.dict())

    X        = pd.DataFrame([input_dict])[features]
    X_scaled = scaler.transform(X)
    pred     = float(np.clip(model.predict(X_scaled)[0], 14.8, 26.9))

    # Label
    if pred > 23:
        label, color = "High Poverty",     "#ef4444"
    elif pred > 19:
        label, color = "Moderate Poverty", "#f59e0b"
    else:
        label, color = "Lower Poverty",    "#22c55e"

    # Similar districts
    df_copy = df.copy()
    df_copy["_dist"] = (df_copy["poverty_predicted"] - pred).abs()
    similar = df_copy.nsmallest(3, "_dist")[[
        "district_name", "division_name", "poverty_hcr"
    ]].to_dict("records")

    return {
        "prediction":        round(pred, 2),
        "label":             label,
        "color":             color,
        "similar_districts": similar
    }

@app.get("/districts")
def get_districts():
    cols = [
        "district_name", "division_name",
        "poverty_hcr", "poverty_predicted",
        "ntl_mean", "ndvi_mean", "elevation_mean",
        "road_density", "urban_fraction",
        "ntl_per_capita", "ntl_trend", "ntl_iqr",
        "elevation_std"
    ]
    # Remove duplicate column names
    cols = list(dict.fromkeys(cols))
    return df[cols].round(3).to_dict("records")

@app.get("/model-info")
def get_model_info():
    return model_info

@app.get("/district/{district_name}")
def get_district(district_name: str):
    row = df[df["district_name"] == district_name]
    if len(row) == 0:
        return {"error": f"District {district_name} not found"}
    return row.iloc[0].to_dict()
