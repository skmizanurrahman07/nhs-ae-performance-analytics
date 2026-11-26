"""Assemble validated monthly provider datasets."""

from collections.abc import Sequence
from pathlib import Path

import pandas as pd

EXPECTED_COLUMN_COUNT = 23
PROVIDER_KEY_COLUMNS = (
    "reporting_month",
    "org_code",
)


def combine_monthly_provider_data(
    source_paths: Sequence[Path],
    *,
    start_month: str,
    end_month: str,
) -> pd.DataFrame:
    """Combine validated monthly provider files into one dataset."""
    if not source_paths:
        raise ValueError("No monthly provider files supplied.")

    frames = [
        pd.read_csv(
            path,
            parse_dates=["reporting_month"],
        )
        for path in source_paths
    ]

    schemas = {
        tuple(frame.columns)
        for frame in frames
    }

    if len(schemas) != 1:
        raise ValueError(
            "Processed monthly schemas are inconsistent."
        )

    combined = pd.concat(
        frames,
        ignore_index=True,
    )

    if len(combined.columns) != EXPECTED_COLUMN_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_COLUMN_COUNT} analytical columns; "
            f"found {len(combined.columns)}."
        )

    expected_months = pd.date_range(
        start_month,
        end_month,
        freq="MS",
    )

    actual_months = pd.DatetimeIndex(
        combined["reporting_month"]
        .drop_duplicates()
        .sort_values()
    )

    if not actual_months.equals(expected_months):
        raise ValueError(
            "Reporting-month sequence does not match "
            "the expected analytical period."
        )

    duplicate_keys = combined.duplicated(
        subset=list(PROVIDER_KEY_COLUMNS),
        keep=False,
    )

    if duplicate_keys.any():
        duplicate_count = int(
            duplicate_keys.sum()
        )
        raise ValueError(
            "Duplicate provider-month keys detected: "
            f"{duplicate_count} rows."
        )

    return combined.sort_values(
        [
            "reporting_month",
            "org_code",
        ],
        kind="stable",
    ).reset_index(drop=True)
