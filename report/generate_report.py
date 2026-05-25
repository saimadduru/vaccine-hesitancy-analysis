"""Generates HTML + PDF research brief for Vaccine Hesitancy study."""

import base64, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def b64(path):
    with open(path, "rb") as f: return base64.b64encode(f.read()).decode()

imgs = {k: b64(f"output/figures/{k}.png") for k in
        ["fig1_hesitancy_distribution","fig2_sir_model","fig3_predictors","fig4_state_hesitancy"]}

# ── HTML ──────────────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Vaccine Hesitancy & SIR Modeling — Sai Manasa Adduru</title>
<style>
  :root{{--blue:#1B4F8A;--teal:#2AAFA4;--red:#C0392B;--green:#27AE60;--gray:#6C757D;--light:#F0F4F8;}}
  *{{box-sizing:border-box;margin:0;padding:0;}}
  body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#222;line-height:1.65;font-size:15px;}}
  header{{background:linear-gradient(135deg,var(--blue),var(--teal));color:white;padding:48px 40px 40px;}}
  header h1{{font-size:1.6rem;font-weight:700;margin-bottom:8px;line-height:1.3;}}
  header .meta{{opacity:.85;font-size:.9rem;margin-top:12px;}}
  .badge{{display:inline-block;background:rgba(255,255,255,.2);border:1px solid rgba(255,255,255,.4);border-radius:20px;padding:3px 12px;font-size:.78rem;margin:4px 4px 0 0;}}
  .container{{max-width:1000px;margin:0 auto;padding:40px 24px;}}
  h2{{font-size:1.1rem;font-weight:700;color:var(--blue);border-left:4px solid var(--teal);padding-left:12px;margin:32px 0 14px;text-transform:uppercase;letter-spacing:.03em;}}
  .abstract{{background:var(--light);border-left:4px solid var(--teal);border-radius:0 8px 8px 0;padding:20px 24px;margin:24px 0;}}
  .kpi-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:16px;margin:24px 0;}}
  .kpi{{background:var(--light);border-radius:10px;padding:20px 16px;text-align:center;border-top:3px solid var(--teal);}}
  .kpi .number{{font-size:2rem;font-weight:800;color:var(--blue);line-height:1;}}
  .kpi .label{{font-size:.8rem;color:var(--gray);margin-top:6px;}}
  .kpi .sub{{font-size:.75rem;color:#999;margin-top:4px;}}
  figure{{margin:28px 0;}}
  figure img{{width:100%;border-radius:8px;border:1px solid #e8edf2;box-shadow:0 2px 12px rgba(0,0,0,.07);}}
  figcaption{{font-size:.82rem;color:var(--gray);margin-top:8px;font-style:italic;padding:0 4px;}}
  table{{width:100%;border-collapse:collapse;font-size:.88rem;margin:16px 0;}}
  th{{background:var(--blue);color:white;padding:10px 14px;text-align:left;font-size:.82rem;}}
  td{{padding:9px 14px;border-bottom:1px solid #e8edf2;}}
  tr:nth-child(even) td{{background:var(--light);}}
  .highlight{{color:var(--teal);font-weight:700;}}
  .sig{{color:var(--red);font-weight:700;}}
  footer{{background:#1a1a2e;color:#aaa;text-align:center;padding:24px;font-size:.82rem;margin-top:48px;}}
  footer a{{color:var(--teal);text-decoration:none;}}
</style>
</head>
<body>
<header>
  <h1>Vaccine Hesitancy and Outbreak Dynamics:<br>A County-Level Epidemiologic Analysis with SIR Modeling</h1>
  <div class="meta">
    <strong>Sai Manasa Adduru</strong>, MPH (Epidemiology), PharmD &nbsp;|&nbsp; Portage County Combined General Health District Internship
    <br>
    <span class="badge">SIR Epidemic Modeling</span>
    <span class="badge">Logistic Regression</span>
    <span class="badge">Vaccine Hesitancy</span>
    <span class="badge">Public Health Surveillance</span>
    <span class="badge">County-Level Analysis</span>
  </div>
</header>
<div class="container">
  <div class="abstract">
    <h3>Abstract</h3>
    <p><strong>Background:</strong> Vaccine hesitancy remains a significant threat to herd immunity and outbreak containment. Understanding the structural and behavioral drivers of hesitancy at the county level is essential for targeted public health intervention.</p>
    <p><strong>Methods:</strong> We analyzed 500 US counties using a synthetic dataset mirroring CDC vaccination records, Census demographics, and BRFSS survey data. Logistic regression identified independent predictors of high hesitancy (top tertile). SIR compartmental models (β=0.35, γ=0.10) simulated outbreak dynamics under three vaccination scenarios: high (75%), moderate (50%), and low/hesitant (25%) population immunity.</p>
    <p><strong>Results:</strong> Hesitancy score was strongly negatively correlated with vaccination rate (r=−0.934, p&lt;0.001). Rural counties showed significantly higher hesitancy (68.5 vs 58.2, p&lt;0.001). High hesitancy resulted in 17,375 excess infections per 100,000 versus a high-vaccination scenario. Prior flu vaccination rate and social trust were the strongest protective predictors; rural index and Republican vote share increased hesitancy risk.</p>
    <p><strong>Conclusion:</strong> Structural and behavioral factors drive vaccine hesitancy in predictable, measurable ways. Interventions targeting prior vaccine engagement, social trust, and rural healthcare access can meaningfully reduce community-level hesitancy and outbreak risk.</p>
  </div>

  <div class="kpi-grid">
    <div class="kpi"><div class="number">−0.934</div><div class="label">Hesitancy–Vaccination Correlation</div><div class="sub">p &lt; 0.001</div></div>
    <div class="kpi"><div class="number">17,375</div><div class="label">Excess Infections from Hesitancy</div><div class="sub">per 100,000 population</div></div>
    <div class="kpi"><div class="number">10.3pt</div><div class="label">Rural vs Urban Hesitancy Gap</div><div class="sub">68.5 vs 58.2 (p&lt;0.001)</div></div>
    <div class="kpi"><div class="number">33%</div><div class="label">Counties High Hesitancy</div><div class="sub">Top tertile threshold</div></div>
  </div>

  <h2>Methods</h2>
  <p>County-level analysis of 500 US counties (15 states) using synthetic data mirroring CDC vaccination surveillance, American Community Survey demographics, and BRFSS behavioral data. High hesitancy defined as top tertile of hesitancy score. Logistic regression adjusted for 7 predictors. SIR model simulated 365-day outbreak trajectories across vaccination scenarios starting from I₀=100 infected individuals per 100,000 population.</p>

  <h2>Hesitancy Distribution & Correlation with Vaccination</h2>
  <figure><img src="data:image/png;base64,{imgs['fig1_hesitancy_distribution']}" alt="Hesitancy distribution"><figcaption>Figure 1. (A) Vaccine hesitancy score distribution by urbanicity — rural counties show significantly higher hesitancy (p&lt;0.001). (B) Scatter plot of hesitancy score vs. vaccination rate — strong negative correlation (r=−0.934), color-coded by rural index.</figcaption></figure>

  <h2>SIR Outbreak Simulation</h2>
  <figure><img src="data:image/png;base64,{imgs['fig2_sir_model']}" alt="SIR model"><figcaption>Figure 2. (A) SIR model showing active infections over 365 days under three vaccination scenarios. High hesitancy accelerates the epidemic curve and shifts the peak earlier (Day 44 vs Day 75). (B) Total outbreak size — high hesitancy results in 93,090 total infections vs 75,715 in the high-vaccination scenario.</figcaption></figure>

  <h2>Predictors of High Hesitancy</h2>
  <figure><img src="data:image/png;base64,{imgs['fig3_predictors']}" alt="Forest plot — predictors"><figcaption>Figure 3. Forest plot of logistic regression odds ratios for predictors of high vaccine hesitancy. Red bars indicate risk factors (OR &gt;1); green bars indicate protective factors (OR &lt;1). All shown predictors significant at p&lt;0.001.</figcaption></figure>

  <h2>State-Level Hesitancy Profile</h2>
  <figure><img src="data:image/png;base64,{imgs['fig4_state_hesitancy']}" alt="State hesitancy"><figcaption>Figure 4. Mean vaccine hesitancy score by state, ranked lowest to highest. Color coding: green (&lt;50), yellow (50–65), red (&gt;65). Substantial geographic variation reflects differing social, political, and structural contexts across states.</figcaption></figure>

  <h2>Key Findings Table</h2>
  <table>
    <tr><th>Finding</th><th>Navigated</th><th>p-value</th></tr>
    <tr><td>Hesitancy–vaccination correlation</td><td class="highlight">r = −0.934</td><td class="sig">&lt;0.001</td></tr>
    <tr><td>Rural vs urban hesitancy score</td><td class="highlight">68.5 vs 58.2</td><td class="sig">&lt;0.001</td></tr>
    <tr><td>Excess infections (hesitant vs high-vax)</td><td class="highlight">17,375 per 100k</td><td>—</td></tr>
    <tr><td>Prior flu vax rate — OR (protective)</td><td class="highlight">0.00 [very low]</td><td class="sig">&lt;0.001</td></tr>
    <tr><td>Rural index — OR (risk)</td><td class="highlight">794 [elevated]</td><td class="sig">&lt;0.001</td></tr>
  </table>

  <h2>Discussion & Implications</h2>
  <p>This analysis demonstrates that vaccine hesitancy is not randomly distributed — it is structurally and behaviorally predictable. Rural geography, low social trust, and low prior vaccine engagement are robust, modifiable targets for public health messaging and outreach. The SIR simulations quantify the population-level cost of inaction: hesitancy translates directly into thousands of excess infections and earlier epidemic peaks that stress healthcare systems.</p>
  <p>For local health departments like Portage County, these findings support targeted outreach to rural, low-trust communities — particularly those with low prior flu vaccination — as the highest-yield intervention point. Building vaccine confidence before the next outbreak is both feasible and measurable.</p>
</div>
<footer>
  <p>Sai Manasa Adduru, MPH (Epidemiology), PharmD &nbsp;|&nbsp; <a href="mailto:saimanasaadduru@gmail.com">saimanasaadduru@gmail.com</a></p>
  <p style="margin-top:6px;font-size:.75rem;">Python 3.9 · pandas · scipy · statsmodels · matplotlib</p>
</footer>
</body></html>"""

os.makedirs("report", exist_ok=True)
with open("report/vaccine_hesitancy_report.html", "w") as f:
    f.write(html)
print("HTML report written to report/vaccine_hesitancy_report.html")

# ── PDF via reportlab ─────────────────────────────────────────
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Image as RLImage, Table, TableStyle, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import io
from PIL import Image as PILImage

DARK_BLUE = colors.HexColor("#1B4F8A")
TEAL      = colors.HexColor("#2AAFA4")
LIGHT_BG  = colors.HexColor("#F0F4F8")
RED_C     = colors.HexColor("#C0392B")

doc = SimpleDocTemplate("report/vaccine_hesitancy_report.pdf",
                         pagesize=letter,
                         topMargin=0.6*inch, bottomMargin=0.6*inch,
                         leftMargin=0.75*inch, rightMargin=0.75*inch)
styles = getSampleStyleSheet()
story  = []

def add_style(name, parent="Normal", **kwargs):
    s = ParagraphStyle(name, parent=styles[parent], **kwargs)
    return s

title_style = add_style("Title2", fontSize=16, fontName="Helvetica-Bold",
                         textColor=DARK_BLUE, spaceAfter=6, alignment=TA_LEFT)
subtitle_style = add_style("Sub", fontSize=10, textColor=TEAL,
                            fontName="Helvetica", spaceAfter=4)
author_style = add_style("Author", fontSize=9, textColor=colors.gray,
                          fontName="Helvetica", spaceAfter=12)
h2_style = add_style("H2", fontSize=11, fontName="Helvetica-Bold",
                      textColor=DARK_BLUE, spaceBefore=14, spaceAfter=6,
                      borderPad=4)
body_style = add_style("Body2", fontSize=9, fontName="Helvetica",
                        leading=14, spaceAfter=8, alignment=TA_JUSTIFY)
caption_style = add_style("Caption", fontSize=8, fontName="Helvetica-Oblique",
                           textColor=colors.gray, spaceAfter=10, alignment=TA_CENTER)
bold_style = add_style("Bold2", fontSize=9, fontName="Helvetica-Bold",
                        textColor=DARK_BLUE)

# Title block
story.append(Paragraph("Vaccine Hesitancy and Outbreak Dynamics:", title_style))
story.append(Paragraph("A County-Level Epidemiologic Analysis with SIR Modeling", title_style))
story.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=6))
story.append(Paragraph("Sai Manasa Adduru, MPH (Epidemiology), PharmD", author_style))
story.append(Paragraph("Portage County Combined General Health District · Public Health Internship", subtitle_style))
story.append(Paragraph("Methods: SIR Epidemic Modeling · Logistic Regression · County-Level Surveillance", subtitle_style))
story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey, spaceAfter=10))

# Abstract
story.append(Paragraph("ABSTRACT", h2_style))
story.append(Paragraph("<b>Background:</b> Vaccine hesitancy threatens herd immunity. Understanding county-level drivers enables targeted public health intervention. <b>Methods:</b> Analysis of 500 US counties (synthetic data mirroring CDC/BRFSS/Census). Logistic regression identified predictors of high hesitancy; SIR models (β=0.35, γ=0.10) simulated outbreak scenarios. <b>Results:</b> Hesitancy strongly negatively correlated with vaccination (r=−0.934). Rural counties more hesitant (68.5 vs 58.2, p&lt;0.001). High hesitancy produced 17,375 excess infections per 100,000. Prior flu vaccination and social trust were protective; rural index and political lean increased risk. <b>Conclusion:</b> Hesitancy is structurally predictable and targetable.", body_style))

# KPI table
story.append(Paragraph("KEY FINDINGS", h2_style))
kpi_data = [
    ["Metric", "Value", "Significance"],
    ["Hesitancy–Vaccination Correlation", "r = −0.934", "p < 0.001"],
    ["Excess Infections (Hesitant vs High-Vax)", "17,375 per 100,000", "—"],
    ["Rural vs Urban Hesitancy Score", "68.5 vs 58.2", "p < 0.001"],
    ["High Hesitancy Counties (33rd pctile)", "33% of counties", "—"],
    ["Peak epidemic day — High Hesitancy", "Day 44", "vs Day 75 (moderate vax)"],
]
t = Table(kpi_data, colWidths=[2.8*inch, 1.8*inch, 2.2*inch])
t.setStyle(TableStyle([
    ("BACKGROUND",  (0,0), (-1,0), DARK_BLUE),
    ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
    ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",    (0,0), (-1,-1), 8),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [LIGHT_BG, colors.white]),
    ("GRID",        (0,0), (-1,-1), 0.3, colors.lightgrey),
    ("TOPPADDING",  (0,0), (-1,-1), 5),
    ("BOTTOMPADDING",(0,0), (-1,-1), 5),
]))
story.append(t)
story.append(Spacer(1, 0.15*inch))

# Figures
for fig_key, caption in [
    ("fig1_hesitancy_distribution",
     "Figure 1. Hesitancy score distribution by urbanicity (A) and hesitancy vs vaccination scatter plot (B). Strong negative correlation (r=−0.934)."),
    ("fig2_sir_model",
     "Figure 2. SIR model active infections over 365 days (A) and total outbreak size by vaccination scenario (B). High hesitancy = 17,375 excess infections."),
    ("fig3_predictors",
     "Figure 3. Forest plot of predictors of high vaccine hesitancy. All predictors significant at p<0.001."),
    ("fig4_state_hesitancy",
     "Figure 4. Mean vaccine hesitancy score by state. Substantial geographic variation across 15 states."),
]:
    story.append(Paragraph(caption.split(".")[0] + ".", h2_style))
    img_path = f"output/figures/{fig_key}.png"
    pil = PILImage.open(img_path)
    w_px, h_px = pil.size
    max_w = 6.5 * inch
    scale = max_w / w_px
    img = RLImage(img_path, width=max_w, height=h_px * scale)
    story.append(img)
    story.append(Paragraph(caption, caption_style))

# Discussion
story.append(Paragraph("DISCUSSION & PUBLIC HEALTH IMPLICATIONS", h2_style))
story.append(Paragraph("Vaccine hesitancy is structurally and behaviorally predictable. Rural geography, low social trust, and low prior vaccine engagement are robust, modifiable targets. SIR simulations quantify the cost of inaction: hesitancy produces thousands of excess infections and earlier epidemic peaks. Targeted outreach to rural, low-trust communities — particularly those with low prior flu vaccination — represents the highest-yield intervention for local health departments.", body_style))

doc.build(story)
print("PDF report written to report/vaccine_hesitancy_report.pdf")
