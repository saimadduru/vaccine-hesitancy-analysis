"""
2025 Public Health HTML report — policy brief / health dept style.
Green/amber palette, informational layout, like a CDC brief.
"""
import base64, os

def b64(p):
    with open(p,"rb") as f: return base64.b64encode(f.read()).decode()

imgs = {k: b64(f"output/figures/{k}.png") for k in
        ["fig1_hesitancy_distribution","fig2_sir_model","fig3_predictors","fig4_state_hesitancy"]}

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Vaccine Hesitancy Analysis — Sai Manasa Adduru</title>
<style>
  :root {{ --green:#2D6A4F; --lgreen:#74C69D; --amber:#E9C46A; --orange:#F4A261;
           --red:#E76F51; --light:#F0FAF4; --dark:#1B3A2D; }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ font-family: "Helvetica Neue", Arial, sans-serif; font-size:14px;
          color:#222; background:#fff; line-height:1.65; }}
  .topbar {{ background:var(--green); color:white; padding:8px 32px;
             font-size:0.78rem; letter-spacing:0.05em; text-transform:uppercase; }}
  .hero {{ background:var(--light); border-bottom:4px solid var(--lgreen);
           padding:36px 48px 28px; }}
  .hero h1 {{ font-size:1.55rem; color:var(--dark); font-weight:700;
              line-height:1.3; margin-bottom:10px; }}
  .hero .byline {{ font-size:0.88rem; color:#555; }}
  .hero .tags span {{ display:inline-block; background:var(--green); color:white;
                      border-radius:3px; padding:2px 9px; font-size:0.72rem;
                      margin:6px 4px 0 0; }}
  .body {{ max-width:960px; margin:0 auto; padding:36px 32px; }}
  .callout-row {{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin:24px 0; }}
  .callout {{ background:var(--dark); color:white; border-radius:6px; padding:18px 14px; text-align:center; }}
  .callout .num {{ font-size:1.9rem; font-weight:800; color:var(--lgreen); }}
  .callout .lbl {{ font-size:0.72rem; color:#ccc; margin-top:4px; line-height:1.3; }}
  .section-head {{ display:flex; align-items:center; gap:10px; margin:28px 0 12px; }}
  .section-head .bar {{ width:5px; height:22px; background:var(--green); border-radius:2px; flex-shrink:0; }}
  .section-head h2 {{ font-size:1.05rem; font-weight:700; color:var(--dark);
                      text-transform:uppercase; letter-spacing:0.04em; }}
  p {{ margin-bottom:10px; }}
  .sidebar-layout {{ display:grid; grid-template-columns:2fr 1fr; gap:24px; margin:16px 0; }}
  .highlight-box {{ background:var(--light); border-left:4px solid var(--green);
                    padding:16px 18px; border-radius:0 6px 6px 0; font-size:0.88rem; }}
  figure {{ margin:20px 0; }}
  figure img {{ width:100%; border:1px solid #dde; border-radius:4px; }}
  figcaption {{ font-size:0.8rem; color:#666; margin-top:6px; font-style:italic; }}
  table {{ width:100%; border-collapse:collapse; font-size:0.87rem; margin:14px 0; }}
  th {{ background:var(--green); color:white; padding:9px 12px; text-align:left; font-size:0.82rem; }}
  td {{ padding:8px 12px; border-bottom:1px solid #e0ede5; }}
  tr:nth-child(even) td {{ background:var(--light); }}
  .footer {{ background:var(--dark); color:#aaa; text-align:center;
             padding:20px; font-size:0.8rem; margin-top:40px; }}
  .footer a {{ color:var(--lgreen); text-decoration:none; }}
</style>
</head>
<body>
<div class="topbar">Public Health Research · Epidemiology · Vaccine Hesitancy Surveillance</div>
<div class="hero">
  <h1>Vaccine Hesitancy and Outbreak Dynamics:<br>A County-Level Epidemiologic Analysis with SIR Modeling</h1>
  <p class="byline">Sai Manasa Adduru, MPH (Epidemiology), PharmD &nbsp;·&nbsp;
     Portage County Combined General Health District &nbsp;·&nbsp; 2025</p>
  <div class="tags">
    <span>SIR Epidemic Modeling</span>
    <span>County-Level Analysis</span>
    <span>Logistic Regression</span>
    <span>Vaccine Hesitancy</span>
    <span>Public Health Surveillance</span>
  </div>
</div>

<div class="body">
  <div class="callout-row">
    <div class="callout"><div class="num">−0.934</div><div class="lbl">Hesitancy–Vaccination Correlation (p&lt;0.001)</div></div>
    <div class="callout"><div class="num">17,375</div><div class="lbl">Excess Infections from Hesitancy per 100k</div></div>
    <div class="callout"><div class="num">10.3 pt</div><div class="lbl">Rural–Urban Hesitancy Gap (p&lt;0.001)</div></div>
    <div class="callout"><div class="num">Day 44</div><div class="lbl">Earlier Epidemic Peak in Hesitant Communities</div></div>
  </div>

  <div class="section-head"><div class="bar"></div><h2>Background & Purpose</h2></div>
  <p>Vaccine hesitancy — defined as the delay or refusal of vaccines despite availability — remains a critical threat to community immunity. During my epidemiology internship at Portage County Combined General Health District, I observed first-hand how localized hesitancy affected immunization rates and outbreak preparedness. This project applies county-level epidemiologic analysis and SIR transmission modeling to quantify the drivers and consequences of hesitancy across 500 US counties.</p>

  <div class="section-head"><div class="bar"></div><h2>Methods</h2></div>
  <div class="sidebar-layout">
    <p>500 US counties across 15 states. Synthetic dataset mirroring CDC vaccination surveillance, ACS demographics, and BRFSS behavioral health data. High hesitancy defined as top tertile of hesitancy score (n=165, 33%). Logistic regression on 7 predictors. SIR compartmental model (β=0.35, γ=0.10) simulated 365-day outbreaks from I₀=100 infections across three vaccination scenarios.</p>
    <div class="highlight-box">
      <strong>Covariates</strong><br>
      • % College educated<br>
      • Republican vote share<br>
      • Social trust score<br>
      • % Uninsured<br>
      • Prior flu vaccination<br>
      • Rural index<br>
      • Primary care access
    </div>
  </div>

  <div class="section-head"><div class="bar"></div><h2>Hesitancy Distribution</h2></div>
  <figure><img src="data:image/png;base64,{imgs['fig1_hesitancy_distribution']}" alt="Hesitancy distribution">
  <figcaption>Figure 1. Hesitancy score distribution by urbanicity (left) and scatter plot of hesitancy vs. vaccination rate (right). Rural counties show significantly higher hesitancy (68.5 vs 58.2, p&lt;0.001). Hesitancy and vaccination rates strongly negatively correlated (r=−0.934).</figcaption></figure>

  <div class="section-head"><div class="bar"></div><h2>SIR Outbreak Simulation</h2></div>
  <figure><img src="data:image/png;base64,{imgs['fig2_sir_model']}" alt="SIR model">
  <figcaption>Figure 2. SIR model curves for 3 vaccination scenarios (left) and total outbreak size comparison (right). High hesitancy accelerates the epidemic peak by 31 days and produces 17,375 excess infections per 100,000 population.</figcaption></figure>

  <div class="section-head"><div class="bar"></div><h2>Predictors of High Hesitancy</h2></div>
  <figure><img src="data:image/png;base64,{imgs['fig3_predictors']}" alt="Predictors">
  <figcaption>Figure 3. Logistic regression odds ratios for predictors of high vaccine hesitancy. All predictors significant at p&lt;0.001. Green = protective (OR&lt;1); Red = risk factor (OR&gt;1).</figcaption></figure>

  <div class="section-head"><div class="bar"></div><h2>State-Level Profile</h2></div>
  <figure><img src="data:image/png;base64,{imgs['fig4_state_hesitancy']}" alt="State profile">
  <figcaption>Figure 4. Mean vaccine hesitancy score by state across 15-state sample. Substantial geographic variation reflects differences in social, political, and structural contexts.</figcaption></figure>

  <div class="section-head"><div class="bar"></div><h2>Key Results</h2></div>
  <table>
    <tr><th>Finding</th><th>Result</th><th>Significance</th></tr>
    <tr><td>Hesitancy–vaccination correlation</td><td>r = −0.934</td><td>p &lt; 0.001</td></tr>
    <tr><td>Rural vs urban hesitancy score</td><td>68.5 vs 58.2 (+10.3 pts)</td><td>p &lt; 0.001</td></tr>
    <tr><td>Excess infections (hesitant vs high-vax)</td><td>17,375 per 100,000</td><td>Model-derived</td></tr>
    <tr><td>Epidemic peak — High hesitancy vs High vax</td><td>Day 44 vs Day 0 (contained)</td><td>Model-derived</td></tr>
    <tr><td>Strongest protective predictor</td><td>Prior flu vaccination rate</td><td>p &lt; 0.001</td></tr>
    <tr><td>Strongest risk predictor</td><td>Republican vote share + Rural index</td><td>p &lt; 0.001</td></tr>
  </table>

  <div class="section-head"><div class="bar"></div><h2>Public Health Implications</h2></div>
  <p>Hesitancy is not randomly distributed — it is structurally and behaviorally predictable. This analysis supports targeted outreach strategies for local health departments: communities with low prior vaccination engagement, high rurality, and low social trust represent highest-priority intervention targets. Building trust before an outbreak is both measurable and achievable through community health worker programs, trusted messenger campaigns, and expanded primary care access in rural areas.</p>
</div>

<div class="footer">
  Sai Manasa Adduru, MPH (Epidemiology), PharmD &nbsp;|&nbsp;
  <a href="mailto:saimanasaadduru@gmail.com">saimanasaadduru@gmail.com</a> &nbsp;|&nbsp;
  <a href="https://github.com/saimadduru/vaccine-hesitancy-analysis">GitHub</a>
  <br><span style="font-size:0.72rem;margin-top:4px;display:block;">Python 3.9 · pandas · scipy · statsmodels · seaborn · matplotlib</span>
</div>
</body></html>"""

os.makedirs("report", exist_ok=True)
with open("report/vaccine_hesitancy_report.html","w") as f: f.write(html)
print("HTML written — 2025 public health style")
