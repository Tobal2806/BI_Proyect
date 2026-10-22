"""Builds report/GROUP_XX_W1_Report.pdf from the tables and figures produced by notebook 02 (data/processed, data/figures)."""
import pandas as pd
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping

R = Path(__file__).resolve().parent.parent  # GROUP_XX_W1 root folder
P, F = R/"data/processed", R/"data/figures"
D = "/usr/share/fonts/truetype/dejavu/"  # DejaVu fonts (Linux path); adjust on Windows
pdfmetrics.registerFont(TTFont("DV", D+"DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", D+"DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVI", D+"DejaVuSans-Oblique.ttf"))
addMapping("DV", 0, 0, "DV"); addMapping("DV", 1, 0, "DVB"); addMapping("DV", 0, 1, "DVI"); addMapping("DV", 1, 1, "DVB")

ss = getSampleStyleSheet()
INK, INK2 = colors.HexColor("#0b0b0b"), colors.HexColor("#52514e")
body = ParagraphStyle("b", parent=ss["Normal"], fontName="DV", fontSize=9.2, leading=12.6, alignment=TA_JUSTIFY, textColor=INK, spaceAfter=5)
small = ParagraphStyle("s", parent=body, fontSize=7.6, leading=9.6, alignment=0)
cell = ParagraphStyle("c", parent=body, fontSize=7.8, leading=9.8, alignment=0, spaceAfter=0)
cellb = ParagraphStyle("cb", parent=cell, fontName="DVB")
h1 = ParagraphStyle("h1", parent=body, fontName="DVB", fontSize=13, leading=16, spaceBefore=10, spaceAfter=6, alignment=0)
h2 = ParagraphStyle("h2", parent=body, fontName="DVB", fontSize=10.5, leading=13, spaceBefore=8, spaceAfter=4, alignment=0)
h3 = ParagraphStyle("h3", parent=body, fontName="DVB", fontSize=9.4, leading=12, spaceBefore=5, spaceAfter=3, textColor=INK2, alignment=0)
for _s in (h1, h2, h3): _s.keepWithNext = 1
title = ParagraphStyle("t", parent=body, fontName="DVB", fontSize=17, leading=21, alignment=0, spaceAfter=4)
cap = ParagraphStyle("cap", parent=small, textColor=INK2, spaceAfter=8)

S = []
def p(t, st=body): S.append(Paragraph(t, st))
def bullets(items):
    for it in items: S.append(Paragraph("• " + it, ParagraphStyle("bl", parent=body, leftIndent=10, firstLineIndent=-7, spaceAfter=2)))
def table(rows, widths, header=True):
    data = [[Paragraph(str(c), cellb if (header and i == 0) else cell) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, 0), 0.8, INK2),
          ("LINEBELOW", (0, -1), (-1, -1), 0.5, INK2), ("TOPPADDING", (0, 0), (-1, -1), 2.5),
          ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]
    for i in range(1, len(rows)):
        if i % 2 == 0: st.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#f3f3f1")))
    t.setStyle(TableStyle(st)); S.append(t); S.append(Spacer(1, 6))
def fig(path, w, caption):
    im = Image(str(path)); r = im.imageHeight / im.imageWidth; im.drawWidth = w; im.drawHeight = w*r
    S.append(KeepTogether([im, Paragraph(caption, cap)]))
pct = lambda x, d=1: f"{x*100:.{d}f}%"
num = lambda x: f"{x:,.0f}"
dec = lambda x, d=2: f"{x:.{d}f}"

