"""Generate a read-only audit of the ETAI datasets (no cleaning and no training)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]


def summarize_table(df: pd.DataFrame, date_column: str = "purchase_date") -> dict:
    """Report observable data quality without changing the original dataframe."""
    out: dict = {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "duplicate_rows": int(df.duplicated().sum()),
        "nulls_by_column": {str(k): int(v) for k, v in df.isna().sum().items()},
        "dtypes": {str(k): str(v) for k, v in df.dtypes.items()},
    }
    if "ID" in df:
        out["duplicate_IDs"] = int(df["ID"].duplicated().sum())
    if "customer_id" in df:
        out["unique_customers"] = int(df["customer_id"].nunique(dropna=True))
    if date_column in df:
        parsed = pd.to_datetime(df[date_column], errors="coerce")
        out["date_unparseable_or_missing"] = int(parsed.isna().sum())
        out["date_min"] = str(parsed.min().date()) if parsed.notna().any() else None
        out["date_max"] = str(parsed.max().date()) if parsed.notna().any() else None
    # Explicit sentinels and impossible values flagged for human review, never fixed here.
    diagnostics = {}
    for col in ("days_since_previous_purchase", "prior_mean_gap_days", "prior_std_gap_days", "customer_tenure_days"):
        if col in df:
            values = pd.to_numeric(df[col], errors="coerce")
            diagnostics[f"negative::{col}"] = int((values < 0).sum())
    for col in ("prior_mean_purchase_value", "spend_365d"):
        if col in df:
            values = pd.to_numeric(df[col], errors="coerce")
            diagnostics[f"value_1e9::{col}"] = int(np.isclose(values, 1e9).sum())
    out["diagnostics_requiring_review"] = diagnostics
    return out


def audit(config_path: Path) -> tuple[dict, Path]:
    config_path = config_path.expanduser().resolve()
    with config_path.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    # Paths in config are project-relative regardless of the working directory.
    def project_path(value: str) -> Path:
        p = Path(value)
        return p if p.is_absolute() else ROOT / p

    frames = {}
    for key, config_key in (("train", "train"), ("test", "test"), ("customers", "customers"),
                            ("sample_submission", "sample_submission")):
        p = project_path(config["data"][config_key])
        if not p.is_file():
            raise FileNotFoundError(f"Missing {key}: {p}. Run uv run python -m src.prepare_data first.")
        frames[key] = pd.read_csv(p, low_memory=False)

    date_column = config["columns"]["date"]
    report = {
        "description": "Read-only source-data audit; no transformations or model fitting performed.",
        "files": {key: summarize_table(df, date_column) for key, df in frames.items()},
    }
    train, test = frames["train"], frames["test"]
    classification_target = config["columns"]["classification_target"]
    regression_target = config["columns"]["regression_target"]
    if classification_target not in train or regression_target not in train:
        raise ValueError("Training targets are missing from train.csv")
    if classification_target in test or regression_target in test:
        raise ValueError("Targets unexpectedly present in test.csv; review data provenance")
    diff = sorted((set(train.columns) - {classification_target, regression_target}) ^ set(test.columns))
    report["features_symmetric_difference_train_test"] = diff
    y = pd.to_numeric(train[classification_target], errors="coerce")
    report["classification_target_counts"] = {
        str(int(value)): int((y == value).sum()) for value in (0, 1)
    }
    report["classification_target_missing_or_invalid"] = int((~y.isin([0, 1])).sum())
    spend = pd.to_numeric(train[regression_target], errors="coerce")
    report["regression_target_missing_among_positives"] = int((y.eq(1) & spend.isna()).sum())
    report["regression_target_present_among_negatives"] = int((y.eq(0) & spend.notna()).sum())
    if "customer_id" in train and "customer_id" in test:
        a, b = set(train["customer_id"].dropna()), set(test["customer_id"].dropna())
        report["customer_overlap"] = {
            "train_unique": len(a), "test_unique": len(b),
            "seen_in_both": len(a & b), "test_only": len(b - a)
        }
    output = project_path(config["outputs"]["audit_summary"])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report, output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "config.yaml")
    args = parser.parse_args()
    report, output = audit(args.config)
    print("ETAI dataset audit (read-only)")
    for name, info in report["files"].items():
        print(f"  {name:>17}: {info['rows']:,} rows x {info['columns']} columns")
    print(f"  Classification counts: {report['classification_target_counts']}")
    print(f"  Missing regression labels for returning purchases: "
          f"{report['regression_target_missing_among_positives']}")
    print(f"  Report: {output}")


if __name__ == "__main__":
    main()
