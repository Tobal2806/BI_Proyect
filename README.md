# Business Intelligence IIB423T-1 · GROUP_01 · Final study (C3)

Universidad del Desarrollo · Instructor: Tomás Fontecilla Correa

| | |
|---|---|
| Group ID | GROUP_01 |
| Members | Matías López, Cristóbal Ramírez |
| Assessed version | tag `c3-submission` in `https://github.com/Tobal2806/BI_Proyect` (full SHA given in the Canvas submission) |
| Question | Using only what is known on the day of admission to a FONASA public hospital, can we flag the stays likely to become extreme (longer than the cut-off of their GRD) well enough for bed managers to start discharge planning early, and does this beat flagging every emergency admission? |
| Central message | On 2024 admissions, a simple model flags a third as many admissions as the emergency rule and catches half as many extreme stays, with more of its flags right (10.6% against 6.9%). It can focus discharge planning as a prioritisation aid, depending on each team's review capacity; it does not work for scheduled admissions and must not decide care for individual patients. |

No installation, setup or data download is needed to review the study: every notebook is saved executed, with its tables and figures.

## Reading order

1. **`GROUP_01_C3/notebooks/C3_study.ipynb`** is the final, integrated pipeline: data card, quality summary, preparation and its effect on the records, EDA, chronological split, train-only labels, comparison of 6 model configurations with the reference rule, one test run, the final views, conclusions and limits, and the decision record (feedback use, W3 design selection, contributions, AI use).
2. **`GROUP_01_C3/presentation/GROUP_01_C3_Slides.pptx`** is the presentation: an external part for hospital bed managers, then an internal part for the reviewer.
3. The stage folders are the development record, in order. Each one is kept as submitted; the C3 notebook says what each contributed and what was later corrected:

| Order | Folder | Stage | Read | Submitted | Tag | Result |
|---|---|---|---|---|---|---|
| 1 | `GROUP_01_W1/` | W1 · Two candidate questions and a first data audit | `report/GROUP_01_Report.pdf`, `analysis/02_inspeccion_GRD_W1.ipynb` | 25-09-2026 | `w1-submission` | 97/100 |
| 2 | `GROUP_01_C1/` | C1 · Profiling, preparation, length-of-stay benchmark, sensitivity and EDA | `README.md`, `analysis/02_C1_profiling_preparation_eda.ipynb` | 29-09-2026 | `c1-submission` | 94/100 |
| 3 | `GROUP_01_W2/` | W2 · Validation checks, revised EDA, leakage audit, train/validation/test split | `README.md`, `notebooks/W2_project.ipynb` | 29-10-2026 | `w2-submission` | 100/100 |
| 4 | `GROUP_01_C2/` | C2 · First model: logistic regression against the emergency-admission rule | `notebooks/C2_model.ipynb`, `brief/GROUP_01_C2_Brief.pdf` | 08-11-2026 | `c2-submission` | 93.75/100 |
| 5 | `GROUP_01_W3/` | W3 · Visual system (rules R1-R8) for the C2 results | `README.md`, `report/GROUP_01_W3_Report.pdf`, `notebooks/W3_visual_system.ipynb` | 21-11-2026 | `w3-submission` | pending |
| 6 | `GROUP_01_C3/` | C3 · Integrated study, model comparison, final views and presentation | `notebooks/C3_study.ipynb`, `presentation/` | 24-11-2026 | `c3-submission` | — |

## Pipeline

```
FONASA GRD files 2023 + 2024 (2,125,400 episodes)  →  reduction script (C1 analysis/01_extraer_grd.py; SHA-256 checked)
  →  quality checks and exclusions (1,719,718 valid inpatient stays)  →  EDA
  →  chronological split by admission date (train Jan-Jun 2023 · validation Jul-Sep 2023 · test Jan-Sep 2024)
  →  extreme-stay cut-off per GRD fitted on train only (783 codes, frozen)  →  admission-time inputs only
  →  6 candidate models compared on validation, plus the emergency rule  →  one test run of the chosen model
  →  final views drawn with GROUP_01_W3/notebooks/w3_style.py  →  conclusions, limits and presentation
```

## File roles (C3)

