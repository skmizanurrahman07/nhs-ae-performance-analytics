"""Reconcile processed measures against published raw totals."""

import pandas as pd

from nhs_ae.transformation.columns import (
    COLUMN_RENAME_MAP,
    STANDARD_MEASURE_COLUMNS,
)
from nhs_ae.validation.profiling import total_records
from nhs_ae.validation.schema import MEASURE_COLUMNS


def reconcile_processed_totals(
    raw_data: pd.DataFrame,
    processed_data: pd.DataFrame,
) -> pd.DataFrame:
    """Compare processed measure sums with published raw totals."""
    totals = total_records(raw_data)

    if len(totals) != 1:
        message = (
            "Expected exactly one published TOTAL record; "
            f"found {len(totals)}."
        )
        raise ValueError(message)

    published = totals.iloc[0]

    raw_to_standard = {
        raw_column: COLUMN_RENAME_MAP[raw_column]
        for raw_column in MEASURE_COLUMNS
    }

    rows: list[dict[str, object]] = []

    for raw_column, standard_column in raw_to_standard.items():
        processed_total = processed_data[standard_column].sum()
        published_total = published[raw_column]
        difference = processed_total - published_total

        rows.append(
            {
                "raw_column": raw_column,
                "standard_column": standard_column,
                "processed_total": processed_total,
                "published_total": published_total,
                "difference": difference,
                "reconciled": difference == 0,
            }
        )

    result = pd.DataFrame(rows)

    if tuple(result["standard_column"]) != STANDARD_MEASURE_COLUMNS:
        raise ValueError(
            "Reconciliation measure order does not match the contract."
        )

    return result
