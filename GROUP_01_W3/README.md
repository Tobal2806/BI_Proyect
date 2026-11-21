# GROUP_01_W3 · From separate charts to a visual system

Business Intelligence IIB423T-1 · Universidad del Desarrollo · Instructor: Tomás Fontecilla Correa

| | |
|---|---|
| Group ID | GROUP_01 |
| Members | Matías López, Cristóbal Ramírez |
| Submission | Workshop 3 |
| Project line | Extreme stays in FONASA GRD hospitals, 2023-2024: visual system for the C2 results (continued from W1, C1, W2 and C2) |
| Repository | `https://github.com/Tobal2806/BI_Proyect` · tag `w3-submission` |

Start with `report/GROUP_01_W3_Report.pdf` (the same document is editable in `report/GROUP_01_W3_Report.docx`). It covers the audience and purpose, the visual system guide, the three views with their before-and-after pairs, and the limits of each final view.

## Package contents

```
GROUP_01_W3/
  README.md                                   this file
  requirements.txt                            Python packages and versions used
  report/GROUP_01_W3_Report.docx              the W3 document (editable)
  report/GROUP_01_W3_Report.pdf               the same document as PDF
  notebooks/W3_visual_system.ipynb            draws every figure from the C2 tables and checks the values (executed, outputs saved)
  notebooks/w3_style.py                       the visual system rules R1-R8 as code, imported by every final view
  data/figures/w3_fig1_after_rules_compared.png
  data/figures/w3_fig2_after_threshold_tradeoff.png
  data/figures/w3_fig3_before_c2_table.png    the C2 admission-type table as printed (earlier version of view 3)
  data/figures/w3_fig3_after_admission_type.png
  data/processed/w3_00_inputs.csv             C2 files read, with SHA-256
  data/processed/w3_01_value_checks.csv       17 checks: every value shown agrees with C2
  data/processed/w3_02_values_shown.csv       every number printed in the final views
```

The earlier versions of views 1 and 2 are the C2 figures `GROUP_01_C2/data/figures/c2_fig2_test_confusion_matrices.png` and `c2_fig1_validation_threshold.png`, used unchanged. The earlier version of view 3 is the table the C2 notebook printed in section 6 (`c2_07`), reproduced as printed.

## Data

W3 adds no data and trains no model. It reads only the C2 outputs in `../GROUP_01_C2/data/processed/` (`c2_03`, `c2_04`, `c2_05`, `c2_07`, `c2_08`) and the two C2 figures. Their checksums are written to `w3_00_inputs.csv`. The C2 outputs come from FONASA's public GRD files 2023-2024; provenance is in `GROUP_01_C1/README.md` and `GROUP_01_W2/README.md`.

## How to run

1. Clone the repository. The notebook needs `GROUP_01_C2/` next to `GROUP_01_W3/`, as in the repository.
2. Install the packages: `pip install -r GROUP_01_W3/requirements.txt`.
3. From `GROUP_01_W3/notebooks/`, either open `W3_visual_system.ipynb`, restart the kernel and run all cells, or run `jupyter nbconvert --to notebook --execute --inplace W3_visual_system.ipynb`. It takes a few seconds.
4. The notebook rewrites `data/figures/` and `data/processed/` inside `GROUP_01_W3/` only.

The figures use the Inter font when it is installed and fall back to Segoe UI or DejaVu Sans, so a re-run on another computer can change the letter shapes but not the values or the layout rules.

## Software

Executed on 21-11-2026 on Linux with Python 3.13.18, pandas 3.0.5, numpy 2.5.3 and matplotlib 3.11.2.
