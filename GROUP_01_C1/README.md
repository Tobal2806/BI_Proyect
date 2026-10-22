# GROUP_01_C1 · Case-mix-adjusted length of stay in FONASA GRD hospitals, 2023-2024

Business Intelligence IIB423T-1 · Universidad del Desarrollo · Instructor: Tomás Fontecilla Correa

| | |
|---|---|
| Group ID | GROUP_01 |
| Members | Matías López, Cristóbal Ramírez |
| Submission | 29-09-2026, version 1.0 |
| Selected line | Candidate B from W1: case-mix-adjusted length of stay and extreme stays |

Start with `report/GROUP_01_C1_Report.pdf`. It is self-contained and explains the whole investigation. The files below support verification and reproduction.

## Package contents and roles

```
GROUP_01_C1/
  README.md                         this file (entry point)
  requirements.txt                  Python dependencies and versions used
  report/GROUP_01_C1_Report.pdf     report (mandatory, self-contained, includes Process record)
  report/GROUP_01_C1_Report.docx    editable source of the report
  presentation/GROUP_01_C1_Slides.pdf   slides (mandatory)
  presentation/GROUP_01_C1_Slides.pptx  editable source of the slides
  analysis/01_extraer_grd.py        builds the reduced inputs from the official FONASA files (unchanged from W1)
  analysis/02_C1_profiling_preparation_eda.ipynb   profiling, preparation, benchmark, sensitivity, EDA, Five Cs (executed, outputs saved)
  data/extracted/                   EXTRACTED INPUTS (uncleaned, never modified)
    grd_2023_extracto.csv.gz        1,039,587 rows, 26 columns
    grd_2024_extracto.csv.gz        1,085,813 rows, 26 columns
  data/reference/                   REFERENCE INPUTS (unchanged)
    Tablas_maestras_bases_GRD.xlsx  FONASA GRD dictionary (hospitals, IR-GRD codes, severity)
    establecimientos_datosgobcl.csv MINSAL health facilities, current version (datos.gob.cl)
  data/processed/                   PROCESSED OUTPUTS written by the notebook (c1_00 to c1_18)
  data/figures/                     FIGURES written by the notebook (c1_fig1 to c1_fig7)
```

Key processed tables: `c1_07_benchmark_by_grd.csv` (cut-off, expected stay and level per GRD code), `c1_10_hospital_kpis.csv` (hospital-year IEMA with intervals and extreme-stay KPIs), `c1_12_sensitivity.csv`, `c1_18_five_cs.csv`. `c1_01` to `c1_06` hold the profiling, duplicate, validity, consistency and join checks.

## Order to open and run

All paths are project-relative. Run from the folder named in each step.

1. (Only to rebuild the extracts; not needed to verify the results.) From `analysis/`:
   `python 01_extraer_grd.py <path>/GRD_PUBLICO_2023.zip 2023 ../data/extracted/grd_2023_extracto.csv` then `gzip` the output; same for 2024.
2. From `analysis/`: open `02_C1_profiling_preparation_eda.ipynb`, restart the kernel and run all cells top to bottom (about 5 minutes and 1.5 GB of RAM), or run
   `jupyter nbconvert --to notebook --execute --inplace 02_C1_profiling_preparation_eda.ipynb`.
3. The report and slides were drafted from the notebook outputs (`data/processed/`, `data/figures/`) and then edited manually in Word and PowerPoint. Their editable sources are `report/GROUP_01_C1_Report.docx` and `presentation/GROUP_01_C1_Slides.pptx`; the PDFs are exports of those files.

## Software

Python 3.12.3 with pandas 3.0.2, numpy 2.4.4, matplotlib 3.10.8, openpyxl 3.1.5, nbconvert 7.17.1. Install with `pip install -r requirements.txt`. Report and slides: Microsoft Word and PowerPoint (or any editor that opens .docx and .pptx). No credentials or connectors are needed.

## Sources, versions and how the reduced inputs were obtained

- FONASA GRD public files, from the "Catálogo de Datos" (Data Catalogue) tab of the FONASA dashboard https://public.tableau.com/views/PropuestaTableroGRD/PropuestaTableroGRD (the fonasa.cl bases-grd page returns a 404):
  - https://www.fonasa.cl/assets/datos-abiertos/Financiamiento_y_Gasto_en_Salud/GRD_PUBLICO_2023.zip (extracted by FONASA 04-09-2024)
  - https://adjuntos.fonasa.gob.cl/assets/datos-abiertos/Financiamiento_y_Gasto_en_Salud/GRD_PUBLICO_2024.zip (extracted by FONASA 16-05-2025)
  - Downloaded manually on 25-09-2026 (automatic download failed from our environments). The originals are omitted for size; they are kept locally by the team.
- Formats differ by year: 2023 is UTF-16 with admission/discharge dates DD-MM-YYYY; 2024 is Latin-1 with YYYY-MM-DD; GRD weight uses a decimal comma in both. The extraction script detects the encoding and the notebook parses each year with its own format.
- Reduction (`01_extraer_grd.py`): keeps 23 original columns, adds age in years, number of diagnoses, number of procedures and file year; no rows are filtered and no values are cleaned; drops the encrypted patient identifier and the date of birth (data minimisation).
- FONASA dictionary "Tablas maestras bases GRD": https://www.fonasa.cl/assets/datos-abiertos/Financiamiento_y_Gasto_en_Salud/Tablas%20maestras%20bases%20GRD%20.xlsx (retrieved 25-09-2026).
- MINSAL facilities file: https://datos.gob.cl/dataset/establecimientos-de-salud-vigentes, obtained through repository thenoeyedgirl/proyecto-GRD-Fonasa (commit e87ab54); its version date is not documented.

SHA-256 of the inputs (also in `data/processed/c1_00_input_files.csv`):

| File | SHA-256 |
|---|---|
| grd_2023_extracto.csv.gz | dbe960f33b21837589bda4c989fcada57ff70de8e572714fea3f0574947d3878 |
| grd_2024_extracto.csv.gz | 7bb1f18b0a9817a578bc2c786f151c28c25965af20cf1438090832e3420ae3a0 |
| Tablas_maestras_bases_GRD.xlsx | 29da22ac27a79a5f3d62e0b97fcff79dcaf1f19908dcf517a7e6bb88f216bd8a |
| establecimientos_datosgobcl.csv | 21c596531528078107b01388716f93d98516f7a9da1817927fd67644b7faa176 |

## Transformations from inputs to results (summary)

Inpatient stays only (CMA excluded) → valid dates, GRD code in the dictionary and numeric weight → GRD stratum benchmarkable. 1,719,815 inpatient stays become 1,719,702 analysed stays. Exact duplicate rows (0.14%) and same-day stays are retained, for the reasons given in the report (section 3). Exclusions are flags in the notebook; no input file is overwritten. The benchmark, sensitivity variants and KPIs are defined in report section 4 and notebook sections 4-5.

## Execution status and known issues

- The notebook was executed top to bottom on 29-09-2026 with no errors; saved outputs match the submitted code and data.
- The report and slides are based on those outputs and were edited manually afterwards.
- No unresolved execution issue. Known data limitations are listed in report section 8.
- W1 package: GROUP_01_W1 (submitted separately); C1 reuses its extracts and extraction script unchanged.