| File | Role |
|---|---|
| `GROUP_01_C3/notebooks/C3_study.ipynb` | Integrated pipeline, executed with saved outputs |
| `GROUP_01_W3/notebooks/w3_style.py` | Shared visual rules (colours, shapes, names, scales, text, layout), imported by every final view |
| `GROUP_01_C3/outputs/figures/c3_fig0` to `c3_fig4` | Final views written by the C3 notebook |
| `GROUP_01_C3/outputs/figures/slides/` | Presentation versions of the final views (same values and rules, larger text), written by the C3 notebook, section 7.5 |
| `GROUP_01_C3/outputs/tables/c3_01` to `c3_04` | Saved results: candidate comparison on validation, test metrics, test results by admission type, bed-days held by extreme stays |
| `GROUP_01_C3/presentation/GROUP_01_C3_Slides.pptx` | Presentation (editable): Part 1 for bed managers, Part 2 for the reviewer, appendix with every number's source and the detailed final views; speaker notes hold each slide's checkpoints |
| `GROUP_01_C3/requirements.txt` | Software versions used to execute C3 |

## Software

Python 3.13.18 with pandas 3.0.5, numpy 2.5.3, scikit-learn 1.9.1, matplotlib 3.11.2 and Jupyter (nbconvert); openpyxl reads the FONASA dictionary. Earlier stages list their versions in their own `requirements.txt`.

## Data (not included)

The C3 rules exclude data files, so the repository holds no raw data, extracts or reference datasets; the notebooks show compact summaries only. The sources are:

- FONASA public GRD files, from the *Catálogo de Datos* tab of https://public.tableau.com/views/PropuestaTableroGRD/PropuestaTableroGRD:
  - https://www.fonasa.cl/assets/datos-abiertos/Financiamiento_y_Gasto_en_Salud/GRD_PUBLICO_2023.zip (extracted by FONASA 04-09-2024)
  - https://adjuntos.fonasa.gob.cl/assets/datos-abiertos/Financiamiento_y_Gasto_en_Salud/GRD_PUBLICO_2024.zip (extracted by FONASA 16-05-2025)
- FONASA dictionary *Tablas maestras bases GRD*: https://www.fonasa.cl/assets/datos-abiertos/Financiamiento_y_Gasto_en_Salud/Tablas%20maestras%20bases%20GRD%20.xlsx
- MINSAL health facilities: https://datos.gob.cl/dataset/establecimientos-de-salud-vigentes

To re-run, rebuild the reduced extracts with `GROUP_01_C1/analysis/01_extraer_grd.py` and place them in `GROUP_01_C1/data/extracted/`, with the two reference files in `GROUP_01_C1/data/reference/`; these folders are ignored by Git. The notebooks check the files against these SHA-256 values:

| File | SHA-256 |
|---|---|
| grd_2023_extracto.csv.gz | dbe960f33b21837589bda4c989fcada57ff70de8e572714fea3f0574947d3878 |
| grd_2024_extracto.csv.gz | 7bb1f18b0a9817a578bc2c786f151c28c25965af20cf1438090832e3420ae3a0 |
| Tablas_maestras_bases_GRD.xlsx | 29da22ac27a79a5f3d62e0b97fcff79dcaf1f19908dcf517a7e6bb88f216bd8a |
| establecimientos_datosgobcl.csv | 21c596531528078107b01388716f93d98516f7a9da1817927fd67644b7faa176 |

Earlier stage notebooks still name these files in their saved outputs, because they were executed when the data were in the repository; their results remain readable without them.

## Feedback received and how it was used

- **W1 (97/100):** the deduction was the missing README entry point. The instructor also asked to close clearly the definition of the stay benchmark and its limits. Both were addressed in C1.
- **C1 (94/100):** the README was named incorrectly; paths and packaging should be reviewed; methodology and traceability were judged fully complete.
  - The C1 README is stored in this repository as `GROUP_01_C1/README.md`.
  - The W2 notebook checks paths and packaging.
  - Informal feedback also asked to state the hypotheses before presenting results and data, which W2 does.
- **W2 (100/100):** exclude fields not available at admission; freeze extreme-stay thresholds inside training. Both applied in C2 and kept in C3.
- **C2 (93.75/100):** no deductions on documentation; deductions on presentation clarity and on connecting the data to its purpose for the audience.
  - Also asked to report how many models were tried before choosing the final one, and to compare at least 3 to 5 candidate models at each modelling stage. C3 compares 6 configurations from 3 families (C3 notebook section 5) and keeps the C2 model.
  - The C3 presentation opens with the decision of its audience, bed managers, and explains why the findings matter to them.
- **W3:** no feedback received at the time of C3.

## Contributions and AI use

See `GROUP_01_C3/notebooks/C3_study.ipynb`, sections 9.4 and 9.5, and the AI-use sections of each stage.
