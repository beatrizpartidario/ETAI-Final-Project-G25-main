"""Deterministic cleaning for ETAI purchase records.

Use on train, test, or a new purchase before model-specific preprocessing.
This module does not learn statistics, impute missing values, drop rows,
or modify target labels. It leaves the source DataFrame unchanged.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# Timing and standard deviations cannot be negative.
NONNEGATIVE_FEATURES = (
    "days_since_previous_purchase",
    "customer_tenure_days",
    "prior_mean_gap_days",
    "prior_std_gap_days",
    "prior_mean_purchase_value",
    "prior_std_purchase_value",
    "spend_30d",
    "spend_90d",
    "spend_180d",
    "spend_365d",
)

# Historical purchase counts: nonnegative whole numbers.
NONNEGATIVE_INTEGER_COUNTS = (
    "prior_purchase_count",
    "purchase_count_30d",
    "purchase_count_90d",
    "purchase_count_180d",
    "purchase_count_365d",
)

# Current transaction counts: positive whole numbers.
POSITIVE_INTEGER_COUNTS = (
    "N_ Detalhes",
    "invoice_count_current_purchase",
)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Replace confirmed domain-rule violations with NaN, preserving rows.

    Does not resolve suspicious monetary values (such as 1e9), negative
    monetary amounts (possibly returns), or cross-column discrepancies:
    those require a documented business rule before automatic correction.
    """
    cleaned = df.copy()

    if "purchase_date" in cleaned.columns:
        cleaned["purchase_date"] = pd.to_datetime(
            cleaned["purchase_date"], errors="coerce", format="%Y-%m-%d"
        )

    for col in (NONNEGATIVE_FEATURES):
        if col in cleaned.columns:
            values = pd.to_numeric(cleaned[col], errors="coerce")
            cleaned[col] = values.mask(values < 0)

    for col in (*NONNEGATIVE_INTEGER_COUNTS, *POSITIVE_INTEGER_COUNTS):
        if col in cleaned.columns:
            values = pd.to_numeric(cleaned[col], errors="coerce")
            minimum = 1 if col in POSITIVE_INTEGER_COUNTS else 0
            invalid = (values < minimum) | (values.notna() & (values % 1 != 0))
            cleaned[col] = values.mask(invalid)

    return cleaned
