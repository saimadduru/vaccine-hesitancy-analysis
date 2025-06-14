"""
Synthetic county-level vaccine hesitancy dataset.
Mimics CDC vaccination data + Census + BRFSS survey structure.
500 US counties with realistic relationships between predictors and hesitancy.
"""

import numpy as np
import pandas as pd

np.random.seed(99)
N = 500

states = ["OH","PA","MI","IN","KY","WV","VA","NC","GA","FL","TX","IL","MO","TN","AL"]
state_col = np.random.choice(states, N)

rural_index      = np.random.beta(2, 3, N)
pct_college      = np.clip(np.random.normal(0.28, 0.10, N), 0.05, 0.65)
median_income    = np.clip(np.random.normal(52000, 14000, N), 22000, 110000)
pct_uninsured    = np.clip(np.random.normal(0.11, 0.05, N), 0.02, 0.28)
primary_care_per_100k = np.clip(np.random.normal(68, 22, N), 15, 140)
pct_republican   = np.clip(np.random.normal(0.52, 0.18, N), 0.10, 0.92)
social_trust     = np.clip(np.random.normal(0.55, 0.15, N), 0.15, 0.90)
prior_flu_vax    = np.clip(np.random.normal(0.48, 0.12, N), 0.18, 0.78)
covid_death_rate = np.clip(np.random.normal(180, 65, N), 40, 420)  # per 100k
population       = np.random.lognormal(10.8, 1.1, N).astype(int)

# Hesitancy score (0-100, higher = more hesitant)
hesitancy_logit = (
     1.2
    - 2.5 * pct_college
    - 0.8 * social_trust
    + 1.8 * pct_republican
    + 1.2 * rural_index
    + 0.9 * pct_uninsured
    - 1.1 * prior_flu_vax
    - 0.6 * (primary_care_per_100k / 100)
    + np.random.normal(0, 0.4, N)
)
hesitancy_score = np.clip(1 / (1 + np.exp(-hesitancy_logit)) * 100, 5, 95)

# Vaccination rate driven by hesitancy + access
vax_rate = np.clip(
    0.85
    - 0.007 * hesitancy_score
    - 0.3   * pct_uninsured
    + 0.15  * prior_flu_vax
    - 0.08  * rural_index
    + np.random.normal(0, 0.04, N),
    0.18, 0.92
)

# High hesitancy flag (top tertile)
high_hesitancy = (hesitancy_score >= np.percentile(hesitancy_score, 67)).astype(int)

df = pd.DataFrame({
    "county_id":             [f"CTY{str(i).zfill(4)}" for i in range(N)],
    "state":                 state_col,
    "population":            population,
    "rural_index":           rural_index.round(3),
    "pct_college_educated":  pct_college.round(3),
    "median_household_income": median_income.astype(int),
    "pct_uninsured":         pct_uninsured.round(3),
    "primary_care_per_100k": primary_care_per_100k.round(1),
    "pct_republican_vote":   pct_republican.round(3),
    "social_trust_score":    social_trust.round(3),
    "prior_flu_vax_rate":    prior_flu_vax.round(3),
    "covid_death_rate_100k": covid_death_rate.round(1),
    "hesitancy_score":       hesitancy_score.round(2),
    "vaccination_rate":      vax_rate.round(3),
    "high_hesitancy":        high_hesitancy,
})

df.to_csv("data/county_vaccine_data.csv", index=False)
print(f"Generated {N} counties")
print(f"Mean vaccination rate:  {df.vaccination_rate.mean():.1%}")
print(f"Mean hesitancy score:   {df.hesitancy_score.mean():.1f}/100")
print(f"High hesitancy counties:{df.high_hesitancy.sum()} ({df.high_hesitancy.mean():.0%})")