# ---------- figures used in the text (read from the notebook outputs) ----------
cov = pd.read_csv(P/"t01_cobertura.csv", index_col=0)
qc = pd.read_csv(P/"t02_five_cs.csv")
tA1 = pd.read_csv(P/"tA1_fuera_region_por_region_residencia.csv", index_col=0)
tA2 = pd.read_csv(P/"tA2_top_flujos.csv")
tA3 = pd.read_csv(P/"tA3_fuera_region_por_complejidad.csv")
tB1 = pd.read_csv(P/"tB1_estancia_descriptiva.csv", index_col=0)
tB2 = pd.read_csv(P/"tB2_outliers.csv", index_col=0)
tB3 = pd.read_csv(P/"tB3_iema_por_hospital.csv", dtype={"COD_HOSPITAL": str})
outA = {y: tA1[f"outside_{y}"].sum()/tA1[f"n_{y}"].sum() for y in (2023, 2024)}
w = tB3.pivot(index="COD_HOSPITAL", columns="BASE_YEAR", values="IEMA").dropna()
r_iema = w.corr().iloc[0, 1]
b24 = tB3[tB3.BASE_YEAR == 2024]
lab = tA3.iloc[:, 1].astype(str); val = tA3.iloc[:, 2]
q4, q1 = val[lab.str.startswith("Q4")].iloc[0], val[lab.str.startswith("Q1")].iloc[0]
elective, emergency = val[lab == "Elective"].iloc[0], val[lab == "Emergency"].iloc[0]
MET, OHI = "Metropolitan (Santiago)", "O'Higgins"

# ---------------------------------- Title / summary ----------------------------------
p("W1 · Discovering questions worth investigating", title)
p("Business Intelligence IIB423T-1 · Universidad del Desarrollo · Instructor: Tomás Fontecilla Correa", small)
p("<b>Group:</b> GROUP_XX [COMPLETE ID] · <b>Members:</b> [COMPLETE] · <b>Submission:</b> 25-09-2026, version 1.1", small)
S.append(Spacer(1, 8))
p("<b>Summary.</b> This W1 checkpoint brings two candidate lines of inquiry, both based on FONASA's public Diagnosis-Related Groups (GRD) files "
  f"for discharge years 2023 and 2024 ({num(cov.loc[2023,'episodes'])} and {num(cov.loc[2024,'episodes'])} episodes). "
  "<b>A</b> examines hospitalisation outside the patient's region of residence within the network of GRD-funded hospitals. "
  "<b>B</b> examines case-mix-adjusted length of stay and the weight of extreme stays by hospital. "
  f"Real data were inspected for both. A shows clear regional differences (Metropolitan region ≈ {pct(tA1.loc[MET,'pct_2024'])} vs O'Higgins ≈ {pct(tA1.loc[OHI,'pct_2024'])} in 2024), "
  "but its denominator is not population-based. "
  f"B shows that extreme stays (≈ {pct(tB2.loc[2024,'pct_episodes_outlier'])} of episodes) account for ≈ {pct(tB2.loc[2024,'pct_bed_days_in_outliers'],0)} of bed-days, "
  f"and that an adjusted stay index (IEMA) is stable between years (r = {dec(r_iema)}). Our <b>provisional</b> preference is <b>B</b>. "
  "This is an initial framing only: full cleaning, the complete EDA and the final question are left for C1, after instructor feedback (section 6).")
p("<b>Starting point.</b> We used the course repository (<i>Mxtiilxz/Workshop</i>: source inventory and download script) and, as a methodological reference, "
  "the public repository <i>thenoeyedgirl/proyecto-GRD-Fonasa</i> (another team's regional GRD analysis for 2023-2024). "
  "We adopted its territorial focus as candidate A, tested its assumptions and corrected three of them (section 3.3). Candidate B is our own.")

# ---------------------------------- 1. Candidate A ----------------------------------
p("1. Candidate A · Hospitalisation outside the region of residence", h1)
p("<b>Problem.</b> In Chile, high-complexity care and medical specialists are concentrated in a few regions. Some patients are admitted "
  "to a hospital in another region, with travel costs for families and pressure on receiving centres. Population: inpatient stays "
  "(excluding major ambulatory surgery, CMA) in the public hospitals funded through GRD, 2023-2024, by region of residence.")
p("<b>Documented relevance.</b> A report by the Departamento de Estudios y Desarrollo (July 2023) states that the Metropolitan region concentrates 59.7% "
  "of the country's certified medical specialists (20,846 of 34,944, September 2022). Tarapacá has 0.70 specialists per 1,000 inhabitants against a national 1.76 [4]. "
  "FONASA describes GRD as a payment mechanism for a network of public hospitals (68 in 2023) and contracted private clinics [3]. Policy link: MINSAL's "
  "National Health Strategy for the 2030 Health Objectives (2022 edition) includes Strategic Axis 7, «Management, quality and innovation» [5]. "
  "We did not verify an indicator or target in that strategy that directly measures inter-regional referral, so we do <i>not</i> equate our indicator with a health target.")
