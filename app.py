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
    /* Main background */
    .stApp { background-color: #0e1117; color: #fafafa; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    
    /* Metric cards */
    div[data-testid="metric-container"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 12px;
    }
    
    /* Headers */
    h1 { color: #58a6ff !important; }
    h2 { color: #58a6ff !important; }
    h3 { color: #e6edf3 !important; }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab"] {
        background-color: #161b22;
        color: #8b949e;
        border-radius: 6px 6px 0 0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f6feb !important;
        color: white !important;
    }
    
    /* Divider */
    hr { border-color: #30363d; }
    
    /* Stat card */
    .stat-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 5px;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #58a6ff;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #8b949e;
        margin-top: 4px;
    }
    
    /* Hero */
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: #58a6ff;
        line-height: 1.2;
    }
    .hero-sub {
        font-size: 1.1rem;
        color: #8b949e;
        margin-top: 10px;
    }
    
    /* District card */
    .district-card {
        background: #161b22;
        border: 1px solid #1f6feb;
        border-radius: 10px;
        padding: 16px;
        margin-top: 10px;
    }
    
    /* Prediction badge */
    .pred-badge {
        background: #1f6feb22;
        border: 1px solid #1f6feb;
        border-radius: 20px;
        padding: 6px 16px;
        display: inline-block;
        font-size: 1.4rem;
        font-weight: 700;
        color: #58a6ff;
    }
</style>
""", unsafe_allow_html=True)

# ── Data loading (cached) ─────────────────────────────────────
@st.cache_data
def load_data():
    df       = pd.read_csv("data/processed/master_features.csv")
    shap_df  = pd.read_csv("data/processed/shap_values.csv")
    gdf      = gpd.read_file("data/processed/master_features.gpkg")
    return df, shap_df, gdf

@st.cache_resource
def load_models():
    model    = joblib.load("models/random_forest_final.pkl")
    scaler   = joblib.load("models/scaler_final.pkl")
    features = joblib.load("models/feature_cols.pkl")
    return model, scaler, features

df, shap_df, gdf = load_data()
model, scaler, features = load_models()

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛰️ Bangladesh Poverty")
    st.markdown("*Predicting poverty from satellite data*")
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
    st.markdown("**Data Sources**")
    st.markdown("- VIIRS Nighttime Light")
    st.markdown("- Sentinel-2 Satellite")
    st.markdown("- HIES 2022 (BBS)")
    st.markdown("- OpenStreetMap")
    st.markdown("---")
    st.markdown("**Model**")
    st.markdown("Random Forest · 19 features")
    st.markdown("LODO-CV RMSE: **3.626 pp**")
    st.markdown("---")
    st.caption("ISRT · University of Dhaka · 2024")

# ════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ════════════════════════════════════════════════════════════
if page == "🏠 Overview":

    # Hero
    st.markdown("""
    <div style='padding: 40px 0 20px 0'>
        <div class='hero-title'>🛰️ Mapping Poverty<br>from Space</div>
        <div class='hero-sub'>
            Predicting regional poverty levels in Bangladesh<br>
            using satellite nighttime light &amp; geospatial features
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stat cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>64</div>
            <div class='stat-label'>Districts Analyzed</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>19</div>
            <div class='stat-label'>Satellite Features</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>0.733</div>
            <div class='stat-label'>Moran's I (Poverty Clustering)</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>3.63</div>
            <div class='stat-label'>Best RMSE (pp)</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Side by side maps
    st.markdown("### 🗺️ Poverty vs Nighttime Light")
    st.caption("Poorer divisions (north & south) have less satellite-detected light at night")

    col1, col2 = st.columns(2)

    with col1:
        fig_poverty = px.choropleth_mapbox(
            gdf,
            geojson=json.loads(gdf.to_json()),
            locations=gdf.index,
            color='poverty_hcr',
            hover_name='district_name',
            hover_data={'division_name': True,
                       'poverty_hcr': ':.1f'},
            color_continuous_scale='Reds',
            range_color=[14, 27],
            mapbox_style='carto-darkmatter',
            zoom=5.5,
            center={'lat': 23.7, 'lon': 90.3},
            opacity=0.75,
            title='Poverty Rate (HCR %)',
            labels={'poverty_hcr': 'HCR (%)'}
        )
        fig_poverty.update_layout(
            height=450,
            margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor='#0e1117',
            plot_bgcolor='#0e1117',
            font_color='#fafafa',
            coloraxis_colorbar=dict(
                title='HCR (%)',
                tickfont=dict(color='#fafafa')
                
            )
        )
        st.plotly_chart(fig_poverty, use_container_width=True)

    with col2:
        fig_ntl = px.choropleth_mapbox(
            gdf,
            geojson=json.loads(gdf.to_json()),
            locations=gdf.index,
            color='ntl_mean',
            hover_name='district_name',
            hover_data={'division_name': True,
                       'ntl_mean': ':.3f'},
            color_continuous_scale='YlOrRd',
            mapbox_style='carto-darkmatter',
            zoom=5.5,
            center={'lat': 23.7, 'lon': 90.3},
            opacity=0.75,
            title='Mean Nighttime Light (2022)',
            labels={'ntl_mean': 'Radiance'}
        )
        fig_ntl.update_layout(
            height=450,
            margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor='#0e1117',
            plot_bgcolor='#0e1117',
            font_color='#fafafa',
            coloraxis_colorbar=dict(
                title='Radiance',
                tickfont=dict(color='#fafafa')
                
            )
        )
        st.plotly_chart(fig_ntl, use_container_width=True)

    st.markdown("---")

    # Key findings
    st.markdown("### 🔬 Key Research Findings")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**🌍 Spatial Clustering**\n\nPoverty is strongly clustered (Moran's I = 0.733, p < 0.001). Poor districts neighbor poor districts — geography matters as much as features.")
    with col2:
        st.success("**🌙 NTL Spatial Lag Wins**\n\nNeighboring districts' nighttime light (spatial lag) is more predictive than a district's own light — context beats individual features.")
    with col3:
        st.warning("**🌄 Elevation Dominates**\n\nElevation mean is the single most important feature (19.2% importance). Terrain shapes economic geography across Bangladesh.")

# ════════════════════════════════════════════════════════════
# PAGE 2 — EXPLORE MAP
# ════════════════════════════════════════════════════════════
elif page == "🗺️ Explore Map":
    st.markdown("## 🗺️ Explore Districts")
    st.caption("Click any district on the map to see its satellite features and poverty prediction")

    col_map, col_detail = st.columns([3, 2])

    with col_map:
        # Build folium map
        m = folium.Map(
            location=[23.7, 90.3],
            zoom_start=7,
            tiles='CartoDB dark_matter'
        )

        # Choropleth layer
        folium.Choropleth(
            geo_data=gdf.__geo_interface__,
            data=df,
            columns=['district_name', 'poverty_hcr'],
            key_on='feature.properties.district_name',
            fill_color='RdYlGn_r',
            fill_opacity=0.7,
            line_opacity=0.3,
            line_color='white',
            legend_name='Poverty HCR (%)',
            name='Poverty Rate'
        ).add_to(m)

        # Clickable district markers
        for _, row in df.iterrows():
            centroid = gdf[gdf['district_name'] == row['district_name']].geometry.centroid.iloc[0]
            folium.CircleMarker(
                location=[centroid.y, centroid.x],
                radius=5,
                color='white',
                weight=1,
                fill=True,
                fill_color='#58a6ff',
                fill_opacity=0.7,
                tooltip=f"{row['district_name']}: {row['poverty_hcr']}%",
                popup=folium.Popup(row['district_name'], parse_html=True)
            ).add_to(m)

        map_data = st_folium(m, width=700, height=500)

    with col_detail:
        # Get clicked district
        clicked = None
        if map_data and map_data.get('last_object_clicked_popup'):
            clicked = map_data['last_object_clicked_popup']

        if clicked and clicked in df['district_name'].values:
            row      = df[df['district_name'] == clicked].iloc[0]
            shap_row = shap_df[shap_df['district_name'] == clicked].iloc[0]

            st.markdown(f"### 📍 {clicked}")
            st.markdown(f"**Division:** {row['division_name']}")

            # Poverty gauge
            poverty_val = row['poverty_hcr']
            color = '#ff4444' if poverty_val > 22 else '#ffaa00' if poverty_val > 18 else '#00cc44'
            st.markdown(f"""
            <div class='district-card'>
                <div style='color:#8b949e; font-size:0.85rem'>POVERTY RATE (HCR)</div>
                <div class='pred-badge' style='color:{color};border-color:{color};
                     background:{color}22'>{poverty_val:.1f}%</div>
                <div style='color:#8b949e; font-size:0.8rem; margin-top:8px'>
                RF Predicted: {row['poverty_predicted']:.1f}% &nbsp;|&nbsp;
                Error: {abs(row['poverty_predicted']-poverty_val):.1f} pp
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**Key Features:**")
            feat_display = {
                '🌙 NTL Mean':        f"{row['ntl_mean']:.3f}",
                '🌿 NDVI':            f"{row['ndvi_mean']:.3f}",
                '🏔️ Elevation':       f"{row['elevation_mean']:.1f} m",
                '🛣️ Road Density':    f"{row['road_density']:.2f} km/km²",
                '🏙️ Urban Fraction':  f"{row['urban_fraction']*100:.1f}%",
                '💧 Water Fraction':  f"{row['water_fraction']*100:.1f}%",
            }
            for k, v in feat_display.items():
                col_a, col_b = st.columns([2, 1])
                col_a.caption(k)
                col_b.caption(f"**{v}**")

            # SHAP bar chart
            st.markdown("**What drove this prediction?**")
            shap_vals = shap_row.drop('district_name')
            shap_vals = pd.to_numeric(shap_vals, errors='coerce').dropna()
            top_shap  = shap_vals.abs().nlargest(6)
            shap_plot = pd.DataFrame({
                'feature': top_shap.index,
                'shap':    [shap_vals[f] for f in top_shap.index]
            })
            shap_plot['color'] = shap_plot['shap'].apply(
                lambda x: '#ff4444' if x > 0 else '#00cc44'
            )
            fig_shap = go.Figure(go.Bar(
                x=shap_plot['shap'],
                y=shap_plot['feature'],
                orientation='h',
                marker_color=shap_plot['color'],
            ))
            fig_shap.update_layout(
                height=250,
                margin=dict(l=0, r=0, t=10, b=0),
                paper_bgcolor='#161b22',
                plot_bgcolor='#161b22',
                font_color='#fafafa',
                xaxis_title='SHAP value',
                xaxis=dict(gridcolor='#30363d'),
                yaxis=dict(gridcolor='#30363d'),
            )
            st.plotly_chart(fig_shap, use_container_width=True)

        else:
            st.markdown("""
            <div class='district-card' style='text-align:center; padding:40px'>
                <div style='font-size:2rem'>👆</div>
                <div style='color:#8b949e; margin-top:10px'>
                    Click any district on the map<br>to see its details
                </div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# PAGE 3 — LIVE PREDICTOR
# ════════════════════════════════════════════════════════════
elif page == "🎛️ Live Predictor":
    st.markdown("## 🎛️ Live Poverty Predictor")
    st.caption("Adjust satellite feature values to get a real-time poverty prediction from the Random Forest model")

    col_sliders, col_output = st.columns([2, 3])

    with col_sliders:
        st.markdown("### Adjust Features")

        ntl_mean       = st.slider("🌙 NTL Mean (Nighttime Light)",
                                    float(df['ntl_mean'].min()),
                                    float(df['ntl_mean'].max()),
                                    float(df['ntl_mean'].median()), 0.01)
        ndvi_mean      = st.slider("🌿 NDVI (Vegetation Index)",
                                    float(df['ndvi_mean'].min()),
                                    float(df['ndvi_mean'].max()),
                                    float(df['ndvi_mean'].median()), 0.01)
        elevation_mean = st.slider("🏔️ Elevation Mean (m)",
                                    float(df['elevation_mean'].min()),
                                    float(df['elevation_mean'].max()),
                                    float(df['elevation_mean'].median()), 0.5)
        road_density   = st.slider("🛣️ Road Density (km/km²)",
                                    float(df['road_density'].min()),
                                    float(df['road_density'].max()),
                                    float(df['road_density'].median()), 0.1)
        urban_fraction = st.slider("🏙️ Urban Fraction",
                                    float(df['urban_fraction'].min()),
                                    float(df['urban_fraction'].max()),
                                    float(df['urban_fraction'].median()), 0.001)
        water_fraction = st.slider("💧 Water Fraction",
                                    float(df['water_fraction'].min()),
                                    float(df['water_fraction'].max()),
                                    float(df['water_fraction'].median()), 0.001)

    with col_output:
        # Build full feature vector using median for non-slider features
        input_dict = {f: df[f].median() for f in features}
        input_dict.update({
            'ntl_mean':       ntl_mean,
            'ndvi_mean':      ndvi_mean,
            'elevation_mean': elevation_mean,
            'road_density':   road_density,
            'urban_fraction': urban_fraction,
            'water_fraction': water_fraction,
        })

        input_df     = pd.DataFrame([input_dict])[features]
        input_scaled = scaler.transform(input_df)
        prediction   = model.predict(input_scaled)[0]
        prediction   = float(np.clip(prediction, 14.8, 26.9))

        # Color coding
        if prediction > 23:
            color, label = '#ff4444', 'High Poverty'
        elif prediction > 19:
            color, label = '#ffaa00', 'Moderate Poverty'
        else:
            color, label = '#00cc44', 'Lower Poverty'

        # Prediction display
        st.markdown(f"""
        <div style='background:#161b22; border:2px solid {color};
             border-radius:16px; padding:32px; text-align:center;
             margin-bottom:20px'>
            <div style='color:#8b949e; font-size:0.9rem'>
                PREDICTED POVERTY RATE
            </div>
            <div style='font-size:4rem; font-weight:800; color:{color}'>
                {prediction:.1f}%
            </div>
            <div style='color:{color}; font-size:1rem; font-weight:600'>
                {label}
            </div>
            <div style='color:#8b949e; font-size:0.8rem; margin-top:8px'>
                Headcount Ratio (Upper Poverty Line · HIES 2022)
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Find similar districts
        df['_dist'] = (df['poverty_predicted'] - prediction).abs()
        similar = df.nsmallest(3, '_dist')[
            ['district_name', 'division_name', 'poverty_hcr', 'poverty_predicted']
        ]
        df.drop(columns='_dist', inplace=True)

        st.markdown("**📍 Most similar districts:**")
        for _, r in similar.iterrows():
            st.markdown(
                f"- **{r['district_name']}** ({r['division_name']}) "
                f"— actual: {r['poverty_hcr']}%"
            )

        # Gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prediction,
            number={'suffix': '%', 'font': {'color': color, 'size': 36}},
            gauge={
                'axis': {'range': [14, 27],
                         'tickcolor': '#8b949e',
                         'tickfont': {'color': '#8b949e'}},
                'bar':  {'color': color},
                'bgcolor': '#161b22',
                'steps': [
                    {'range': [14, 19], 'color': '#0d2b1a'},
                    {'range': [19, 23], 'color': '#2b2000'},
                    {'range': [23, 27], 'color': '#2b0000'},
                ],
                'threshold': {
                    'line': {'color': 'white', 'width': 2},
                    'thickness': 0.75,
                    'value': df['poverty_hcr'].mean()
                }
            }
        ))
        fig_gauge.update_layout(
            height=280,
            margin=dict(l=20, r=20, t=20, b=0),
            paper_bgcolor='#0e1117',
            font_color='#fafafa'
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.caption(f"White line = national average ({df['poverty_hcr'].mean():.1f}%)")

# ════════════════════════════════════════════════════════════
# PAGE 4 — MODEL RESULTS
# ════════════════════════════════════════════════════════════
elif page == "📊 Model Results":
    st.markdown("## 📊 Model Results & Findings")

    tab1, tab2, tab3 = st.tabs(
        ["🏆 Model Comparison", "🔍 Feature Importance", "🗺️ Error Analysis"]
    )

    with tab1:
        st.markdown("### Model Performance (LODO Cross-Validation)")
        st.caption("Leave-One-Division-Out CV — trained on 7 divisions, tested on 1, rotated 8 times")

        results_df = pd.DataFrame({
            'Model':      ['Naive Baseline', 'CNN ResNet-18', 'Random Forest'],
            'RMSE':       [4.163, 4.354, 3.626],
            'MAE':        [3.596, 3.188, 2.926],
            'R²':         [0.000, -0.094, 0.241],
        })

        col1, col2 = st.columns(2)
        with col1:
            fig_rmse = px.bar(
                results_df, x='Model', y='RMSE',
                color='RMSE',
                color_continuous_scale='RdYlGn_r',
                title='RMSE by Model (lower = better)',
                text='RMSE'
            )
            fig_rmse.update_traces(texttemplate='%{text:.3f}', textposition='outside')
            fig_rmse.update_layout(
                paper_bgcolor='#161b22', plot_bgcolor='#161b22',
                font_color='#fafafa', height=350,
                showlegend=False,
                yaxis=dict(gridcolor='#30363d'),
            )
            st.plotly_chart(fig_rmse, use_container_width=True)

        with col2:
            fig_r2 = px.bar(
                results_df, x='Model', y='R²',
                color='R²',
                color_continuous_scale='RdYlGn',
                title='R² by Model (higher = better)',
                text='R²'
            )
            fig_r2.update_traces(texttemplate='%{text:.3f}', textposition='outside')
            fig_r2.update_layout(
                paper_bgcolor='#161b22', plot_bgcolor='#161b22',
                font_color='#fafafa', height=350,
                showlegend=False,
                yaxis=dict(gridcolor='#30363d'),
            )
            st.plotly_chart(fig_r2, use_container_width=True)

        # Per-division table
        st.markdown("### Per-Division Error Breakdown")
        div_results = pd.DataFrame({
            'Division':   ['Barishal','Chattogram','Dhaka','Khulna',
                          'Mymensingh','Rajshahi','Rangpur','Sylhet'],
            'Poverty HCR':['26.9%','15.8%','17.9%','14.8%',
                          '24.2%','16.7%','24.8%','17.4%'],
            'Districts':  [6, 11, 13, 10, 4, 8, 8, 4],
            'RF RMSE':    [5.326, 2.364, 0.474, 4.180, 5.622, 2.039, 4.057, 2.514],
            'CNN RMSE':   [10.439, 1.264, 1.984, 1.020, 3.636, 2.630, 7.284, 1.685],
        })
        st.dataframe(
            div_results.style.background_gradient(
                subset=['RF RMSE', 'CNN RMSE'],
                cmap='RdYlGn_r'
            ),
            use_container_width=True,
            hide_index=True
        )

    with tab2:
        st.markdown("### Feature Importance (Random Forest)")
        st.caption("Mean decrease in impurity — how much each feature contributes to predictions")

        feat_imp = pd.DataFrame({
            'Feature':    features,
            'Importance': model.feature_importances_ * 100
        }).sort_values('Importance', ascending=True)

        feat_imp['Type'] = feat_imp['Feature'].apply(
            lambda x: 'Spatial Lag' if 'spatial_lag' in x else 'Satellite'
        )
        color_map = {'Spatial Lag': '#ff7f0e', 'Satellite': '#1f77b4'}

        fig_imp = px.bar(
            feat_imp, x='Importance', y='Feature',
            color='Type',
            color_discrete_map=color_map,
            orientation='h',
            title='Feature Importance (%)',
            labels={'Importance': 'Importance (%)'}
        )
        fig_imp.update_layout(
            height=600,
            paper_bgcolor='#161b22',
            plot_bgcolor='#161b22',
            font_color='#fafafa',
            xaxis=dict(gridcolor='#30363d'),
            yaxis=dict(gridcolor='#30363d'),
        )
        st.plotly_chart(fig_imp, use_container_width=True)

        st.info("**🔑 Key insight:** Spatial lag features (orange) — the average satellite values of *neighboring* districts — contribute ~29% of total importance. This confirms that poverty is spatially structured: where you are matters as much as what you measure.")

    with tab3:
        st.markdown("### Prediction Error Map")
        st.caption("Which districts are hardest to predict? Red = overpredicted, Blue = underpredicted")

        gdf['error'] = df['poverty_predicted'].values - df['poverty_hcr'].values

        fig_err = px.choropleth_mapbox(
            gdf,
            geojson=json.loads(gdf.to_json()),
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
            title='Prediction Error (pp)',
            labels={'error': 'Error (pp)'}
        )
        fig_err.update_layout(
            height=500,
            margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor='#0e1117',
            plot_bgcolor='#0e1117',
            font_color='#fafafa',
        )
        st.plotly_chart(fig_err, use_container_width=True)

        st.warning("**📌 Spatial bias pattern:** Barishal and Mymensingh (highest poverty divisions) are consistently underpredicted. The model pulls predictions toward the mean — a known limitation of tree-based models with discrete training labels.")