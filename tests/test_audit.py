import pandas as pd
from src.audit import summarize_table


def test_summary_does_not_modify_input():
    df = pd.DataFrame({
        "ID": [1, 1, 2],
        "customer_id": [3, 3, 4],
        "purchase_date": ["2024-01-01", "not-a-date", None],
        "days_since_previous_purchase": [2, -4, None],
        "spend_365d": [10.0, 1e9, None],
    })
    original = df.copy(deep=True)
    report = summarize_table(df)
    pd.testing.assert_frame_equal(df, original)
    assert report["rows"] == 3
    assert report["duplicate_IDs"] == 1
    assert report["unique_customers"] == 2
    assert report["date_unparseable_or_missing"] == 2
    assert report["diagnostics_requiring_review"]["negative::days_since_previous_purchase"] == 1
    assert report["diagnostics_requiring_review"]["value_1e9::spend_365d"] == 1