p("<b>Tentative question.</b> What share of inpatient stays of residents of each region takes place in GRD hospitals of another region, where do they go, and for which kinds of case "
  "(GRD weight, elective or emergency admission)? Did it change between 2023 and 2024?")
p("<b>Proposed user and use (our proposal).</b> The Undersecretariat of Healthcare Networks and the sending Health Services could use it to prioritise regional capacity "
  "(beds or specialties) and to size referral agreements and travel support.")
p("<b>Data opportunity.</b> The GRD files record the municipality of residence, the hospital, the GRD, its weight, admission type and origin. Missing: stays in non-GRD facilities "
  "(lower-complexity hospitals, private clinics, armed forces) and the reference population. A population denominator would need DEIS discharges from all facilities or INE population (2024 Census).")

# ---------------------------------- 2. Candidate B ----------------------------------
p("2. Candidate B · Case-mix-adjusted length of stay and extreme stays", h1)
p("<b>Problem.</b> Length of stay (LOS) drives bed use, the critical resource of public hospitals. Comparing crude LOS between hospitals "
  "is unfair because each hospital treats a different case mix; GRD allows that case mix to be adjusted for. Population: inpatient stays in GRD hospitals, 2023-2024.")
p("<b>Documented relevance.</b> Zapata (2018) explains that GRD groups clinically and economically similar episodes and that it allows case-mix-adjusted LOS to be compared. "
  "The author reports a 2014 national norm with a mean LOS of 6.2 days and 6.4% upper outliers over 807,195 discharges [6]. "
  "FONASA (2023) reports that in 2023 it allocated resources through GRD to 68 facilities and that hospital complexity remained high after the pandemic [3]. "
  "Policy link: Axis 7 «Management, quality and innovation» of the 2022 National Strategy [5]. Here too we found no quantitative LOS target that we can cite.")
p("<b>Tentative question.</b> Which hospitals have a systematically longer stay than expected for their case mix (IEMA > 1)? How much of that excess comes from extreme stays? "
  "Is the signal stable between 2023 and 2024?")
p("<b>Proposed user and use (our proposal).</b> FONASA (Financing Models Department) and hospital bed-management teams could use it to target "
  "reviews of prolonged stays and complex discharges in the GRDs and hospitals where excess bed-days concentrate.")
p("<b>Data opportunity.</b> The files contain admission and discharge dates, the GRD (IR 3.0), severity, mortality, discharge type, internal transfers and specialty. Missing: the official LOS norm "
  "per GRD (we use an internal benchmark), bed-waiting time, social reasons for delayed discharge and cost per day.")

# ---------------------------------- 3. Inspection ----------------------------------
p("3. Inspection of real data", h1)
p("3.1 Source, version and unit of observation", h2)
p("<b>Source.</b> FONASA, «Grupos Relacionados por el Diagnóstico (GRD)» dashboard, Data Catalogue tab [1]: GRD_PUBLICO_2023.zip (extracted by FONASA on 04-09-2024) and "
  "GRD_PUBLICO_2024.zip (extracted on 16-05-2025), downloaded on 25-09-2026. The catalogue warns that each file is a «snapshot» of what was coded at extraction time. "
  "Dictionary: «Tablas maestras bases GRD» [2]. For hospital location and complexity we used the current health-facilities file (MINSAL, datos.gob.cl) included in the reference repository [8]. "
  "SHA-256 fingerprints of every file are recorded in the README.")
p("<b>What a row is.</b> One episode coded in GRD, i.e. an inpatient discharge or a major ambulatory surgery (CMA), from one of the GRD-funded hospitals. It is not a patient or a bed-day. "
  "Files are organised by <b>discharge year</b>: every discharge in the 2023 file falls in 2023, while admission may be earlier. Fields used: hospital (DEIS code), municipality and province of residence, "
  "episode type, admission and discharge dates, admission type, origin, discharge type, IR-GRD code (6 digits), weight, severity and mortality (0 to 3). An encrypted patient identifier exists "
  "but was left out of the extract because W1 does not need it.")
