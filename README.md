# Vaccine Hesitancy & SIR Outbreak Modeling
### County-Level Epidemiologic Analysis | Applied During Portage County Health Department Internship

**Author:** Sai Manasa Adduru, MPH (Epidemiology), PharmD
**Methods:** SIR Epidemic Modeling · Logistic Regression · Geospatial Analysis · BRFSS-style Survey Data

---

## Overview

This project examines the **epidemiologic and social drivers of COVID-19 vaccine hesitancy** across 500 US counties and quantifies the **outbreak consequences** of hesitancy using SIR transmission modeling — directly applied during my epidemiology internship at the Portage County Combined General Health District.

---

## Key Findings

| Finding | Result |
|---------|--------|
| Hesitancy ↔ Vaccination correlation | **r = −0.934** (p < 0.001) |
| Rural vs. urban hesitancy | **68.5 vs 58.2** score (p < 0.0001) |
| Excess infections from hesitancy | **17,375 per 100,000** population |
| Strongest protective predictor | Prior flu vaccination rate (OR = 0.00***) |
| Strongest risk predictor | Republican vote share, rural index (OR >> 1***) |

---

## SIR Model Scenarios

| Vaccination Scenario | Total Infected (per 100k) | Peak Day |
|----------------------|--------------------------|----------|
| High vaccination (75% immune) | 75,715 | Day 0 (contained) |
| Moderate vaccination (50%) | 85,693 | Day 75 |
| **High hesitancy (25% immune)** | **93,090** | **Day 44** |

High hesitancy results in **17,375 excess infections** and earlier peak — meaning faster healthcare system overload.

---

## Methods

- **Data:** Synthetic county-level dataset (N=500) mimicking CDC vaccination records + Census + BRFSS survey
- **SIR Model:** ODE-based compartmental model (β=0.35, γ=0.10) across 3 vaccination scenarios
- **Regression:** Logistic regression on 7 predictors of high hesitancy (top tertile)
- **Software:** Python 3.9 (pandas, scipy, statsmodels, matplotlib)

---

## Repository Structure

```
├── data/
│   ├── simulate_counties.py      # County-level synthetic data generator
│   └── county_vaccine_data.csv   # 500-county dataset
├── analysis/
│   └── hesitancy_analysis.py     # Full analysis: SIR + regression + figures
└── output/figures/               # 4 publication-quality figures
```

---

## Reproduce

```bash
git clone https://github.com/saimadduru/vaccine-hesitancy-analysis
cd vaccine-hesitancy-analysis
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 data/simulate_counties.py
python3 analysis/hesitancy_analysis.py
```

---

`Python 3.9` · `pandas` · `scipy` · `statsmodels` · `matplotlib` · `seaborn`
