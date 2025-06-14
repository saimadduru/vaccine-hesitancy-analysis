"""
Vaccine Hesitancy & SIR Outbreak Modeling
County-level epidemiologic analysis of COVID-19 vaccination uptake
Author: Sai Manasa Adduru, MPH, PharmD
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.integrate import odeint
from scipy import stats
import statsmodels.formula.api as smf
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import warnings, os

warnings.filterwarnings("ignore")
os.makedirs("output/figures", exist_ok=True)

BLUE  = "#1B4F8A"
RED   = "#C0392B"
GREEN = "#27AE60"
GOLD  = "#F39C12"
GRAY  = "#7F8C8D"
LIGHT = "#F4F6F7"

plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "white",
    "axes.spines.top": False, "axes.spines.right": False,
    "font.family": "sans-serif", "font.size": 11,
    "axes.titlesize": 12, "axes.titleweight": "bold",
})

df = pd.read_csv("data/county_vaccine_data.csv")
print(f"\n{'='*60}")
print("  VACCINE HESITANCY EPIDEMIOLOGIC ANALYSIS")
print(f"  N = {len(df)} counties  |  States = {df.state.nunique()}")
print(f"{'='*60}\n")

# ── 1. Descriptive Stats ─────────────────────────────────────
print("DESCRIPTIVE STATISTICS")
print(f"  Mean hesitancy score:      {df.hesitancy_score.mean():.1f}/100")
print(f"  Mean vaccination rate:     {df.vaccination_rate.mean():.1%}")
print(f"  High hesitancy counties:   {df.high_hesitancy.sum()} ({df.high_hesitancy.mean():.0%})")
print(f"  Correlation (hesitancy↔vax): r = {df.hesitancy_score.corr(df.vaccination_rate):.3f}")

# ── 2. Predictors of High Hesitancy — Logistic Regression ────
predictors = ["pct_college_educated","median_household_income","pct_uninsured",
              "primary_care_per_100k","pct_republican_vote","social_trust_score",
              "prior_flu_vax_rate","rural_index"]

formula = "high_hesitancy ~ pct_college_educated + pct_republican_vote + social_trust_score + pct_uninsured + prior_flu_vax_rate + rural_index + primary_care_per_100k"
model = smf.logit(formula, data=df).fit(disp=0)

print("\nLOGISTIC REGRESSION — Predictors of High Hesitancy")
results = []
for var in ["pct_college_educated","pct_republican_vote","social_trust_score",
            "pct_uninsured","prior_flu_vax_rate","rural_index","primary_care_per_100k"]:
    OR  = np.exp(model.params[var])
    ci  = np.exp(model.conf_int().loc[var])
    p   = model.pvalues[var]
    sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
    results.append({"Predictor": var, "OR": round(OR,2), "95% CI": f"[{ci[0]:.2f},{ci[1]:.2f}]", "p": f"{p:.4f}", "": sig})
    print(f"  {var:35s}  OR={OR:.2f}  {sig}")

# ── 3. SIR Model ─────────────────────────────────────────────
def sir(y, t, beta, gamma):
    S, I, R = y
    N = S + I + R
    dS = -beta * S * I / N
    dI =  beta * S * I / N - gamma * I
    dR =  gamma * I
    return [dS, dI, dR]

t = np.linspace(0, 365, 365)
N_pop = 100000
I0, R0_init = 100, 0

scenarios = {
    "High Vaccination\n(75% immune)": {"vax": 0.75, "color": GREEN,  "ls": "-"},
    "Moderate Vaccination\n(50% immune)": {"vax": 0.50, "color": GOLD, "ls": "--"},
    "High Hesitancy\n(25% immune)":  {"vax": 0.25, "color": RED,   "ls": "-."},
}

beta  = 0.35
gamma = 0.10

print("\nSIR MODEL — Outbreak Simulation by Vaccination Scenario")
sir_results = {}
for label, cfg in scenarios.items():
    immune = int(cfg["vax"] * N_pop)
    S0 = N_pop - immune - I0
    sol = odeint(sir, [S0, I0, immune], t, args=(beta, gamma))
    total_infected = N_pop - sol[-1, 0]
    peak_infected  = sol[:, 1].max()
    peak_day       = sol[:, 1].argmax()
    sir_results[label] = {"sol": sol, "total_infected": total_infected,
                          "peak": peak_infected, "peak_day": peak_day, **cfg}
    name = label.split("\n")[0]
    print(f"  {name:30s}  Total infected: {total_infected:,.0f}  Peak day: {peak_day}")

# ── 4. FIGURES ────────────────────────────────────────────────
print("\nGENERATING FIGURES…")

# Figure 1 — Hesitancy Score Distribution by Rural/Urban
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

ax = axes[0]
rural_q  = df[df.rural_index > df.rural_index.median()]["hesitancy_score"]
urban_q  = df[df.rural_index <= df.rural_index.median()]["hesitancy_score"]
ax.hist(urban_q, bins=25, alpha=0.6, color=BLUE,  label=f"Urban (n={len(urban_q)})", density=True)
ax.hist(rural_q, bins=25, alpha=0.6, color=RED,   label=f"Rural (n={len(rural_q)})",  density=True)
t_stat, p = stats.ttest_ind(rural_q, urban_q)
ax.set_xlabel("Vaccine Hesitancy Score (0–100)")
ax.set_ylabel("Density")
ax.set_title(f"Figure 1A — Hesitancy by Urbanicity\n(p={p:.4f}, rural higher)")
ax.legend(); ax.set_facecolor(LIGHT)

ax = axes[1]
ax.scatter(df.hesitancy_score, df.vaccination_rate * 100,
           c=df.rural_index, cmap="RdYlBu_r", alpha=0.5, s=30, edgecolors="none")
r, p_r = stats.pearsonr(df.hesitancy_score, df.vaccination_rate)
m, b = np.polyfit(df.hesitancy_score, df.vaccination_rate * 100, 1)
x_line = np.linspace(df.hesitancy_score.min(), df.hesitancy_score.max(), 100)
ax.plot(x_line, m * x_line + b, color=BLUE, lw=2.5)
ax.text(0.05, 0.08, f"r = {r:.3f}  p < 0.001", transform=ax.transAxes, fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#ccc"))
ax.set_xlabel("Vaccine Hesitancy Score")
ax.set_ylabel("Vaccination Rate (%)")
ax.set_title("Figure 1B — Hesitancy vs. Vaccination Rate\n(Color = rural index)")
ax.set_facecolor(LIGHT)
plt.tight_layout()
plt.savefig("output/figures/fig1_hesitancy_distribution.png", dpi=180, bbox_inches="tight")
plt.close(); print("  ✓ Figure 1 saved")

# Figure 2 — SIR Curves
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

ax = axes[0]
for label, res in sir_results.items():
    ax.plot(t, res["sol"][:, 1] / N_pop * 100,
            color=res["color"], ls=res["ls"], lw=2.5,
            label=label.replace("\n", " "))
ax.set_xlabel("Days"); ax.set_ylabel("Infected (% of population)")
ax.set_title("Figure 2A — SIR Model: Active Infections Over Time")
ax.legend(fontsize=8); ax.set_facecolor(LIGHT)

ax = axes[1]
categories = [l.split("\n")[0] for l in sir_results.keys()]
totals     = [r["total_infected"] / 1000 for r in sir_results.values()]
colors     = [r["color"] for r in sir_results.values()]
bars = ax.bar(categories, totals, color=colors, width=0.5, edgecolor="white")
for bar, val in zip(bars, totals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f"{val:.1f}k", ha="center", va="bottom", fontweight="bold", fontsize=10)
ax.set_ylabel("Total Infected (thousands, per 100k pop)")
ax.set_title("Figure 2B — Total Outbreak Size by Vaccination Scenario")
ax.set_facecolor(LIGHT)
plt.suptitle("SIR Epidemic Simulation — Impact of Vaccine Hesitancy on Outbreak Dynamics",
             fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig("output/figures/fig2_sir_model.png", dpi=180, bbox_inches="tight")
plt.close(); print("  ✓ Figure 2 saved")

# Figure 3 — Predictor Forest Plot
fig, ax = plt.subplots(figsize=(9, 5.5))
vars_plot = ["pct_college_educated","pct_republican_vote","social_trust_score",
             "pct_uninsured","prior_flu_vax_rate","rural_index","primary_care_per_100k"]
labels_plot = ["% College Educated","% Republican Vote","Social Trust Score",
               "% Uninsured","Prior Flu Vax Rate","Rural Index","Primary Care per 100k"]
ORs  = [np.exp(model.params[v]) for v in vars_plot]
CIs  = [(np.exp(model.conf_int().loc[v][0]), np.exp(model.conf_int().loc[v][1])) for v in vars_plot]
pvals = [model.pvalues[v] for v in vars_plot]
colors_fp = [RED if OR > 1 else GREEN for OR in ORs]
y = range(len(vars_plot))
for i, (OR, ci, p, col) in enumerate(zip(ORs, CIs, pvals, colors_fp)):
    ax.plot([ci[0], ci[1]], [i, i], color=col, lw=2, alpha=0.7)
    ax.scatter(OR, i, color=col, s=100, zorder=5)
    sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
    ax.text(max(ci[1], OR) + 0.05, i, sig, va="center", fontsize=11, color=col)
ax.axvline(1.0, color="black", ls="--", lw=1.2, alpha=0.5, label="OR = 1.0 (no effect)")
ax.set_yticks(list(y)); ax.set_yticklabels(labels_plot)
ax.set_xlabel("Odds Ratio (95% CI)")
ax.set_title("Figure 3 — Predictors of High Vaccine Hesitancy\n(Red = increases hesitancy, Green = reduces hesitancy)")
ax.set_facecolor(LIGHT)
plt.tight_layout()
plt.savefig("output/figures/fig3_predictors.png", dpi=180, bbox_inches="tight")
plt.close(); print("  ✓ Figure 3 saved")

# Figure 4 — State-level hesitancy heatmap
fig, ax = plt.subplots(figsize=(11, 5))
state_avg = df.groupby("state")[["hesitancy_score","vaccination_rate"]].mean().sort_values("hesitancy_score", ascending=True)
colors_bar = [GREEN if r < 50 else GOLD if r < 65 else RED for r in state_avg["hesitancy_score"]]
bars = ax.barh(state_avg.index, state_avg["hesitancy_score"], color=colors_bar, edgecolor="white")
for bar, val in zip(bars, state_avg["hesitancy_score"]):
    ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
            f"{val:.1f}", va="center", fontsize=9)
ax.axvline(50, color="black", ls="--", lw=1, alpha=0.4, label="Score = 50")
ax.set_xlabel("Mean Vaccine Hesitancy Score (0–100)")
ax.set_title("Figure 4 — Mean Vaccine Hesitancy Score by State\n(Green < 50 · Yellow 50–65 · Red > 65)")
ax.set_facecolor(LIGHT)
plt.tight_layout()
plt.savefig("output/figures/fig4_state_hesitancy.png", dpi=180, bbox_inches="tight")
plt.close(); print("  ✓ Figure 4 saved")

# Summary
print(f"\n{'='*60}")
print("  KEY FINDINGS")
print(f"{'='*60}")
print(f"  Hesitancy-vaccination correlation: r = {r:.3f}")
print(f"  Rural counties hesitancy:  {rural_q.mean():.1f}  vs Urban: {urban_q.mean():.1f}  (p={p:.4f})")
print(f"  High vax scenario (75%):   {list(sir_results.values())[0]['total_infected']:,.0f} total infected")
print(f"  High hesitancy scenario:   {list(sir_results.values())[2]['total_infected']:,.0f} total infected")
diff = list(sir_results.values())[2]['total_infected'] - list(sir_results.values())[0]['total_infected']
print(f"  Excess infections from hesitancy: {diff:,.0f} per 100,000 population")
print(f"{'='*60}")