rows = [["Discharge year", "Episodes", "Inpatient stays", "CMA", "Hospitals", "Municipalities of residence"]]
for y in (2023, 2024):
    c = cov.loc[y]
    rows.append([y, num(c["episodes"]), num(c["inpatient"]), num(c["ambulatory_surgery_CMA"]), int(c["hospitals"]), int(c["municipalities_of_residence"])])
table(rows, [2.5*cm, 2.4*cm, 2.8*cm, 2*cm, 2*cm, 3.6*cm])
p("Table 1. Coverage by year. Four hospitals join in 2024 (Constitución, Cauquenes, Penco-Lirquén and Padre Las Casas). Comparisons between years use only the 68 common hospitals.", cap)

p("3.2 First quality checks (Five Cs)", h2)
p("We applied an operational reading of the Five Cs (completeness, consistency, conformity, coverage and credibility). If the Class 03 definition differs, the checks are re-labelled but their content stays the same.")
rows = [["C", "Check", "Result"]]
for _, r in qc.iterrows():
    res = r["result"] if pd.isna(r["pct_of_episodes"]) else f"{num(int(r['result']))} ({r['pct_of_episodes']})"
    rows.append([r["C"], r["check"], res])
rows += [["Consistency", "Different schema between years", "2023: UTF-16, CIP_ENCRIPTADO, dates DD-MM-YYYY; 2024: Latin-1, ID_BENEFICIARIO, dates YYYY-MM-DD"],
         ["Consistency", "Region labels in the facilities file", "«De» and «de» mixed; 2 municipalities assigned to 2 regions (Longaví, Tucapel), resolved by mode"]]
table(rows, [2.3*cm, 6.5*cm, 7.4*cm])
p("Table 2. Initial checks on 2,125,400 episodes. Critical fields are almost complete. The relevant problems concern consistency between versions and coverage, not missing data.", cap)

p("3.3 Checking the reference repository", h2)
bullets([
 "<b>Dates.</b> The reference reads dates as DD/MM/YYYY for both years. In the data, 0% of dates match that format: 2023 uses DD-MM-YYYY and 2024 uses YYYY-MM-DD. "
 "Its notebook reports only 211,157 valid stays with a mean of 110.9 days. Recomputing with each year's format gives 1.72 million valid stays with a mean of ≈ 7 days, consistent with the 2014 norm of 6.2 days [6].",
 "<b>SERVICIO_SALUD.</b> The reference uses it as the hospital's location. However, each hospital records a median of 18.5 different health services (up to 30), so the field describes the <i>patient</i>. We locate hospitals through the DEIS code joined to the facilities file.",
 "<b>Non-local by municipality (48.6%) and expected region by modal province.</b> A high-complexity hospital treating patients from other municipalities is expected by network design, and a region assigned by mode is circular. "
 "We use the region of residence derived from the municipality. We also exclude CMA episodes (19.1%), which the reference mixes with inpatient stays."])

p("3.4 Candidate A: first observations", h2)
p("<b>Joins.</b> (1) COD_HOSPITAL → facility code: <b>verified</b>, 72 of 72 hospitals match (58 high and 14 medium complexity). (2) Municipality of residence (text) → region, "
  "through a municipality-region table derived from the facilities file with normalised labels: <b>proposed and tested</b>, 12 episodes (0.0006%) remain without a region. "
  "Matching names do not guarantee the same meaning: the hospital's region comes from the current version of the facilities file, not necessarily the 2023 one.")
fig(F/"figA1_fuera_region.png", 14.2*cm, f"Figure 1. Share of inpatient stays in a GRD hospital of another region, by region of residence (68 common hospitals). Total: {pct(outA[2023])} in 2023 and {pct(outA[2024])} in 2024.")
rows = [["Flow (residence → hospital)", "Inpatient stays 2023+2024"]] + [[r.flow, num(r.episodes_2023_2024)] for r in tA2.itertuples()]
S.append(Paragraph("Table 3. Ten most frequent inter-regional flows.", h3))
table(rows, [8.5*cm, 4.5*cm])
p(f"<b>Interpretation.</b> Leaving the region is uncommon on average (≈ {pct(outA[2024])}), but it is about three to six times more frequent in O'Higgins, Aysén, Los Ríos and Atacama than in the Metropolitan region or Biobío. "
  "The Metropolitan region is the main destination, although flows between neighbouring regions also appear (Ñuble → Biobío, Los Ríos ↔ Los Lagos). Leaving the region rises with complexity: "
  f"it is {pct(q4)} in the highest GRD-weight quartile against {pct(q1)} in the lowest, and {pct(elective)} for elective admissions against {pct(emergency)} for emergency admissions. "
  "The pattern fits referral of complex, elective cases to reference centres. "
  "<b>Limitation.</b> The denominator is inpatient stays in GRD hospitals, not the population. A resident treated outside the GRD network is not observed, so the indicator does not measure access or unmet need. "
  "Flows from the Metropolitan region to Valparaíso or O'Higgins may reflect temporary stays (holidays) rather than referral.")

