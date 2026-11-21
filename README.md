# Business Intelligence IIB423T-1 · GROUP_01

Universidad del Desarrollo · Instructor: Tomás Fontecilla Correa · Members: Matías López, Cristóbal Ramírez

Line of inquiry: case-mix-adjusted length of stay and extreme stays in the public hospitals funded through GRD (FONASA public files, discharges 2023-2024).

Each stage is a separate package folder. W1 and C1 are kept exactly as submitted, and tags mark each submission.

| Folder | Stage | Submitted | Tag | Result |
|---|---|---|---|---|
| `GROUP_01_W1/` | W1 · Discovering questions worth investigating (candidates A and B) | 25-09-2026 | `w1-submission` | 97/100 |
| `GROUP_01_C1/` | C1 · Profiling, preparation, closed benchmark, sensitivity and EDA of candidate B | 29-09-2026 | `c1-submission` | 94/100 |
| `GROUP_01_W2/` | W2 · Validation checks, revised EDA, sampling, leakage audit and train/validation/test split | 29-10-2026 | `w2-submission` | 100/100 |
| `GROUP_01_C2/` | C2 · First model: extreme-stay classification, logistic regression vs emergency-admission baseline | 08-11-2026 | `c2-submission` | 93.75/100 |
| `GROUP_01_W3/` | W3 · Visual system for the C2 results | 21-11-2026 | `w3-submission` | pending |

## Where to start

- W1 has no package README (as submitted). Start from `GROUP_01_W1/report/GROUP_01_Report.pdf`.
- C1 starts from `GROUP_01_C1/README.md`.
- W2 starts from `GROUP_01_W2/README.md` and `GROUP_01_W2/notebooks/W2_project.ipynb`.
- C2 starts from `GROUP_01_C2/notebooks/C2_model.ipynb`.
- W3 starts from `GROUP_01_W3/README.md` and `GROUP_01_W3/report/GROUP_01_W3_Report.pdf`.

## Data

- The reduced FONASA extracts and reference files live in `GROUP_01_C1/data/`. They are byte-identical to W1's copies, and W2 reads them in place.
- Provenance, download URLs and SHA-256 checksums are in `GROUP_01_C1/README.md` and `GROUP_01_W2/README.md`.

## Feedback received

- **W1:** the deduction was the missing README entry point. The instructor also asked to close clearly the definition of the stay benchmark and its limits. Both were addressed in C1.
- **C1 (94/100):** the README was named incorrectly; paths and packaging should be reviewed; methodology and traceability were judged fully complete.
  - The C1 README is stored in this repository as `GROUP_01_C1/README.md`.
  - The W2 notebook checks paths and packaging.
  - Informal feedback also asked to state the hypotheses before presenting results and data, which W2 does.
- **W2 (100/100):** exclude fields not available at admission; freeze extreme-stay thresholds inside training. Both applied in C2.
- **C2 (93.75/100):** no deductions on documentation; deductions on presentation clarity and on connecting the data to its purpose for the audience.
  - Also asked to report how many models were tried before choosing the final one, and to compare at least 3 to 5 candidate models at each modelling stage. C2 trained one model (logistic regression) against two reference rules; this applies from C3.
