"""PDF — 2025 public health policy brief style. Green palette, left accent bar."""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Image as RLImage, Table, TableStyle,
                                 HRFlowable, KeepTogether)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from PIL import Image as PILImage

PH_GREEN  = colors.HexColor("#2D6A4F")
PH_LGREEN = colors.HexColor("#74C69D")
PH_AMBER  = colors.HexColor("#E9C46A")
PH_DARK   = colors.HexColor("#1B3A2D")
PH_LIGHT  = colors.HexColor("#F0FAF4")

doc = SimpleDocTemplate("report/vaccine_hesitancy_report.pdf", pagesize=letter,
                         topMargin=0.5*inch, bottomMargin=0.7*inch,
                         leftMargin=0.8*inch, rightMargin=0.75*inch)
styles = getSampleStyleSheet()

def s(name, parent="Normal", **kw):
    return ParagraphStyle(name, parent=styles[parent], **kw)

title_s   = s("T",  fontSize=16, fontName="Helvetica-Bold", textColor=PH_DARK, spaceAfter=5, leading=20)
sub_s     = s("S",  fontSize=10, fontName="Helvetica",      textColor=PH_GREEN, spaceAfter=3)
author_s  = s("A",  fontSize=9,  fontName="Helvetica",      textColor=colors.gray, spaceAfter=12)
h2_s      = s("H2", fontSize=10, fontName="Helvetica-Bold", textColor=PH_DARK,
               spaceBefore=14, spaceAfter=5, borderPad=3,
               borderColor=PH_GREEN, borderWidth=0, leftIndent=10,
               textTransform="uppercase")
body_s    = s("B",  fontSize=9,  fontName="Helvetica", leading=14, spaceAfter=7, alignment=TA_JUSTIFY)
caption_s = s("C",  fontSize=8,  fontName="Helvetica-Oblique", textColor=colors.gray, spaceAfter=10)
small_s   = s("Sm", fontSize=8,  fontName="Helvetica", textColor=colors.gray)

story = []

# Header band via table
hdr = Table([[
    Paragraph("Vaccine Hesitancy and Outbreak Dynamics:<br/>A County-Level Epidemiologic Analysis with SIR Modeling", title_s),
]], colWidths=[7*inch])
hdr.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1), PH_LIGHT),
    ("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14),
    ("TOPPADDING",(0,0),(-1,-1),14),("BOTTOMPADDING",(0,0),(-1,-1),10),
    ("LINEBELOW",(0,0),(-1,-1),3,PH_GREEN),
]))
story.append(hdr)
story.append(Paragraph("Sai Manasa Adduru, MPH (Epidemiology), PharmD  ·  Portage County Combined General Health District  ·  2025", author_s))
story.append(Paragraph("Methods: SIR Epidemic Modeling  ·  Logistic Regression  ·  County-Level Surveillance  ·  Python / seaborn", sub_s))
story.append(Spacer(1, 0.1*inch))

# KPI row
kpi = Table([
    [Paragraph("<font color='#2D6A4F'><b>−0.934</b></font><br/>Hesitancy–Vax Correlation", s("k1",fontSize=9,fontName="Helvetica",alignment=TA_CENTER,leading=13)),
     Paragraph("<font color='#2D6A4F'><b>17,375</b></font><br/>Excess Infections per 100k", s("k2",fontSize=9,fontName="Helvetica",alignment=TA_CENTER,leading=13)),
     Paragraph("<font color='#2D6A4F'><b>10.3 pts</b></font><br/>Rural–Urban Gap (p&lt;0.001)", s("k3",fontSize=9,fontName="Helvetica",alignment=TA_CENTER,leading=13)),
     Paragraph("<font color='#2D6A4F'><b>Day 44</b></font><br/>Epidemic Peak (High Hesitancy)", s("k4",fontSize=9,fontName="Helvetica",alignment=TA_CENTER,leading=13))],
], colWidths=[1.75*inch]*4)
kpi.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1),PH_DARK),("TEXTCOLOR",(0,0),(-1,-1),colors.white),
    ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
    ("LINEBEFORE",(1,0),(-1,-1),0.5,PH_LGREEN),
    ("ALIGN",(0,0),(-1,-1),"CENTER"),
]))
story.append(kpi); story.append(Spacer(1,0.12*inch))

