"""Tests for provider-level source transformation."""

import pandas as pd

from nhs_ae.transformation.provider import transform_provider_records
from nhs_ae.validation.schema import (
    IDENTIFIER_COLUMNS,
    MEASURE_COLUMNS,
)


def make_test_data(
    period: str = "MSitAE-SEPTEMBER-2026",
    total_period: str = "TOTAL",
) -> pd.DataFrame:
    """Create representative raw provider and TOTAL records."""
    rows: list[dict[str, object]] = []

    for reporting_period, code in (
        (period, "AAA"),
        (total_period, "TOTAL"),
    ):
        row: dict[str, object] = {
            "Period": reporting_period,
            "Org Code": code,
            "Parent Org": (
                "TOTAL"
                if code == "TOTAL"
                else "NHS ENGLAND TEST REGION "
            ),
            "Org name": (
                "TOTAL"
                if code == "TOTAL"
                else "Provider AAA"
            ),
        }

        for column in MEASURE_COLUMNS:
            row[column] = 1

        rows.append(row)

    return pd.DataFrame(
        rows,
        columns=[
            *IDENTIFIER_COLUMNS,
            *MEASURE_COLUMNS,
        ],
    )


def test_transform_excludes_total_record() -> None:
    """Analytical provider data must exclude TOTAL."""
    result = transform_provider_records(make_test_data())

    assert len(result) == 1
    assert "TOTAL" not in result["reporting_period_raw"].values


def test_transform_excludes_historical_total_record() -> None:
    """Historical Total row must not enter provider data."""
    result = transform_provider_records(
        make_test_data(
            period="MSitAE-SEPTEMBER-2024",
            total_period="Total",
        )
    )

    assert len(result) == 1
    assert "Total" not in result["reporting_period_raw"].values


def test_transform_creates_reporting_month() -> None:
    """Raw period must produce a monthly analytical date."""
    result = transform_provider_records(make_test_data())

    assert result.iloc[0]["reporting_month"] == pd.Timestamp(
        "2026-09-01"
    )


def test_transform_creates_historical_reporting_month() -> None:
    """Historical period must produce the correct monthly date."""
    result = transform_provider_records(
        make_test_data(
            period="MSitAE-SEPTEMBER-2024",
            total_period="Total",
        )
    )

    assert result.iloc[0]["reporting_month"] == pd.Timestamp(
        "2024-09-01"
    )


def test_transform_strips_parent_org_whitespace() -> None:
    """Controlled transformation must trim Parent Org."""
    result = transform_provider_records(make_test_data())

    assert result.iloc[0]["parent_org"] == (
        "NHS ENGLAND TEST REGION"
    )


def test_transform_preserves_raw_reporting_period() -> None:
    """Original reporting-period value must remain traceable."""
    result = transform_provider_records(make_test_data())

    assert result.iloc[0]["reporting_period_raw"] == (
        "MSitAE-SEPTEMBER-2026"
    )


def test_transform_outputs_integer_measures() -> None:
    """All standardised measures must use integer dtype."""
    result = transform_provider_records(make_test_data())

    measure_columns = result.columns[5:]

    assert all(
        pd.api.types.is_integer_dtype(result[column])
        for column in measure_columns
    )
