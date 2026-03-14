# Data Dictionary

All features used in the Bangladesh Poverty Prediction model.
Generated from `master_features.csv` — 64 districts, 30 columns.

---

## Identity Columns

| Column | Type | Description |
|--------|------|-------------|
| `district_name` | string | District name in BBS standard spelling (64 districts) |
| `division_name` | string | Division the district belongs to (8 divisions) |

---

## Nighttime Light Features
**Source:** VIIRS DNB Monthly Composites (NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG)  
**Extracted via:** Google Earth Engine `reduceRegions()`  
**Period:** 2022 annual median composite  
**Unit:** Radiance (nW/cm²/sr)

| Column | Description |
|--------|-------------|
| `ntl_mean` | Mean nighttime light radiance across the district. Core economic activity proxy. |
| `ntl_std` | Standard deviation of light within the district. High = uneven urban-rural development. |
| `ntl_max` | Maximum radiance pixel. Captures the brightest urban core. |
| `ntl_min` | Minimum radiance. Near zero in rural areas. |
| `ntl_p25` | 25th percentile of radiance. Represents darker/poorer areas within the district. |
| `ntl_p75` | 75th percentile of radiance. Represents brighter/wealthier areas. |
| `ntl_iqr` | Interquartile range (p75 - p25). Measures inequality of light distribution. |
| `ntl_yoy_change` | Year-on-year change in mean NTL from 2021 to 2022. Recent economic momentum. |
| `ntl_trend` | Linear slope of NTL from 2018 to 2022. Positive = growing economy. |

---

## Population Features
**Source:** WorldPop GP 100m Population Density (WorldPop/GP/100m/pop)  
**Extracted via:** Google Earth Engine  
**Period:** 2020  
**Unit:** People per 100m x 100m pixel

| Column | Description |
|--------|-------------|
| `pop_density` | Average population density per pixel across the district. |
| `pop_total` | Total estimated population of the district (sum of all pixels). |

---

## Vegetation Feature
**Source:** MODIS Terra Vegetation Indices (MODIS/061/MOD13A3)  
**Extracted via:** Google Earth Engine  
**Period:** 2022 annual mean  
**Unit:** NDVI (dimensionless, -1 to 1)

| Column | Description |
|--------|-------------|
| `ndvi_mean` | Mean Normalized Difference Vegetation Index. Higher = more vegetation. Rural/agricultural proxy. |
| `ndvi_std` | Variation in vegetation within the district. Mixed urban-rural districts have higher std. |

---

## Land Cover Features
**Source:** ESA WorldCover v200 (ESA/WorldCover/v200)  
**Extracted via:** Google Earth Engine  
**Period:** 2021  
**Unit:** Fraction (0 to 1)

| Column | Description |
|--------|-------------|
| `urban_fraction` | Proportion of district classified as urban land (class 50). Strong poverty correlate. |
| `water_fraction` | Proportion of district covered by water bodies (class 80). High in coastal/delta districts. |

---

## Terrain Features
**Source:** SRTM Digital Elevation Model (USGS/SRTMGL1_003)  
**Extracted via:** Google Earth Engine  
**Unit:** Metres above sea level

| Column | Description |
|--------|-------------|
| `elevation_mean` | Average elevation. Low = coastal/delta. High = Chittagong Hill Tracts. |
| `elevation_std` | Variation in elevation. High = hilly terrain. Low = flat delta plains. |

---

## Infrastructure Features
**Source:** OpenStreetMap via OSMnx Python library  
**Extracted:** March 2024  
**Unit:** Kilometres / km²

| Column | Description |
|--------|-------------|
| `road_length_km` | Total length of driveable roads in the district (km). |
| `road_density` | Road length per sq km of district area. Development proxy normalized for size. |
| `area_sqkm` | District area in square kilometres (from projected geometry). |

---

## Engineered Features

| Column | Description |
|--------|-------------|
| `ntl_per_capita` | Mean NTL divided by population density. Economic activity per person. |
| `ntl_mean_spatial_lag` | Weighted average of neighbouring districts' NTL mean (Queen contiguity weights). |
| `ntl_per_capita_spatial_lag` | Weighted average of neighbouring districts' NTL per capita. |
| `ndvi_mean_spatial_lag` | Weighted average of neighbouring districts' NDVI mean. |
| `pop_density_spatial_lag` | Weighted average of neighbouring districts' population density. |

---

## Target Variables
**Source:** Household Income and Expenditure Survey 2022 (HIES 2022)  
**Publisher:** Bangladesh Bureau of Statistics (BBS)  
**Note:** Labels are at division level (8 divisions). All districts within a division share the same label.

| Column | Description |
|--------|-------------|
| `poverty_hcr` | **Main target Y.** Headcount ratio (%) — population below upper poverty line (2022). |
| `poverty_hcr_lower` | Headcount ratio below the lower (extreme) poverty line. |
| `poverty_change` | Change in upper HCR from 2016 to 2022. Negative = poverty reduced. |

---

## Model Output

| Column | Description |
|--------|-------------|
| `poverty_predicted` | Random Forest model prediction of poverty_hcr (in-sample fit). |
