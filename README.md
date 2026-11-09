# ETAI 2026/27 — Everything & Then Some

**Task:** predict whether a wholesale customer will purchase again within the next 90 days of a purchase, and estimate the subsequent 90-day spend conditional on returning.

**Course:** Experimental Topics in Artificial Intelligence (NOVA IMS)  
**Project deadline:** 22 December 2026, 18:00 (Europe/Lisbon)

> **Current status: scaffold + dataset loading and read-only audit.** Model training, evaluation, inference and client interface are **not implemented yet**. Do not present this repository as deployment-ready.

## Data

The assignment provides four CSVs in `Project data-20261102.zip`:

| File | Use |
|---|---|
| `train.csv` | Historical purchase occasions with classification and regression labels |
| `test.csv` | Later purchase occasions; labels are withheld |
| `clientes.csv` | Optional customer metadata, joinable by `customer_id` |
| `sample_submission.csv` | Kaggle submission example (`ID`, `repeat_purchase_90d`) |

**One row represents a purchase occasion, not a unique customer.** Store supplied data only in `data/raw/`. These files are excluded by `.gitignore`. Do not commit them without explicit authorization to distribute the assignment data.

## Setup (Python 3.12 + uv)

Install **uv** following the official instructions: <https://docs.astral.sh/uv/getting-started/installation/>. Run the following commands in the repository root on **macOS or Windows** (PowerShell):

```bash
uv sync
```

`uv` creates/manages `.venv` and installs Python 3.12 if needed. The **first successful** `uv sync` will also create `uv.lock`. **Commit `uv.lock`** to make the environment reproducible across the team; afterwards prefer `uv sync --locked`.

Add dependencies with `uv add <package>`, and development-only dependencies with `uv add --dev <package>`. Do not manually install into the project `.venv` or maintain two independent lists of versions.

The assignment explicitly requires a requirements file. After generating the lockfile, refresh the compatibility export:

```bash
uv export --format requirements.txt --no-dev --no-hashes --output-file requirements.txt
```

`pyproject.toml` and `uv.lock` are the authoritative dependency declarations. `requirements.txt` exists as a derived compatibility deliverable, not as another source of truth.

## Load the supplied data

Run this from the root of the repository with the path to the original ZIP:

```bash
uv run python -m src.prepare_data --archive "/path/to/Project data-20261102.zip"
```

On Windows:

```powershell
uv run python -m src.prepare_data --archive "C:\path\to\Project data-20261102.zip"
```

This extracts only the four expected CSVs to `data/raw/`. It never changes the original ZIP. If files already exist, the command stops unless `--overwrite` is provided.

## Run the initial audit

```bash
uv run python -m src.audit --config config.yaml
```

It generates `outputs/audit_summary.json` with file dimensions, missing values, invalid dates, target availability, duplicated rows and IDs, and selected suspicious-value checks. **This is a diagnostic report, not a cleaning pipeline.**

## Run tests

```bash
uv run pytest -q
```

CI runs tests without the proprietary/assignment dataset.

## Planned pipeline

1. Document EDA, data cleaning and leakage risks.
2. Define temporal validation with a 90-day label-availability buffer, and an untouched holdout. Compare appropriate alternative validation strategies.
3. Benchmark **at least five** classification algorithms, including preprocessing, feature engineering, feature selection, tuning and metric interpretation.
4. Benchmark **at least four** regression algorithms, measuring conditional spend prediction and coherent use with classification.
5. Save trained artifacts and implement terminal training, batch inference, and single-purchase client inference.
6. Add global and local explanations for both tasks and an additional, meaningful analysis or client dashboard.
7. Produce Kaggle predictions from the saved pipeline, test from a fresh clone, and document Mac/Windows commands.

## Important modelling constraints

- Never use `spend_next_90d` as a classification feature.
- Use only features available at the time of the purchase.
- A test row may use **itself**, the supplied training data and `clientes.csv`; it must never use **other test rows** to build features.
- The 90-day future labels must be available before a row becomes eligible for training at a given temporal split.
- Fit imputers, encoders, feature selectors and statistical cleaning parameters **within the training portion of each fold**, not on the entire dataset.
- Do not use Lazy Predict / disallowed AutoML packages.
- Document all choices in `docs/decision_log.md`. The assignment defense may question any part of the code.

## Repository structure

```text
.
├── .github/workflows/ci.yml
├── .python-version
├── pyproject.toml
├── uv.lock                  # created by the first successful uv sync; commit it
├── requirements.txt         # compatibility export, required by the assignment
├── config.yaml
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── notebooks/              # exploratory work and documented experiments
├── src/
│   ├── audit.py
│   ├── prepare_data.py
│   └── models/              # model-building source code (not fitted models)
├── artifacts/
│   └── models/              # serialized fitted pipelines (git-ignored)
├── outputs/                # generated reports, predictions and charts
├── tests/
└── docs/
    ├── requirements_checklist.md
    └── decision_log.md
```

Do not make notebooks part of production training/inference; migrate reusable code to `src/`.

*See `docs/requirements_checklist.md` for the exact requirements transcribed into a working checklist from the supplied assignment brief.*