p("3.5 Candidate B: first observations", h2)
p("<b>Operational definitions (ours).</b> LOS = discharge − admission, in days (inpatient stays only). Upper outlier = LOS > Q3 + 1.5·IQR within the same GRD code. "
  "Expected LOS = mean of the non-outlier episodes of that GRD across all GRD hospitals in 2023-2024. Hospital IEMA = Σ observed LOS / Σ expected LOS (indirect standardisation over non-outliers). "
  "No join is needed. 47 episodes with a GRD code outside the dictionary are excluded.")
rows = [["Year", "N", "Mean", "P25", "P50", "P75", "P90", "P99", "Max", "% outlier", "% bed-days in outliers"]]
for y in (2023, 2024):
    d = tB1.loc[y]; o = tB2.loc[y]
    rows.append([y, num(d["count"]), dec(d["mean"]), int(d["25%"]), int(d["50%"]), int(d["75%"]), int(d["90%"]), int(d["99%"]), int(d["max"]),
                 pct(o["pct_episodes_outlier"]), pct(o["pct_bed_days_in_outliers"])])
table(rows, [1.2*cm, 1.8*cm, 1.2*cm, 1*cm, 1*cm, 1*cm, 1*cm, 1*cm, 1.1*cm, 1.7*cm, 3.2*cm])
p("Table 4. Length of stay (days) and upper outliers by discharge year. N = analysable inpatient stays.", cap)
fig(F/"figB1_estancia.png", 14.2*cm, "Figure 2. Distribution of length of stay (inpatient stays 2023-2024). The right tail is long: 2.1% exceed 40 days.")
fig(F/"figB2_iema_2023_2024.png", 9.4*cm, f"Figure 3. IEMA by hospital, 2023 against 2024 (68 common hospitals). The dashed line is y = x. r = {dec(r_iema)}.")
lo, hi = b24.sort_values("IEMA").iloc[0], b24.sort_values("IEMA").iloc[-1]
p(f"<b>Interpretation.</b> Median LOS is 3 days and the mean ≈ 7. Extreme stays (≈ {pct(tB2.loc[2024,'pct_episodes_outlier'])} of episodes) account for ≈ {pct(tB2.loc[2024,'pct_bed_days_in_outliers'],0)} of bed-days, "
  f"with a mean LOS of ≈ {dec(tB2.loc[2024,'mean_los_outliers'],0)} days against ≈ {dec(tB2.loc[2024,'mean_los_non_outliers'],1)} for the rest. The outlier share is close to the 6.4% of the 2014 norm [6], which is consistent with our operational definition as a first approximation (it does not validate it on its own). "
  f"In 2024 IEMA ranges from {dec(lo.IEMA)} ({lo.HOSPITAL}) to {dec(hi.IEMA)} ({hi.HOSPITAL}), and the ranking is stable between years (r = {dec(r_iema)}). "
  "Crude hospital LOS correlates with mean GRD weight (r ≈ 0.53), whereas IEMA hardly does (r ≈ −0.07), which indicates that the case-mix adjustment removes the complexity effect, as intended. "
  "<b>Limitation.</b> The benchmark is internal, not an official norm. 33 of 790 GRDs have fewer than 30 cases, so their outlier threshold is unstable. A high IEMA may come from complexity not captured by GRD (national referral institutes), internal transfers or waiting for a social discharge, "
  "and the files cannot separate these causes.")

