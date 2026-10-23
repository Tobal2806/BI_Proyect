# GROUP_01_W2 · From exploratory analysis to credible validation

Business Intelligence IIB423T-1 · Universidad del Desarrollo · Instructor: Tomás Fontecilla Correa

| | |
|---|---|
| Group ID | GROUP_01 |
| Members | Matías López, Cristóbal Ramírez |
| Submission | Workshop 2, due 29-10-2026 |
| Project line | Case-mix-adjusted length of stay (IEMA) and extreme stays in FONASA GRD hospitals, 2023-2024 (continued from W1 and C1) |
| Repository | `https://github.com/Tobal2806/BI_Proyect` · tag `w2-submission` |

Start with `notebooks/W2_project.ipynb`. It is the W2 deliverable: one executable notebook with continuity and feedback, data dictionary and validation checks, revised EDA, sampling assessment, leakage audit, the train/validation/test split, revised conclusions, the management summary and the AI-use disclosure.

## Package contents

```
GROUP_01_W2/
  README.md                          this file
  requirements.txt                   Python packages and versions used
  notebooks/W2_project.ipynb         the W2 notebook (executed, outputs saved)
  data/processed/w2_*.csv            tables written by the notebook (w2_00 to w2_12)
  data/figures/w2_fig*.png           figures written by the notebook (four figures)
```

Key outputs: `w2_02_validation_checks.csv` (21 checks with actions), `w2_03_row_flow.csv` and `w2_03b_exclusions_by_reason.csv` (row counts before and after every exclusion), `w2_07_split_counts.csv` and `w2_08_split_verification.csv` (split and overlap checks), `w2_09_train_benchmark_by_grd.csv` and `w2_10_train_fitted_parameters.csv` (parameters learned from training rows only), `w2_12_revised_conclusions.csv`.

## Data provenance

W2 adds no new source. It reads the C1 inputs in place, which are byte-identical to those of W1. The notebook verifies their SHA-256 against the C1 README and stops if any file differs.

- `../GROUP_01_C1/data/extracted/grd_2023_extracto.csv.gz` and `grd_2024_extracto.csv.gz`: reduced extracts of FONASA's public GRD files `GRD_PUBLICO_2023.zip` (extracted by FONASA 04-09-2024) and `GRD_PUBLICO_2024.zip` (extracted 16-05-2025). Both were downloaded on 25-09-2026 from the Data Catalogue tab of the FONASA GRD dashboard (https://public.tableau.com/views/PropuestaTableroGRD/PropuestaTableroGRD).
  - The extracts were produced by `GROUP_01_W1/analysis/01_extraer_grd.py` (23 original columns plus 4 derived; no rows filtered).
  - The encrypted patient identifier and the date of birth were dropped for data minimisation.
  - The original FONASA files are not in the repository because of their size. They can be downloaded again from the URLs in the C1 README.
- `../GROUP_01_C1/data/reference/Tablas_maestras_bases_GRD.xlsx`: FONASA GRD dictionary.
- `../GROUP_01_C1/data/reference/establecimientos_datosgobcl.csv`: MINSAL health facilities file (datos.gob.cl, current version).
- `../GROUP_01_C1/data/processed/c1_07_benchmark_by_grd.csv` and `c1_09_network_summary.csv`: C1 outputs, used to show that W2 reproduces the C1 benchmark and to compare with C1's statements.

All files are public, aggregated administrative data without personal identifiers. No confidential records are published.

## How to run

1. Clone the repository. The notebook needs the folder `GROUP_01_C1/` next to `GROUP_01_W2/`, as in the repository.
2. Install the packages: `pip install -r GROUP_01_W2/requirements.txt` (Python 3.12 or later).
3. From `GROUP_01_W2/notebooks/`, either:
   - open `W2_project.ipynb`, restart the kernel and run all cells, or
   - run `jupyter nbconvert --to notebook --execute --inplace W2_project.ipynb`.

   It takes about 2 minutes and about 3 GB of RAM.
4. The notebook rewrites `data/processed/` and `data/figures/` inside `GROUP_01_W2/`. It never writes to the W1 or C1 folders.

Randomness is used only for the 25% subsamples in section 4, with `SEED = 2026`. The train/validation/test split is defined by admission dates and is deterministic.

## Software

Executed on 23-10-2026 with Python 3.13.16, pandas 3.0.5, numpy 2.5.3, matplotlib 3.11.2, openpyxl 3.1.5, nbconvert 7.17.2, nbformat 5.11.1 and ipykernel 7.4.0. C1 ran on pandas 3.0.2; the notebook checks that its benchmark is identical to C1's.

## Execution status and known limitations

- The notebook runs top to bottom without errors; the saved outputs match the code and data.
- Repeated patients across subsets cannot be checked, because the extract has no patient identifier (leakage risk L5).
- The 2024 period was explored descriptively in W1 and C1, so the test subset is not untouched. No parameter, variable choice or threshold was learned from it (notebook section 6.2).
