# ============================================================
# Bangladesh Poverty Prediction — Interactive Web App
# ISRT, University of Dhaka
# ============================================================

import os
import warnings
warnings.filterwarnings('ignore')

import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
import joblib
import json

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Mapping Poverty from Space · Bangladesh",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
    }

    .stApp {
        background-color: #060810;
        background-image:
            radial-gradient(ellipse at 20% 20%, #0d1f3c 0%, transparent 50%),
            radial-gradient(ellipse at 80% 80%, #0a1628 0%, transparent 50%);
        color: #e2e8f0;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0f1e 0%, #060810 100%);
        border-right: 1px solid #1e2d4a;
    }

    section[data-testid="stSidebar"] .stRadio label {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.9rem;
        color: #94a3b8;
        padding: 8px 12px;
        border-radius: 8px;
        transition: all 0.2s;
        cursor: pointer;
    }

    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #0d1f3c 0%, #0a1628 100%);
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 16px;
        transition: border-color 0.2s;
    }

    div[data-testid="metric-container"]:hover {
        border-color: #3b82f6;
    }

    h1, h2 { color: #60a5fa !important; font-family: 'Space Grotesk', sans-serif !important; font-weight: 700 !important; }
    h3     { color: #e2e8f0 !important; font-family: 'Space Grotesk', sans-serif !important; font-weight: 600 !important; }

    .stTabs [data-baseweb="tab-list"] {
        background: #0a0f1e;
        border-radius: 10px;
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #64748b;
        border-radius: 8px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 500;
        padding: 8px 20px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1d4ed8, #2563eb) !important;
        color: white !important;
    }

    hr { border-color: #1e2d4a; }

    .stat-card {
        background: linear-gradient(135deg, #0d1f3c 0%, #0a1628 100%);
        border: 1px solid #1e3a5f;
        border-radius: 14px;
        padding: 24px 20px;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, #1d4ed8, #60a5fa, #1d4ed8);
        background-size: 200% 100%;
        animation: shimmer 3s infinite;
    }
    @keyframes shimmer {
        0%   { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    .stat-number {
        font-size: 2.4rem;
        font-weight: 700;
        color: #60a5fa;
        font-family: 'JetBrains Mono', monospace;
        line-height: 1;
    }
    .stat-label {
        font-size: 0.78rem;
        color: #64748b;
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 500;
    }

    .hero-badge {
        display: inline-block;
        background: #1e3a5f22;
        border: 1px solid #1e3a5f;
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.78rem;
        color: #60a5fa;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
        margin-bottom: 16px;
    }
    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        color: #f1f5f9;
        line-height: 1.15;
        letter-spacing: -0.02em;
    }
    .hero-title span { color: #60a5fa; }
    .hero-sub {
        font-size: 1.05rem;
        color: #64748b;
        margin-top: 12px;
        line-height: 1.6;
        max-width: 520px;
    }

    .district-card {
        background: linear-gradient(135deg, #0d1f3c 0%, #0a1628 100%);
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 18px;
        margin-top: 12px;
    }
    .pred-badge {
        display: inline-block;
        border-radius: 24px;
        padding: 8px 20px;
        font-size: 1.6rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        margin-top: 6px;
    }

    .explain-box {
        background: #0d1f3c33;
        border: 1px solid #1e3a5f;
        border-left: 3px solid #3b82f6;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 20px;
        font-size: 0.88rem;
        color: #94a3b8;
        line-height: 1.6;
    }
    .explain-box strong { color: #e2e8f0; }

    .finding-card {
        background: linear-gradient(135deg, #0d1f3c 0%, #0a1628 100%);
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 20px;
        height: 100%;
    }
    .finding-icon { font-size: 1.8rem; margin-bottom: 10px; }
    .finding-title {
        font-weight: 700;
        color: #e2e8f0;
        font-size: 0.95rem;
        margin-bottom: 8px;
    }
    .finding-text {
        color: #64748b;
        font-size: 0.85rem;
        line-height: 1.6;
    }

    .stButton>button {
        background: linear-gradient(135deg, #1d4ed8, #2563eb);
        color: white;
        border: none;
        border-radius: 8px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        padding: 8px 20px;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb, #3b82f6);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px #3b82f644;
    }

    .stSlider > div > div > div {
        background: #1d4ed8 !important;
    }

    .stInfo {
        background: #0d1f3c44 !important;
        border-color: #1e3a5f !important;
    }
</style>
""", unsafe_allow_html=True)


# ── Data loading (cached) ─────────────────────────────────────
@st.cache_data
def load_data():
    df      = pd.read_csv("data/processed/master_features.csv")
    shap_df = pd.read_csv("data/processed/shap_values.csv")
    gdf     = gpd.read_file("data/processed/master_features.gpkg")
    return df, shap_df, gdf


@st.cache_resource
def load_models():
    model    = joblib.load("models/random_forest_final.pkl")
    scaler   = joblib.load("models/scaler_final.pkl")
    features = joblib.load("models/feature_cols.pkl")
    return model, scaler, features


@st.cache_data
def get_geojson(_gdf):
    return json.loads(_gdf.to_json())


@st.cache_data
def get_centroids(_gdf):
    c = _gdf.copy()
    c['cx'] = _gdf.geometry.centroid.x
    c['cy'] = _gdf.geometry.centroid.y
    return c[['district_name', 'cx', 'cy']]


def build_folium_map_cached(_gdf, _centroids):
    m = folium.Map(
        location=[23.7, 90.3],
        zoom_start=7,
        tiles='CartoDB dark_matter'
    )
    folium.Choropleth(
        geo_data=_gdf.__geo_interface__,
        data=_gdf[['district_name', 'poverty_hcr']],
        columns=['district_name', 'poverty_hcr'],
        key_on='feature.properties.district_name',
        fill_color='RdYlGn_r',
        fill_opacity=0.7,
        line_opacity=0.3,
        line_color='white',
        legend_name='Poverty HCR (%)',
    ).add_to(m)

    for _, row in _centroids.iterrows():
        folium.CircleMarker(
            location=[row['cy'], row['cx']],
            radius=5,
            color='white',
            weight=1,
            fill=True,
            fill_color='#60a5fa',
            fill_opacity=0.8,
            tooltip=row['district_name'],
            popup=folium.Popup(row['district_name'], parse_html=True)
        ).add_to(m)
    return m

# ── Load everything ───────────────────────────────────────────
df, shap_df, gdf   = load_data()
model, scaler, features = load_models()
geojson            = get_geojson(gdf)
centroids          = get_centroids(gdf)


# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 8px 0 16px 0'>
        <div style='font-size:1.1rem; font-weight:700; color:#60a5fa'>
            🛰️ Bangladesh Poverty
        </div>
        <div style='font-size:0.78rem; color:#475569; margin-top:4px'>
            Predicting poverty from satellite data
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio(
        "Navigate",
        ["🏠 Overview",
         "🗺️ Explore Map",
         "🎛️ Live Predictor",
         "📊 Model Results"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.78rem; color:#475569; text-transform:uppercase;
                letter-spacing:0.08em; font-weight:600; margin-bottom:8px'>
        Data Sources
    </div>
    """, unsafe_allow_html=True)
    for src in ["VIIRS Nighttime Light", "Sentinel-2 Imagery",
                "HIES 2022 (BBS)", "OpenStreetMap", "WorldPop"]:
        st.markdown(f"<div style='font-size:0.82rem;color:#64748b;padding:2px 0'>· {src}</div>",
                    unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.78rem; color:#475569; text-transform:uppercase;
                letter-spacing:0.08em; font-weight:600; margin-bottom:8px'>
        Best Model
    </div>
    <div style='font-size:0.82rem; color:#64748b'>
        Random Forest · 19 features<br>
        <span style='color:#60a5fa; font-weight:600;
                     font-family:monospace'>LODO-CV RMSE: 3.626 pp</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.75rem; color:#334155; text-align:center'>
        ISRT · University of Dhaka · 2024
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ════════════════════════════════════════════════════════════
if page == "🏠 Overview":

    # Hero section
    st.markdown("""
    <div style='padding: 32px 0 24px 0'>
        <div class='hero-badge'>🛰️ Satellite ML Research · ISRT · University of Dhaka</div>
        <div class='hero-title'>Mapping Poverty<br><span>from Space</span></div>
        <div class='hero-sub'>
            Using satellite nighttime light, vegetation indices, terrain data,
            and road networks to predict district-level poverty across Bangladesh —
            without a single ground survey.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Explanation
    st.markdown("""
    <div class='explain-box'>
        <strong>About this project:</strong> This dashboard presents findings from a machine learning
        study that predicts poverty rates for all 64 districts of Bangladesh using freely available
        satellite and geospatial data. The ground truth poverty labels come from the
        <strong>HIES 2022 survey</strong> (Bangladesh Bureau of Statistics). Navigate using the
        sidebar to explore the interactive map, test the live predictor, or review model performance.
    </div>
    """, unsafe_allow_html=True)

    # Stat cards
    c1, c2, c3, c4 = st.columns(4)
    stats = [
        ("64",    "Districts Analyzed",          c1),
        ("19",    "Satellite Features",           c2),
        ("0.733", "Moran's I · Poverty Clusters", c3),
        ("3.63",  "Best RMSE (pp)",               c4),
    ]
    for num, label, col in stats:
        with col:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-number'>{num}</div>
                <div class='stat-label'>{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    # Side-by-side maps
    st.markdown("### 🗺️ Poverty Rate vs Nighttime Light Intensity")
    st.markdown("""
    <div class='explain-box'>
        Compare the two maps below. Poorer divisions (Rangpur, Mymensingh, Barishal) appear
        darker in the nighttime light map — consistent with less economic activity. Dhaka and
        Chattogram are the brightest, reflecting their industrial and urban concentration.
        <strong>Note:</strong> poverty labels are at division level (8 divisions),
        which is why districts in the same division share the same shade.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    def make_choropleth(color_col, title, colorscale, label, vmin=None, vmax=None):
        fig = px.choropleth_mapbox(
            gdf,
            geojson=geojson,
            locations=gdf.index,
            color=color_col,
            hover_name='district_name',
            hover_data={'division_name': True, color_col: ':.2f'},
            color_continuous_scale=colorscale,
            range_color=[vmin, vmax] if vmin is not None else None,
            mapbox_style='carto-darkmatter',
            zoom=5.5,
            center={'lat': 23.7, 'lon': 90.3},
            opacity=0.75,
            labels={color_col: label}
        )
        fig.update_layout(
            height=430,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='#060810',
            plot_bgcolor='#060810',
            font=dict(color='#e2e8f0', family='Space Grotesk'),
            coloraxis_colorbar=dict(
                title=label,
                tickfont=dict(color='#94a3b8'),
                title_font=dict(color='#94a3b8'),
                bgcolor='#0a0f1e',
                bordercolor='#1e2d4a',
            )
        )
        return fig

    with col1:
        st.markdown("**Poverty Rate (HCR %)**")
        st.plotly_chart(
            make_choropleth('poverty_hcr', 'Poverty Rate', 'Reds', 'HCR (%)', 14, 27),
            use_container_width=True
        )

    with col2:
        st.markdown("**Mean Nighttime Light (2022)**")
        st.plotly_chart(
            make_choropleth('ntl_mean', 'NTL Mean', 'YlOrRd', 'Radiance'),
            use_container_width=True
        )

    st.markdown("---")

    # Key findings
    st.markdown("### 🔬 Key Research Findings")
    f1, f2, f3 = st.columns(3)

    findings = [
        ("🌍", "Strong Spatial Clustering",
         "Poverty clusters strongly across Bangladesh (Moran's I = 0.733, p < 0.001). "
         "Poor districts neighbor poor districts — geography is as important as satellite features.",
         "#1e3a5f", "#60a5fa"),
        ("🌙", "Context Beats Individual Signal",
         "The average nighttime light of neighbouring districts (spatial lag) is more predictive "
         "than a district's own NTL value. This justifies using spatial features in the model.",
         "#1a3a1a", "#4ade80"),
        ("🏔️", "Terrain Shapes Economic Geography",
         "Elevation mean is the single most important feature (19.2% importance). "
         "The Chittagong Hill Tracts, coastal delta, and northern flatlands each have "
         "distinct poverty signatures.",
         "#3a1a0a", "#fb923c"),
    ]

    for col, (icon, title, text, bg, accent) in zip([f1, f2, f3], findings):
        with col:
            st.markdown(f"""
            <div class='finding-card' style='border-color:{accent}22'>
                <div class='finding-icon'>{icon}</div>
                <div class='finding-title' style='color:{accent}'>{title}</div>
                <div class='finding-text'>{text}</div>
            </div>
            """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# PAGE 2 — EXPLORE MAP
# ════════════════════════════════════════════════════════════
elif page == "🗺️ Explore Map":
    st.markdown("## 🗺️ Explore Districts")

    st.markdown("""
    <div class='explain-box'>
        <strong>How to use:</strong> The choropleth map shows poverty rates by district
        (red = higher poverty). <strong>Click any blue dot</strong> to select a district —
        the panel on the right updates with that district's satellite features, RF model
        prediction, and a SHAP chart showing which features drove the prediction.
        Green bars push the prediction <em>down</em> (less poverty),
        red bars push it <em>up</em> (more poverty).
    </div>
    """, unsafe_allow_html=True)

    col_map, col_detail = st.columns([3, 2])

    with col_map:
        with st.spinner("🗺️ Building map — first load takes ~10 seconds..."):
            m        = build_folium_map_cached(gdf, centroids)
            map_data = st_folium(
                m,
                width=700,
                height=520,
                returned_objects=["last_object_clicked_popup"]
            )

    with col_detail:
        clicked = None
        if map_data and map_data.get('last_object_clicked_popup'):
            clicked = map_data['last_object_clicked_popup']

        if clicked and clicked in df['district_name'].values:
            row      = df[df['district_name'] == clicked].iloc[0]
            shap_row = shap_df[shap_df['district_name'] == clicked].iloc[0]

            st.markdown(f"### 📍 {clicked}")
            st.markdown(f"<div style='color:#64748b;font-size:0.85rem'>Division: <strong style='color:#94a3b8'>{row['division_name']}</strong></div>",
                        unsafe_allow_html=True)

            # Poverty badge
            val   = row['poverty_hcr']
            pred  = row['poverty_predicted']
            err   = abs(pred - val)
            color = '#ef4444' if val > 22 else '#f59e0b' if val > 18 else '#22c55e'

            st.markdown(f"""
            <div class='district-card'>
                <div style='color:#64748b;font-size:0.78rem;
                            text-transform:uppercase;letter-spacing:0.08em'>
                    Poverty Rate (HCR)
                </div>
                <div class='pred-badge'
                     style='color:{color};border:1.5px solid {color};
                            background:{color}18;margin:8px 0'>
                    {val:.1f}%
                </div>
                <div style='color:#64748b;font-size:0.8rem;margin-top:6px'>
                    RF Predicted: <strong style='color:#94a3b8'>{pred:.1f}%</strong>
                    &nbsp;·&nbsp; Error: <strong style='color:#94a3b8'>{err:.1f} pp</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Feature table
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Satellite Features**")
            feat_display = {
                '🌙 NTL Mean':       (row['ntl_mean'],        '.3f',  ''),
                '🌿 NDVI':           (row['ndvi_mean'],        '.3f',  ''),
                '🏔️ Elevation':      (row['elevation_mean'],  '.1f',  ' m'),
                '🛣️ Road Density':   (row['road_density'],    '.2f',  ' km/km²'),
                '🏙️ Urban Fraction': (row['urban_fraction']*100, '.1f', '%'),
                '💧 Water Fraction': (row['water_fraction']*100, '.1f', '%'),
            }
            for k, (v, fmt, unit) in feat_display.items():
                ca, cb = st.columns([2, 1])
                ca.markdown(f"<span style='font-size:0.82rem;color:#64748b'>{k}</span>",
                            unsafe_allow_html=True)
                cb.markdown(f"<span style='font-size:0.82rem;color:#e2e8f0;font-weight:600'>{v:{fmt.replace(':','')}}{unit}</span>",
                            unsafe_allow_html=True)

            # SHAP chart
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**What drove this prediction?**")
            st.caption("🟢 Green = reduces poverty prediction · 🔴 Red = increases it")

            shap_vals = shap_row.drop('district_name')
            shap_vals = pd.to_numeric(shap_vals, errors='coerce').dropna()
            top_shap  = shap_vals.abs().nlargest(6)
            shap_plot = pd.DataFrame({
                'feature': top_shap.index,
                'shap':    [shap_vals[f] for f in top_shap.index]
            })
            shap_plot['color'] = shap_plot['shap'].apply(
                lambda x: '#ef4444' if x > 0 else '#22c55e'
            )

            fig_shap = go.Figure(go.Bar(
                x=shap_plot['shap'],
                y=shap_plot['feature'],
                orientation='h',
                marker_color=shap_plot['color'],
                marker_line_width=0,
            ))
            fig_shap.add_vline(x=0, line_color='#334155', line_width=1)
            fig_shap.update_layout(
                height=240,
                margin=dict(l=0, r=0, t=8, b=0),
                paper_bgcolor='#0a0f1e',
                plot_bgcolor='#0a0f1e',
                font=dict(color='#94a3b8', family='Space Grotesk', size=11),
                xaxis=dict(gridcolor='#1e2d4a', title='SHAP value',
                           title_font=dict(size=10)),
                yaxis=dict(gridcolor='#1e2d4a'),
            )
            st.plotly_chart(fig_shap, use_container_width=True)

        else:
            st.markdown("""
            <div style='background:#0a0f1e;border:1px dashed #1e2d4a;
                        border-radius:12px;padding:48px 24px;text-align:center;
                        margin-top:24px'>
                <div style='font-size:2.4rem;margin-bottom:12px'>🖱️</div>
                <div style='color:#475569;font-size:0.9rem;line-height:1.6'>
                    Click any <strong style='color:#60a5fa'>blue dot</strong>
                    on the map<br>to explore that district's data
                </div>
            </div>
            """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# PAGE 3 — LIVE PREDICTOR
# ════════════════════════════════════════════════════════════
elif page == "🎛️ Live Predictor":
    st.markdown("## 🎛️ Live Poverty Predictor")

    st.markdown("""
    <div class='explain-box'>
        <strong>How this works:</strong> Adjust the 6 satellite feature sliders below.
        The trained Random Forest model instantly predicts what poverty rate a district
        with these characteristics would have. The remaining 13 features are held at
        their national median. <br><br>
        <strong>Try this:</strong> Set high elevation + low NTL to simulate a
        Chittagong Hill Tract district. Or set high urban fraction + high NTL for
        a Dhaka-like urban district. Watch the gauge respond in real time.
    </div>
    """, unsafe_allow_html=True)

    col_sliders, col_output = st.columns([2, 3])

    with col_sliders:
        st.markdown("### Adjust Features")

        sliders = [
            ("ntl_mean",       "🌙 NTL Mean (Nighttime Light)",   0.01),
            ("ndvi_mean",      "🌿 NDVI (Vegetation Index)",       0.01),
            ("elevation_mean", "🏔️ Elevation Mean (m)",           0.5),
            ("road_density",   "🛣️ Road Density (km/km²)",        0.1),
            ("urban_fraction", "🏙️ Urban Fraction",               0.001),
            ("water_fraction", "💧 Water Fraction",               0.001),
        ]

        slider_vals = {}
        for col_name, label, step in sliders:
            slider_vals[col_name] = st.slider(
                label,
                float(df[col_name].min()),
                float(df[col_name].max()),
                float(df[col_name].median()),
                step
            )

    with col_output:
        # Build input vector
        input_dict = {f: float(df[f].median()) for f in features}
        input_dict.update(slider_vals)

        input_df     = pd.DataFrame([input_dict])[features]
        input_scaled = scaler.transform(input_df)
        prediction   = float(np.clip(model.predict(input_scaled)[0], 14.8, 26.9))

        if prediction > 23:
            color, label, bg = '#ef4444', 'High Poverty',     '#ef444410'
        elif prediction > 19:
            color, label, bg = '#f59e0b', 'Moderate Poverty', '#f59e0b10'
        else:
            color, label, bg = '#22c55e', 'Lower Poverty',    '#22c55e10'

        # Prediction card
        st.markdown(f"""
        <div style='background:{bg};border:2px solid {color};
                    border-radius:16px;padding:32px;text-align:center;
                    margin-bottom:20px'>
            <div style='color:#64748b;font-size:0.78rem;text-transform:uppercase;
                        letter-spacing:0.1em;font-weight:600'>
                Predicted Poverty Rate
            </div>
            <div style='font-size:4rem;font-weight:800;color:{color};
                        font-family:JetBrains Mono,monospace;line-height:1.1;
                        margin:12px 0'>
                {prediction:.1f}%
            </div>
            <div style='color:{color};font-size:0.95rem;font-weight:600'>
                {label}
            </div>
            <div style='color:#475569;font-size:0.78rem;margin-top:8px'>
                Headcount Ratio · Upper Poverty Line · HIES 2022
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Similar districts
        df['_dist'] = (df['poverty_predicted'] - prediction).abs()
        similar     = df.nsmallest(3, '_dist')[
            ['district_name', 'division_name', 'poverty_hcr']
        ]
        df.drop(columns='_dist', inplace=True)

        st.markdown("**📍 Most similar districts:**")
        for _, r in similar.iterrows():
            st.markdown(
                f"<div style='font-size:0.85rem;color:#94a3b8;padding:3px 0'>"
                f"· <strong>{r['district_name']}</strong> "
                f"<span style='color:#475569'>({r['division_name']})</span> "
                f"— actual: <strong style='color:#60a5fa'>{r['poverty_hcr']}%</strong>"
                f"</div>",
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Gauge
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prediction,
            number={
                'suffix': '%',
                'font': {'color': color, 'size': 32, 'family': 'JetBrains Mono'}
            },
            gauge={
                'axis': {
                    'range': [14, 27],
                    'tickcolor': '#475569',
                    'tickfont': {'color': '#475569', 'size': 10}
                },
                'bar':     {'color': color, 'thickness': 0.25},
                'bgcolor': '#0a0f1e',
                'bordercolor': '#1e2d4a',
                'steps': [
                    {'range': [14, 19], 'color': '#052e16'},
                    {'range': [19, 23], 'color': '#431407'},
                    {'range': [23, 27], 'color': '#450a0a'},
                ],
                'threshold': {
                    'line': {'color': '#94a3b8', 'width': 2},
                    'thickness': 0.75,
                    'value': df['poverty_hcr'].mean()
                }
            }
        ))
        fig_gauge.update_layout(
            height=260,
            margin=dict(l=20, r=20, t=20, b=0),
            paper_bgcolor='#060810',
            font=dict(color='#e2e8f0', family='Space Grotesk')
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.caption(
            f"White line = national average poverty ({df['poverty_hcr'].mean():.1f}%). "
            f"Green zone = lower poverty. Red zone = high poverty."
        )


# ════════════════════════════════════════════════════════════
# PAGE 4 — MODEL RESULTS
# ════════════════════════════════════════════════════════════
elif page == "📊 Model Results":
    st.markdown("## 📊 Model Results & Findings")

    st.markdown("""
    <div class='explain-box'>
        <strong>Evaluation method:</strong> All models were evaluated using
        <strong>Leave-One-Division-Out (LODO) Cross-Validation</strong> — the strictest
        spatial validation approach. The model trains on 7 divisions and tests on the
        held-out 8th division, rotating all 8 times. This prevents data leakage between
        geographically neighbouring districts, giving a realistic estimate of how the
        model would perform on genuinely unseen regions.
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(
        ["🏆 Model Comparison", "🔍 Feature Importance", "🗺️ Error Analysis"]
    )

    # ── Tab 1 — Model Comparison ──────────────────────────────
    with tab1:
        st.markdown("### Performance Summary")
        st.caption("Lower RMSE/MAE = better. Higher R² = better. Naive baseline always predicts the mean poverty rate.")

        results_df = pd.DataFrame({
            'Model': ['Naive Baseline', 'CNN ResNet-18', 'Random Forest'],
            'RMSE':  [4.163, 4.354, 3.626],
            'MAE':   [3.596, 3.188, 2.926],
            'R²':    [0.000, -0.094, 0.241],
        })

        # Highlight best row
        def highlight_best(row):
            style = [''] * len(row)
            if row['Model'] == 'Random Forest':
                style = ['background-color: #052e1644; color: #4ade80; font-weight:600'] * len(row)
            return style

        st.dataframe(
            results_df.style.apply(highlight_best, axis=1).format(
                {'RMSE': '{:.3f}', 'MAE': '{:.3f}', 'R²': '{:.3f}'}
            ),
            use_container_width=True,
            hide_index=True
        )

        col1, col2 = st.columns(2)

        layout_base = dict(
            paper_bgcolor='#0a0f1e',
            plot_bgcolor='#0a0f1e',
            font=dict(color='#94a3b8', family='Space Grotesk'),
            height=320,
            showlegend=False,
            yaxis=dict(gridcolor='#1e2d4a'),
            xaxis=dict(gridcolor='#1e2d4a'),
        )

        with col1:
            bar_colors = ['#475569', '#ef4444', '#22c55e']
            fig1 = go.Figure(go.Bar(
                x=results_df['Model'],
                y=results_df['RMSE'],
                marker_color=bar_colors,
                marker_line_width=0,
                text=results_df['RMSE'].round(3),
                textposition='outside',
                textfont=dict(color='#94a3b8', size=11)
            ))
            fig1.update_layout(
                title=dict(text='RMSE by Model (lower = better)',
                           font=dict(color='#e2e8f0', size=13)),
                **layout_base
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            r2_colors = ['#475569', '#ef4444', '#22c55e']
            fig2 = go.Figure(go.Bar(
                x=results_df['Model'],
                y=results_df['R²'],
                marker_color=r2_colors,
                marker_line_width=0,
                text=results_df['R²'].round(3),
                textposition='outside',
                textfont=dict(color='#94a3b8', size=11)
            ))
            fig2.update_layout(
                title=dict(text='R² by Model (higher = better)',
                           font=dict(color='#e2e8f0', size=13)),
                **layout_base
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Per-division table
        st.markdown("### Per-Division Error Breakdown")
        st.caption("Shows which regions are hardest to predict. Barishal and Rangpur (highest poverty) are most challenging.")

        div_results = pd.DataFrame({
            'Division':    ['Barishal', 'Chattogram', 'Dhaka', 'Khulna',
                           'Mymensingh', 'Rajshahi', 'Rangpur', 'Sylhet'],
            'Poverty HCR': ['26.9%', '15.8%', '17.9%', '14.8%',
                           '24.2%', '16.7%', '24.8%', '17.4%'],
            'Districts':   [6, 11, 13, 10, 4, 8, 8, 4],
            'RF RMSE':     [5.326, 2.364, 0.474, 4.180, 5.622, 2.039, 4.057, 2.514],
            'CNN RMSE':    [10.439, 1.264, 1.984, 1.020, 3.636, 2.630, 7.284, 1.685],
        })
        st.dataframe(
            div_results.style.background_gradient(
                subset=['RF RMSE', 'CNN RMSE'],
                cmap='RdYlGn_r'
            ).format({'RF RMSE': '{:.3f}', 'CNN RMSE': '{:.3f}'}),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("""
        <div class='explain-box' style='margin-top:16px'>
            <strong>Key finding:</strong> Random Forest outperforms CNN on overall RMSE
            because CNN needs thousands of training samples to generalize — we only have 64 districts.
            However, CNN achieves better MAE (3.14 vs 2.93), suggesting it makes fewer large errors
            on well-represented divisions (Dhaka, Khulna, Chattogram).
        </div>
        """, unsafe_allow_html=True)

    # ── Tab 2 — Feature Importance ────────────────────────────
    with tab2:
        st.markdown("### Feature Importance (Random Forest)")
        st.caption("Mean decrease in impurity — higher = more important for poverty prediction.")

        feat_imp = pd.DataFrame({
            'Feature':    features,
            'Importance': model.feature_importances_ * 100
        }).sort_values('Importance', ascending=True)

        feat_imp['Type'] = feat_imp['Feature'].apply(
            lambda x: 'Spatial Lag' if 'spatial_lag' in x else 'Satellite'
        )

        fig_imp = px.bar(
            feat_imp,
            x='Importance',
            y='Feature',
            color='Type',
            color_discrete_map={
                'Spatial Lag': '#f59e0b',
                'Satellite':   '#3b82f6'
            },
            orientation='h',
            labels={'Importance': 'Importance (%)'}
        )
        fig_imp.update_layout(
            height=580,
            paper_bgcolor='#0a0f1e',
            plot_bgcolor='#0a0f1e',
            font=dict(color='#94a3b8', family='Space Grotesk', size=11),
            xaxis=dict(gridcolor='#1e2d4a', title='Importance (%)'),
            yaxis=dict(gridcolor='#1e2d4a'),
            legend=dict(
                bgcolor='#0a0f1e',
                bordercolor='#1e2d4a',
                font=dict(color='#94a3b8')
            )
        )
        st.plotly_chart(fig_imp, use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
            <div class='explain-box'>
                <strong>🔵 Satellite features</strong> are direct measurements from
                remote sensing data — elevation, nighttime light intensity, vegetation
                index, road density, and more.
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown("""
            <div class='explain-box'>
                <strong>🟡 Spatial lag features</strong> are the weighted average of
                neighbouring districts' values. They collectively contribute ~29% of
                total importance — confirming that poverty is spatially structured.
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 3 — Error Analysis ────────────────────────────────
    with tab3:
        st.markdown("### Prediction Error Map")
        st.caption("Which districts are hardest to predict? Red = model overpredicts poverty. Blue = model underpredicts.")

        gdf['error'] = df['poverty_predicted'].values - df['poverty_hcr'].values

        fig_err = px.choropleth_mapbox(
            gdf,
            geojson=geojson,
            locations=gdf.index,
            color='error',
            hover_name='district_name',
            hover_data={'error': ':.2f'},
            color_continuous_scale='RdBu_r',
            range_color=[-6, 6],
            mapbox_style='carto-darkmatter',
            zoom=5.5,
            center={'lat': 23.7, 'lon': 90.3},
            opacity=0.8,
            labels={'error': 'Error (pp)'}
        )
        fig_err.update_layout(
            height=480,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='#060810',
            plot_bgcolor='#060810',
            font=dict(color='#e2e8f0', family='Space Grotesk'),
            coloraxis_colorbar=dict(
                title='Error (pp)',
                tickfont=dict(color='#94a3b8'),
                title_font=dict(color='#94a3b8'),
                bgcolor='#0a0f1e',
                bordercolor='#1e2d4a',
            )
        )
        st.plotly_chart(fig_err, use_container_width=True)

        st.markdown("""
        <div class='explain-box'>
            <strong>Spatial bias pattern:</strong> Barishal (south) is systematically
            underpredicted (blue) — the model cannot reach the true 26.9% poverty rate
            from satellite features alone. Rangpur (north) is also challenging. This
            reflects a known limitation: with only 8 discrete poverty labels, tree-based
            models regress toward the mean. This is an honest limitation discussed in the
            research paper.
        </div>
        """, unsafe_allow_html=True)