# ---------------------------------- 4. Seven steps ----------------------------------
p("4. Initial framing with the seven steps (Class 03)", h1)
rows = [["Step", "Candidate A", "Candidate B"],
 ["Decision", "Where to strengthen regional capacity and how to size referral", "Which hospitals and GRDs to target for stay management"],
 ["Success criteria", "A measurable, stable regional gap attributable to complex cases", "Excess bed-days identified and a signal stable between years"],
 ["Business questions", "Who leaves, where to and with which cases", "Who exceeds the expected stay and how much outliers contribute"],
 ["Business process", "Referral: admission → stay in another region → discharge or return", "Admission → stay (with internal transfers) → discharge"],
 ["Entities / events / states", "Patient (residence), hospital (region), episode; event: admission", "Hospital, GRD, episode; states: normal or outlier stay"],
 ["Data representation", "Municipality of residence (text), COD_HOSPITAL, dates, GRD", "Dates, IR-GRD code, severity, discharge type"],
 ["Measurement / gap", "% outside region; <b>gap:</b> no population, no non-GRD hospitals", "IEMA and % bed-days in outliers; <b>gap:</b> no official norm, no causes"]]
table(rows, [3.3*cm, 6.4*cm, 6.4*cm])

# ---------------------------------- 5. Comparison ----------------------------------
p("5. Comparison of the alternatives", h1)
rows = [["Dimension", "Candidate A · Outside region", "Candidate B · Adjusted stay"],
 ["Relevance supported by sources", "Specialist concentration in the Metropolitan region [4]; GRD network [3]; Axis 7 [5] without a verifiable target", "GRD used to compare adjusted LOS; 2014 norm [6]; FONASA [3]; Axis 7 [5]"],
 ["Fit between question and inspected data", "Observes leaving the region <i>within</i> the GRD network; cannot observe population or external providers", "Directly observes LOS and case mix for every episode in the GRD network"],
 ["Analytical opportunity for C1", "Origin-destination matrix by GRD or specialty; relation to regional capacity", "Breakdown of excess by GRD, specialty, discharge type and transfers; monthly trend"],
 ["Main limitation and its consequence", "Non-population denominator: cannot speak about access or equity", "Internal benchmark: IEMA is relative to the network, not absolute efficiency"],
 ["Feasible scope and future ML / dashboard potential", "Possible ML task: classify the probability of an out-of-region admission. Dashboard for Health Services: flows and % by region. To check: which variables are known at admission", "Possible ML task: predict prolonged stay (outlier) from admission variables. Dashboard for bed management: IEMA with intervals and % outlier bed-days. To check: information leakage, as the GRD is assigned at discharge"]]
table(rows, [3.4*cm, 6.3*cm, 6.4*cm])
p("<b>Provisional preference: B.</b> Its data answer the question without external sources, the signal is stable (r ≈ 0.93) and it leads naturally into C1: "
  "the C1 EDA can characterise prolonged stays, and later stages could consider predicting them and a bed-management dashboard. A remains relevant, but its interpretation depends on a denominator we do not have. "
  "<b>What could change the decision:</b> (i) if territorial equity is considered a priority for the observatory and DEIS discharges from all facilities or INE population can be added within the C1 scope; "
  "(ii) if an IEMA with an internal benchmark is judged insufficient without the official MINSAL/FONASA norm.")

p("6. Questions for feedback", h1)
bullets([
 "For C1, is an expected LOS computed internally (mean of non-outliers per GRD within the network) acceptable, or should we look for the official LOS norm per GRD? Do you know of a public source?",
 "In B, should IEMA be stratified by facility complexity, or should national referral institutes (e.g. Asenjo Neurosurgery, Traumatology Institute) be excluded, since GRD may not capture their case mix?",
 "For a future prediction of prolonged stay, which variables do you consider legitimately available at admission? The main diagnosis and the GRD are coded at discharge.",
 "In A, does the C1 scope justify adding DEIS discharges to correct the denominator, or is it better to narrow the question to «referral within the GRD network»?",
 "Does our reading of the Five Cs match the Class 03 definition?"])

p("7. Project continuity (ML and dashboard)", h1)
p("<b>A.</b> Possible task: binary classification (out-of-region admission yes/no) to anticipate referral demand by region and case type. Data: age, sex, municipality, admission type, origin and "
  "main diagnosis. To check: whether the signal is dominated by region of residence (in which case a descriptive table is enough and ML adds no value) and class imbalance (≈ 2%). "
  "Dashboard: Health Services and Undersecretariat of Healthcare Networks; origin-destination matrix, % outside region by region and GRD, monthly trend.")