story.append(Paragraph("BACKGROUND", h2_s))
story.append(HRFlowable(width="100%", thickness=1.5, color=PH_GREEN, spaceAfter=6))
story.append(Paragraph("Vaccine hesitancy poses a persistent threat to herd immunity and outbreak containment. During an epidemiology internship at Portage County Combined General Health District, I examined county-level patterns of vaccine uptake and applied SIR transmission modeling to quantify outbreak consequences of hesitancy. This brief presents results of that analysis across 500 US counties (15 states).", body_s))

story.append(Paragraph("METHODS", h2_s))
story.append(HRFlowable(width="100%", thickness=1.5, color=PH_GREEN, spaceAfter=6))
story.append(Paragraph("N=500 counties. Synthetic dataset mirroring CDC vaccination surveillance, ACS demographics, BRFSS behavioral data. High hesitancy = top tertile (n=165). Logistic regression (7 predictors). SIR model (β=0.35, γ=0.10) across 3 vaccination scenarios (25%, 50%, 75% immune). Analysis: Python 3.9, pandas, scipy, statsmodels, seaborn.", body_s))

for fig_key, sec, cap in [
    ("fig1_hesitancy_distribution","HESITANCY DISTRIBUTION",
     "Figure 1. Hesitancy distribution by urbanicity (left) and hesitancy vs. vaccination scatter (right). r=−0.934, p<0.001."),
    ("fig2_sir_model","SIR OUTBREAK SIMULATION",
     "Figure 2. SIR active infections over 365 days (left); total outbreak size by scenario (right). High hesitancy = 17,375 excess infections."),
    ("fig3_predictors","PREDICTORS OF HIGH HESITANCY",
     "Figure 3. Logistic regression ORs for predictors of high hesitancy. All significant at p<0.001."),
    ("fig4_state_hesitancy","STATE-LEVEL PROFILE",
     "Figure 4. Mean hesitancy score by state. Substantial geographic variation across the 15-state sample."),
]:
    story.append(Paragraph(sec, h2_s))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PH_GREEN, spaceAfter=6))
    pil = PILImage.open(f"output/figures/{fig_key}.png")
    w,h = pil.size; mw=6.4*inch
    story.append(RLImage(f"output/figures/{fig_key}.png", width=mw, height=h*(mw/w)))
    story.append(Paragraph(cap, caption_s))

story.append(Paragraph("KEY RESULTS", h2_s))
story.append(HRFlowable(width="100%", thickness=1.5, color=PH_GREEN, spaceAfter=6))
res = [
    ["Finding","Result","p-value"],
    ["Hesitancy–vaccination correlation","r = −0.934","< 0.001"],
    ["Rural vs urban hesitancy","68.5 vs 58.2 (+10.3 pts)","< 0.001"],
    ["Excess infections (hesitant vs high-vax)","17,375 per 100,000","Model"],
    ["Prior flu vax OR (protective)","Very low (strong protective)","< 0.001"],
]
t = Table(res, colWidths=[2.8*inch,2.5*inch,1.1*inch])
t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),PH_GREEN),("TEXTCOLOR",(0,0),(-1,0),colors.white),
    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),8.5),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[PH_LIGHT,colors.white]),
    ("GRID",(0,0),(-1,-1),0.3,colors.HexColor("#ccddcc")),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
]))
story.append(t)
story.append(Spacer(1,0.1*inch))
story.append(Paragraph("Software: Python 3.9  ·  pandas  ·  scipy  ·  statsmodels  ·  seaborn  ·  matplotlib", small_s))

doc.build(story)
print("PDF written — 2025 public health policy brief style")
