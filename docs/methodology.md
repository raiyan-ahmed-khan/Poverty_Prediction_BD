# Methodology

Decisions made throughout the project, alternatives considered,
and justifications. This document forms the basis of the
Methods section of the research paper.

---

## 1. Problem Framing

**Decision:** Treat poverty prediction as a regression problem 
predicting the Headcount Ratio (HCR %) rather than a 
classification problem.

**Reason:** HCR is a continuous variable. Regression preserves 
the ordering and magnitude of poverty differences between 
divisions. Classification would lose information.

**Limitation acknowledged:** HIES 2022 only reports poverty at 
division level (8 values). All 64 districts within a division 
share the same label. This is the core challenge — we are 
essentially learning to predict 8 distinct values from 
district-level satellite features.

---

## 2. Spatial Unit of Analysis

**Decision:** Use districts (64) as the spatial unit, not 
divisions (8) or upazilas (490+).

**Reason:** 
- Divisions (8) are too few for ML — any model would 
  simply memorize 8 values.
- Upazilas (490+) have no reliable poverty labels available.
- Districts (64) give enough samples for meaningful ML while 
  having reasonably stable satellite feature aggregations.

---

## 3. Target Variable

**Decision:** Use upper poverty line HCR from HIES 2022.

**Alternatives considered:**
- Lower poverty line HCR — captures extreme poverty but 
  misses the moderately poor.
- Consumption expenditure — more granular but not publicly 
  available at district level.
- World Bank estimates — used as secondary cross-validation 
  source.

---

## 4. Feature Engineering

### NTL Temporal Features
**Decision:** Extract 5 years (2018–2022) to compute trend 
and year-on-year change rather than using single-year NTL.

**Reason:** Economic trajectory matters — a district with 
declining NTL may have higher poverty than its current 
absolute NTL suggests.

### NTL per Capita
**Decision:** Divide NTL by population density to create 
NTL per capita.

**Reason:** Raw NTL correlates with population size, not just 
wealth. Dhaka has high NTL partly because it has 10 million 
people, not just because it is wealthy.

### Spatial Lag Features
**Decision:** Compute Queen contiguity spatial lag for 
ntl_mean, ntl_per_capita, ndvi_mean, pop_density.

**Reason:** Moran's I test showed poverty has strong spatial 
autocorrelation (I = 0.733, p < 0.001). Neighboring districts' 
features are informative about a district's poverty level.

**Impact:** Spatial lag features contributed ~29% of total 
Random Forest feature importance, validating this decision.

---

## 5. Evaluation Strategy

**Decision:** Use Leave-One-Division-Out (LODO) 
cross-validation rather than standard k-fold.

**Reason:** Standard k-fold randomly splits districts, meaning 
training and test sets contain neighboring districts. Since 
poverty and satellite features are spatially autocorrelated 
(Moran's I = 0.733), this leaks information and inflates 
performance estimates.

**LODO approach:** Train on 7 divisions, test on 1, rotate 
all 8 times. This simulates predicting poverty in a genuinely 
unseen region.

**Limitation:** With only 8 folds, variance between folds is 
high. Some divisions (Mymensingh, Sylhet) have only 4 districts 
in the test set, making per-fold R² unstable.

---

## 6. Model Selection

### Baseline Models
Linear regression, Ridge, and Lasso were used as baselines. 
All performed worse than the naive mean predictor under LODO-CV 
(RMSE 16–28pp) due to high variance extrapolation — the linear 
models could not handle the large feature values of Dhaka 
district when trained on other divisions.

### Tree-Based Models
Random Forest (RMSE 3.626) and LightGBM (RMSE 3.673) both 
beat the naive baseline. Random Forest was selected as the 
final model due to:
- Marginally better RMSE
- More stable predictions (lower variance across folds)
- Better interpretability via SHAP

### Hyperparameter Tuning
GridSearchCV with LODO-CV was used. Best parameters:
`max_depth=None, max_features=0.7, min_samples_leaf=1, 
n_estimators=100`

### CNN Extension
ResNet-18 was fine-tuned on 4-band Sentinel-2 images 
(100m resolution, 224x224px). Despite using transfer learning 
from ImageNet, the CNN performed worse than RF under LODO-CV 
(RMSE 4.354 vs 3.626). This is expected with only 64 training 
samples — CNNs require thousands of examples to generalize.

**Key finding:** The CNN achieved better MAE (3.19 vs 2.93), 
suggesting it makes fewer large errors on well-represented 
divisions but struggles more on outlier divisions (Barishal, 
Rangpur).

---

## 7. Feature Importance Findings

Top features by Random Forest importance:
1. elevation_mean (19.2%) — terrain geography
2. ntl_mean_spatial_lag (17.3%) — neighboring NTL context
3. ntl_iqr (9.3%) — within-district light inequality
4. road_density (9.2%) — infrastructure
5. ntl_yoy_change (6.5%) — economic momentum

**Key insight:** The spatial lag of NTL (17.3%) is more 
important than the district's own NTL (2.3%). This means 
where a district is located matters more than its own 
nighttime light intensity.

---

## 8. Error Analysis

The model systematically underpredicts poverty in Barishal 
(true: 26.9%, predicted: ~21–22%) and Rangpur (true: 24.8%, 
predicted: ~20–21%).

**Possible explanations:**
- Barishal is a delta region with high water coverage — the 
  satellite signal may be attenuated by water bodies.
- Rangpur has unusually high road density for its poverty 
  level (rural feeder roads), which confounds the model.
- Both divisions have few districts (6 and 8) — the model 
  has less training data for these poverty levels.

---

## 9. Limitations

1. **Division-level labels:** 8 unique target values across 
   64 districts constrains model learning.
2. **Small sample size:** 64 districts is insufficient for 
   deep learning. CNN results should be interpreted cautiously.
3. **Cross-sectional:** Only 2022 data used for the final 
   model. Temporal poverty dynamics are not fully captured.
4. **Label mismatch:** HIES 2022 measures consumption poverty; 
   satellite data measures economic activity proxies. The 
   relationship is correlational, not causal.
5. **Spatial resolution:** Some small districts 
   (Narayanganj: 332x619 pixels at 100m) have limited 
   satellite coverage for CNN.