p("<b>B.</b> Possible task: classify at admission the risk of a prolonged (outlier) stay, to prioritise discharge management. Data: age, admission type, origin, admitting unit, "
  "specialty and insurance category. To check: information leakage (GRD, severity and diagnosis are known at discharge) and stability between years. As required at this stage, no algorithm, validation protocol or accuracy is proposed. "
  "Dashboard: hospital directors and bed managers; IEMA with intervals, % bed-days in outliers by GRD and unit, and comparison with hospitals of similar complexity.")

# ---------------------------------- Process record ----------------------------------
S.append(PageBreak())
p("Process record", h1)
p("Decisions and checks", h2)
rows = [["Date / stage", "Decision", "Alternative", "Reason and evidence", "Check and result", "Location"],
 ["24-09 Sources", "Download GRD from the Data Catalogue of the FONASA dashboard", "bases-grd path in the course script", "The bases-grd page redirects to a 404; the catalogue publishes URLs and extraction dates", "URLs read from the catalogue; ZIPs intact; SHA-256 recorded", "README; report §3.1"],
 ["25-09 Extraction", "Extract 23 columns + 4 derived; drop patient ID and date of birth", "Work with all 129 fields", "Limited memory (3 GB) and personal-data minimisation", "Extract rows = original rows (1,039,587 / 1,085,813)", "analysis/01_extraer_grd.py"],
 ["25-09 Extraction", "Parse each date column with its own format", "One format per file", "The first extraction left age empty in 2023 (birth YYYY-MM-DD, admission DD-MM-YYYY)", "Fixed and re-run: age missing in 0.001%", "01_extraer_grd.py; notebook §2"],
 ["25-09 Reference", "Do not use SERVICIO_SALUD as hospital location", "Use it as the reference repo does", "Up to 30 different services per hospital", "Join by DEIS code: 72/72", "notebook §3-4"],
 ["25-09 A", "Region of residence from municipality", "Modal region per province (reference)", "Avoids circularity; uses a patient attribute", "No region: 12 episodes", "notebook §4"],
 ["25-09 A and B", "Exclude CMA; compare years on 68 common hospitals", "All episodes and hospitals", "CMA has no stay; 4 hospitals join in 2024", "Table 1 and coverage", "notebook §1"],
 ["25-09 B", "Internal benchmark per GRD and Q3+1.5·IQR outlier", "Official MINSAL norm", "No downloadable public norm found", "% outlier 6.3-6.7% vs 6.4% in 2014 norm [6]", "notebook §5"],
 ["25-09 Language", "Translate all files into English", "Keep Spanish text", "The course is taught in English", "Notebook re-run; figures regenerated with English labels", "all files"]]
table(rows, [1.9*cm, 3.1*cm, 2.3*cm, 3.4*cm, 3.2*cm, 2.4*cm])

p("Instructor feedback and response", h2)
p("[COMPLETE] Record the feedback received in the guided session of 24-09-2026 (what was advised, whether it was accepted, adapted or rejected, and why). "
  "If there was none or it is pending: feedback is pending and the provisional decision is to develop B in C1.")

p("Individual contributions", h2)
table([["Member", "Concrete contribution", "Evidence"], ["[COMPLETE]", "[COMPLETE: actual contribution, not the planned one]", "[file / section]"], ["[COMPLETE]", "[COMPLETE]", "[file / section]"]], [3.5*cm, 8.6*cm, 4*cm])

p("AI use and verification", h2)
rows = [["Tool and purpose", "Relevant excerpt", "Accepted / modified / rejected", "Verification"],
 ["Claude (Anthropic), Cowork mode: review both repositories, locate official URLs, draft the extraction script, the notebook and this report",
  "Prompt: «use that repo and follow instructions for W1 [...] using 2023 and 2024 Fonasa GRD data [...] create the second one in case of missing»",
  "The reference's territorial focus (A) was accepted; B was proposed by the AI. Three assumptions of the reference were rejected (section 3.3)",
  "Every figure in the report is read from data/processed/, generated by the executed notebook; URLs were checked against the FONASA catalogue"],
 ["Claude: literature search", "Sources [3]-[6] read in their web or PDF version", "Articles whose authors could not be verified (blocked access or reCAPTCHA) were discarded", "Only sources with verified author/institution, title, date and link are cited"],
 ["Claude: error found", "First extraction with empty 2023 age", "Fixed (date parser per column)", "Re-run and missing-value check"],
 ["Claude: translation", "«Translate every file to English, this class is English only»", "All text translated; file names kept", "Notebook re-executed; numbers unchanged"],
 ["[COMPLETE by the team]", "[what you reviewed]", "[what you changed]", "[how you checked it]"]]
