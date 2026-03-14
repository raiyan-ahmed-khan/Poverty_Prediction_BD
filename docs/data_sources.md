# Data Sources

All datasets used in this project. Every source is documented
for reproducibility and academic citation.

---

## Ground Truth / Target Variable

| Field | Detail |
|-------|--------|
| **Dataset** | Household Income and Expenditure Survey (HIES) 2022 |
| **Publisher** | Bangladesh Bureau of Statistics (BBS) |
| **URL** | https://bbs.gov.bd |
| **Access date** | January 2024 |
| **Variable used** | Upper poverty line headcount ratio by division |
| **Spatial resolution** | Division level (8 divisions) |
| **Notes** | Table 6.4, page 98 of the full report PDF |

---

## Satellite Features

### Nighttime Light (NTL)
| Field | Detail |
|-------|--------|
| **Dataset** | VIIRS Day/Night Band Monthly Composites V1 |
| **Collection ID** | NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG |
| **Platform** | Google Earth Engine |
| **URL** | https://developers.google.com/earth-engine/datasets/catalog/NOAA_VIIRS_DNB_MONTHLY_V1_VCMCFG |
| **Temporal coverage** | 2018–2022 (annual median composites) |
| **Spatial resolution** | ~500m |
| **Access date** | February 2024 |

### Vegetation Index (NDVI)
| Field | Detail |
|-------|--------|
| **Dataset** | MODIS Terra Vegetation Indices 1km Monthly |
| **Collection ID** | MODIS/061/MOD13A3 |
| **Platform** | Google Earth Engine |
| **URL** | https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD13A3 |
| **Temporal coverage** | 2022 annual mean |
| **Spatial resolution** | 1km |
| **Access date** | February 2024 |

### Land Cover
| Field | Detail |
|-------|--------|
| **Dataset** | ESA WorldCover v200 |
| **Collection ID** | ESA/WorldCover/v200 |
| **Platform** | Google Earth Engine |
| **URL** | https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v200 |
| **Temporal coverage** | 2021 |
| **Spatial resolution** | 10m |
| **Access date** | February 2024 |

### Elevation (SRTM)
| Field | Detail |
|-------|--------|
| **Dataset** | SRTM Digital Elevation Data Version 4 |
| **Collection ID** | USGS/SRTMGL1_003 |
| **Platform** | Google Earth Engine |
| **URL** | https://developers.google.com/earth-engine/datasets/catalog/USGS_SRTMGL1_003 |
| **Spatial resolution** | 30m |
| **Access date** | February 2024 |

### Sentinel-2 Satellite Imagery (CNN phase)
| Field | Detail |
|-------|--------|
| **Dataset** | Sentinel-2 MSI: MultiSpectral Instrument, Level-2A (Harmonized) |
| **Collection ID** | COPERNICUS/S2_SR_HARMONIZED |
| **Platform** | Google Earth Engine |
| **URL** | https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED |
| **Temporal coverage** | Nov 2022 – Mar 2023 (dry season, cloud-free) |
| **Spatial resolution** | 100m (resampled from 10m) |
| **Bands used** | B4 (Red), B3 (Green), B2 (Blue), B8 (NIR) |
| **Access date** | March 2024 |

---

## Population

| Field | Detail |
|-------|--------|
| **Dataset** | WorldPop Global Population Density 100m |
| **Collection ID** | WorldPop/GP/100m/pop |
| **Platform** | Google Earth Engine |
| **URL** | https://www.worldpop.org |
| **Temporal coverage** | 2020 |
| **Spatial resolution** | 100m |
| **Access date** | February 2024 |

---

## Administrative Boundaries

| Field | Detail |
|-------|--------|
| **Dataset** | GADM Bangladesh Level 2 (Districts) |
| **Version** | GADM 4.1 |
| **URL** | https://gadm.org/download_country.html |
| **Access date** | January 2024 |
| **Notes** | 64 districts. Some names standardized to BBS spelling (see src/name_mapping.py) |

---

## Road Network

| Field | Detail |
|-------|--------|
| **Dataset** | OpenStreetMap road network |
| **Tool** | OSMnx Python library v1.9.3 |
| **URL** | https://www.openstreetmap.org |
| **Access date** | March 2024 |
| **Network type** | Drive (driveable roads only) |

---

## Secondary / Cross-Validation

| Field | Detail |
|-------|--------|
| **Dataset** | World Bank Poverty Map of Bangladesh |
| **URL** | https://data.worldbank.org |
| **Access date** | January 2024 |
| **Notes** | Used for cross-validation of poverty labels |

---

## GEE Project
All Google Earth Engine extractions were performed under 
GEE Cloud Project: `poverty-prediction-489716`
