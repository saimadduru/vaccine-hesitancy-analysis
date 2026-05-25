"""
Regenerate figures in 2025 public health style:
- seaborn-based
- Green/amber public health palette
- CDC/health dept report aesthetic
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.integrate import odeint
from scipy import stats
import statsmodels.formula.api as smf
import warnings, os

warnings.filterwarnings("ignore")
os.makedirs("output/figures", exist_ok=True)

# 2025 public health style
sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams.update({
    "figure.facecolor": "white",
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# Public health color palette
PH_GREEN  = "#2D6A4F"
PH_LGREEN = "#74C69D"
PH_AMBER  = "#E9C46A"
PH_ORANGE = "#F4A261"
PH_RED    = "#E76F51"
PH_GRAY   = "#8B8B8B"
PH_LIGHT  = "#F8FBF8"

df = pd.read_csv("data/county_vaccine_data.csv")

# Logistic regression model
formula = "high_hesitancy ~ pct_college_educated + pct_republican_vote + social_trust_score + pct_uninsured + prior_flu_vax_rate + rural_index + primary_care_per_100k"
model = smf.logit(formula, data=df).fit(disp=0)

# SIR
def sir(y, t, beta, gamma):
    S,I,R = y; N=S+I+R
    return [-beta*S*I/N, beta*S*I/N-gamma*I, gamma*I]
t = np.linspace(0,365,365); N_pop=100000; I0=100
scenarios = {
    "High Vaccination (75%)":    {"vax":0.75,"color":PH_GREEN,"ls":"-"},
    "Moderate Vaccination (50%)":{"vax":0.50,"color":PH_AMBER,"ls":"--"},
    "High Hesitancy (25%)":      {"vax":0.25,"color":PH_RED,  "ls":"-."},
}
sir_res = {}
for label,cfg in scenarios.items():
    immune=int(cfg["vax"]*N_pop); S0=N_pop-immune-I0
    sol=odeint(sir,[S0,I0,immune],t,args=(0.35,0.10))
    sir_res[label]={"sol":sol,"total":N_pop-sol[-1,0],"peak":sol[:,1].max(),"peak_day":sol[:,1].argmax(),**cfg}

# ── Figure 1 ─────────────────────────────────────────────────
fig, axes = plt.subplots(1,2,figsize=(13,5.5))
fig.patch.set_facecolor("white")

ax = axes[0]
rural  = df[df.rural_index>df.rural_index.median()]["hesitancy_score"]
urban  = df[df.rural_index<=df.rural_index.median()]["hesitancy_score"]
ax.hist(urban, bins=28, alpha=0.65, color=PH_GREEN,  label=f"Urban (n={len(urban)})",
        edgecolor="white", linewidth=0.5)
ax.hist(rural, bins=28, alpha=0.65, color=PH_ORANGE, label=f"Rural (n={len(rural)})",
        edgecolor="white", linewidth=0.5)
_,p = stats.ttest_ind(rural, urban)
ax.axvline(rural.mean(),  color=PH_RED,   ls="--", lw=1.5, alpha=0.8)
ax.axvline(urban.mean(),  color=PH_GREEN, ls="--", lw=1.5, alpha=0.8)
ax.set_xlabel("Vaccine Hesitancy Score (0–100)", labelpad=8)
ax.set_ylabel("Number of Counties")
ax.set_title(f"Hesitancy by Urbanicity\n(Rural mean={rural.mean():.1f}  Urban mean={urban.mean():.1f}  p<0.001)")
ax.legend(framealpha=0.9, fontsize=9)
ax.set_facecolor(PH_LIGHT)

ax = axes[1]
sc = ax.scatter(df.hesitancy_score, df.vaccination_rate*100,
                c=df.rural_index, cmap="YlGn_r", alpha=0.55, s=28, edgecolors="none")
plt.colorbar(sc, ax=ax, label="Rural Index", shrink=0.8)
m,b = np.polyfit(df.hesitancy_score, df.vaccination_rate*100, 1)
x_l = np.linspace(df.hesitancy_score.min(), df.hesitancy_score.max(), 100)
ax.plot(x_l, m*x_l+b, color=PH_RED, lw=2.5, label=f"r = {df.hesitancy_score.corr(df.vaccination_rate):.3f}")
ax.set_xlabel("Vaccine Hesitancy Score"); ax.set_ylabel("Vaccination Rate (%)")
ax.set_title("Hesitancy vs. Vaccination Rate\nby Urbanicity (Color = Rural Index)")
ax.legend(fontsize=10); ax.set_facecolor(PH_LIGHT)
plt.suptitle("County-Level Vaccine Hesitancy Distribution and Correlates", fontsize=12, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig("output/figures/fig1_hesitancy_distribution.png", dpi=170, bbox_inches="tight")
plt.close(); print("Fig 1 done")

# ── Figure 2 ─────────────────────────────────────────────────
fig, axes = plt.subplots(1,2,figsize=(13,5))
ax = axes[0]
for label,res in sir_res.items():
    ax.plot(t, res["sol"][:,1]/N_pop*100, color=res["color"],
            ls=res["ls"], lw=2.8, label=label)
ax.fill_between(t, sir_res["High Hesitancy (25%)"]["sol"][:,1]/N_pop*100,
                sir_res["High Vaccination (75%)"]["sol"][:,1]/N_pop*100,
                alpha=0.08, color=PH_RED, label="Excess burden from hesitancy")
ax.set_xlabel("Days from Initial Case"); ax.set_ylabel("Active Infections (% of population)")
ax.set_title("SIR Model — Active Infections Over Time")
ax.legend(fontsize=8, loc="upper right"); ax.set_facecolor(PH_LIGHT)

ax = axes[1]
names  = [l.split("(")[0].strip() for l in sir_res]
totals = [r["total"]/1000 for r in sir_res.values()]
clrs   = [r["color"] for r in sir_res.values()]
bars   = ax.bar(names, totals, color=clrs, width=0.5, edgecolor="white", linewidth=0.5)
for bar,val in zip(bars,totals):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.4,
            f"{val:.1f}k", ha="center", va="bottom", fontweight="bold", fontsize=10)
ax.set_ylabel("Total Infections (thousands per 100k pop)")
ax.set_title("Total Outbreak Size by Vaccination Level")
ax.set_facecolor(PH_LIGHT)
plt.suptitle("SIR Epidemic Simulation — Consequences of Vaccine Hesitancy", fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig("output/figures/fig2_sir_model.png", dpi=170, bbox_inches="tight")
plt.close(); print("Fig 2 done")

# ── Figure 3 ─────────────────────────────────────────────────
vars_p = ["pct_college_educated","pct_republican_vote","social_trust_score",
          "pct_uninsured","prior_flu_vax_rate","rural_index","primary_care_per_100k"]
lbls_p = ["% College Educated","% Republican Vote","Social Trust Score",
          "% Uninsured","Prior Flu Vax Rate","Rural Index","Primary Care / 100k"]
ORs  = [np.exp(model.params[v]) for v in vars_p]
CIs  = [(np.exp(model.conf_int().loc[v][0]), np.exp(model.conf_int().loc[v][1])) for v in vars_p]
pvals= [model.pvalues[v] for v in vars_p]

fig, ax = plt.subplots(figsize=(9,6))
for i,(OR,ci,p,lbl) in enumerate(zip(ORs,CIs,pvals,lbls_p)):
    col = PH_RED if OR>1 else PH_GREEN
    ax.barh(i, OR-1, left=1, height=0.5, color=col, alpha=0.25)
    ax.plot([ci[0],ci[1]],[i,i], color=col, lw=2.5, solid_capstyle="round")
    ax.scatter(OR, i, color=col, s=90, zorder=5)
    sig = "***" if p<0.001 else "**" if p<0.01 else "*" if p<0.05 else "ns"
    ax.text(max(ci[1],1.8), i, f" {sig}", va="center", fontsize=11, color=col, fontweight="bold")
ax.axvline(1.0, color="black", ls="-", lw=1.5, alpha=0.4)
ax.set_yticks(range(len(vars_p))); ax.set_yticklabels(lbls_p, fontsize=10)
ax.set_xlabel("Odds Ratio (95% Confidence Interval)")
ax.set_title("Predictors of High Vaccine Hesitancy\nLogistic Regression — Odds Ratios with 95% CI")
ax.set_facecolor(PH_LIGHT)
plt.tight_layout()
plt.savefig("output/figures/fig3_predictors.png", dpi=170, bbox_inches="tight")
plt.close(); print("Fig 3 done")

# ── Figure 4 ─────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11,5.5))
state_avg = df.groupby("state")[["hesitancy_score","vaccination_rate"]].mean().sort_values("hesitancy_score")
bar_colors = [PH_GREEN if s<50 else PH_AMBER if s<65 else PH_RED for s in state_avg.hesitancy_score]
bars = ax.barh(state_avg.index, state_avg.hesitancy_score,
               color=bar_colors, edgecolor="white", height=0.65)
for bar,val in zip(bars,state_avg.hesitancy_score):
    ax.text(val+0.4, bar.get_y()+bar.get_height()/2, f"{val:.1f}",
            va="center", fontsize=9, color="#333")
ax.axvline(50, color="gray", ls=":", lw=1.2, alpha=0.6)
ax.set_xlabel("Mean Vaccine Hesitancy Score")
ax.set_title("Mean Vaccine Hesitancy Score by State\n(Green <50 · Amber 50–65 · Red >65)")
ax.set_facecolor(PH_LIGHT)
plt.tight_layout()
plt.savefig("output/figures/fig4_state_hesitancy.png", dpi=170, bbox_inches="tight")
plt.close(); print("Fig 4 done — all figures regenerated in 2025 public health style")