table(rows, [3.9*cm, 4.3*cm, 4*cm, 3.9*cm])

p("Individual reflection", h2)
p("[COMPLETE for each member: one contribution, one learning gain and one unresolved uncertainty.]")

# ---------------------------------- References ----------------------------------
p("References", h1)
refs = [
 "[1] FONASA, Departamento Modelos de Financiamiento and Departamento Estudios y Estadística. «Grupos Relacionados por el Diagnóstico (GRD)», Tableau Public dashboard, Data Catalogue tab (data to December 2024). "
 "https://public.tableau.com/views/PropuestaTableroGRD/PropuestaTableroGRD. Files: https://www.fonasa.cl/assets/datos-abiertos/Financiamiento_y_Gasto_en_Salud/GRD_PUBLICO_2023.zip (extracted 04-09-2024) and "
 "https://adjuntos.fonasa.gob.cl/assets/datos-abiertos/Financiamiento_y_Gasto_en_Salud/GRD_PUBLICO_2024.zip (extracted 16-05-2025). Retrieved 25-09-2026.",
 "[2] FONASA. «Tablas maestras bases GRD» (xlsx). https://www.fonasa.cl/assets/datos-abiertos/Financiamiento_y_Gasto_en_Salud/Tablas%20maestras%20bases%20GRD%20.xlsx. Retrieved 25-09-2026.",
 "[3] FONASA (October 2023). Boletín Analysis, Edición Especial GRD. https://adjuntos.fonasa.gob.cl/assets/datos-abiertos/Biblioteca/Analysis_octubre2023_Fonasa.pdf",
 "[4] Departamento de Estudios y Desarrollo (July 2023). Caracterización de las especialidades médicas en Chile en 2022. https://www.superdesalud.gob.cl/documentacion/666/articles-26547_recurso_1.pdf",
 "[5] Ministerio de Salud de Chile (2022). Estrategia Nacional de Salud para los Objetivos Sanitarios al 2030. https://www.minsal.cl/wp-content/uploads/2022/03/Estrategia-Nacional-de-Salud-2022-MINSAL-V8.pdf",
 "[6] Zapata, M. (2018). Importancia del sistema GRD para alcanzar la eficiencia hospitalaria. Revista Médica Clínica Las Condes, 29(3), 347-352. https://doi.org/10.1016/j.rmclc.2018.04.010",
 "[7] Course IIB423T-1. Repository Mxtiilxz/Workshop (commit af9d0d7): W1 brief, FUENTES inventory and download script. https://github.com/Mxtiilxz/Workshop",
 "[8] Garrido, L. and Ramírez, C. Repository thenoeyedgirl/proyecto-GRD-Fonasa (commit e87ab54): notebook Analisis_Grupo_5_v2.ipynb and BDDs/establecimientos.csv (MINSAL, current health facilities, "
 "https://datos.gob.cl/dataset/establecimientos-de-salud-vigentes; the file's version date is not documented in the repository). https://github.com/thenoeyedgirl/proyecto-GRD-Fonasa"]
for r in refs: p(r, small)

def footer(c, d):
    c.saveState(); c.setFont("DV", 7); c.setFillColor(INK2)
    c.drawString(2*cm, 1.2*cm, "Business Intelligence | IIB423T-1 | W1 | GROUP_XX"); c.drawRightString(A4[0]-2*cm, 1.2*cm, str(d.page)); c.restoreState()
out = R/"report/GROUP_XX_W1_Report.pdf"
doc = SimpleDocTemplate(str(out), pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=1.8*cm, bottomMargin=1.8*cm,
                        title="GROUP_XX_W1_Report", author="GROUP_XX")
doc.build(S, onFirstPage=footer, onLaterPages=footer)
print("ok", out)
