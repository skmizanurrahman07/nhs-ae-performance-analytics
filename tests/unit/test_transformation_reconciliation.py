"""Tests for processed-to-published total reconciliation."""

from typing import cast

import pandas as pd
import pytest

from nhs_ae.transformation.provider import transform_provider_records
from nhs_ae.transformation.reconciliation import reconcile_processed_totals
from nhs_ae.validation.schema import IDENTIFIER_COLUMNS, MEASURE_COLUMNS


def make_test_data() -> pd.DataFrame:
    """Create provider records with a matching published TOTAL."""
    rows: list[dict[str, object]] = []

    for period, code, value in (
        ("MSitAE-SEPTEMBER-2026", "AAA", 1),
        ("MSitAE-SEPTEMBER-2026", "BBB", 2),
        ("TOTAL", "TOTAL", 3),
    ):
        row: dict[str, object] = {
            "Period": period,
            "Org Code": code,
            "Parent Org": (
                "TOTAL" if code == "TOTAL" else "NHS ENGLAND TEST REGION"
            ),
            "Org name": (
                "TOTAL" if code == "TOTAL" else f"Provider {code}"
            ),
        }

        for column in MEASURE_COLUMNS:
            row[column] = value

        rows.append(row)

    return pd.DataFrame(
        rows,
        columns=[
            *IDENTIFIER_COLUMNS,
            *MEASURE_COLUMNS,
        ],
    )


def test_processed_totals_reconcile() -> None:
    """All processed measures must reconcile to published totals."""
    raw_data = make_test_data()
    processed_data = transform_provider_records(raw_data)

    result = reconcile_processed_totals(
        raw_data,
        processed_data,
    )

    assert len(result) == 18
    assert result["difference"].eq(0).all()
    assert result["reconciled"].all()


def test_reconciliation_detects_difference() -> None:
    """Changed processed activity must fail reconciliation."""
    raw_data = make_test_data()
    processed_data = transform_provider_records(raw_data)

    current_value = cast(
        int,
    processed_data.at[
            0,
            "ae_attendances_type1",
        ],
    )

    processed_data.at[
        0,
        "ae_attendances_type1",
    ] = current_value + 1

    result = reconcile_processed_totals(
        raw_data,
        processed_data,
    )

    type1 = result.loc[
        result["standard_column"].eq(
            "ae_attendances_type1"
        )
    ].iloc[0]

    assert type1["difference"] == 1
    assert not bool(type1["reconciled"])


def test_reconciliation_requires_one_total() -> None:
    """Reconciliation must require exactly one published TOTAL."""
    raw_data = make_test_data()
    raw_data = raw_data.loc[
        raw_data["Period"].ne("TOTAL")
    ]

    processed_data = transform_provider_records(raw_data)

    with pytest.raises(
        ValueError,
        match="Expected exactly one published TOTAL",
    ):
        reconcile_processed_totals(
            raw_data,
            processed_data,
        )
