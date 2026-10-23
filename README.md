# Business Intelligence IIB423T-1 · GROUP_01

Universidad del Desarrollo · Instructor: Tomás Fontecilla Correa · Members: Matías López, Cristóbal Ramírez

Line of inquiry: case-mix-adjusted length of stay and extreme stays in the public hospitals funded through GRD (FONASA public files, discharges 2023-2024).

Each stage is a separate package folder. W1 and C1 are kept exactly as submitted, and tags mark each submission.

| Folder | Stage | Submitted | Tag | Result |
|---|---|---|---|---|
| `GROUP_01_W1/` | W1 · Discovering questions worth investigating (candidates A and B) | 25-09-2026 | `w1-submission` | 97/100 |
| `GROUP_01_C1/` | C1 · Profiling, preparation, closed benchmark, sensitivity and EDA of candidate B | 29-09-2026 | `c1-submission` | pending |
| `GROUP_01_W2/` | W2 · Validation checks, revised EDA, sampling, leakage audit and train/validation/test split | 29-10-2026 | `w2-submission` | pending |

## Where to start

- W1 has no package README (as submitted). Start from `GROUP_01_W1/report/GROUP_01_Report.pdf`.
- C1 starts from `GROUP_01_C1/README.md`.
- W2 starts from `GROUP_01_W2/README.md` and `GROUP_01_W2/notebooks/W2_project.ipynb`.

## Data

- The reduced FONASA extracts and reference files live in `GROUP_01_C1/data/`. They are byte-identical to W1's copies, and W2 reads them in place.
- Provenance, download URLs and SHA-256 checksums are in `GROUP_01_C1/README.md` and `GROUP_01_W2/README.md`.

## Feedback received

- **W1:** the deduction was the missing README entry point. The instructor also asked to close clearly the definition of the stay benchmark and its limits. Both were addressed in C1.
- **C1:** informal feedback asked to state the hypotheses before presenting results and data. This is addressed in W2.
