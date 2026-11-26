"""Tests for multi-month provider dataset assembly."""

from pathlib import Path

import pandas as pd
import pytest

from nhs_ae.transformation.multimonth import (
    combine_monthly_provider_data,
)


def write_month(
    path: Path,
    month: str,
    org_code: str = "AAA",
) -> None:
    """Write a representative processed monthly dataset."""
    data = {
        "reporting_period_raw": [f"MSitAE-{month}"],
        "reporting_month": [pd.Timestamp(month)],
        "org_code": [org_code],
        "org_name": [f"Provider {org_code}"],
        "parent_org": ["NHS ENGLAND TEST REGION"],
    }

    for index in range(18):
        data[f"measure_{index}"] = [index]

    pd.DataFrame(data).to_csv(
        path,
        index=False,
    )


def test_combines_consecutive_months(
    tmp_path: Path,
) -> None:
    """Consecutive monthly datasets must combine successfully."""
    september = tmp_path / "september.csv"
    october = tmp_path / "october.csv"

    write_month(
        september,
        "2024-09-01",
    )
    write_month(
        october,
        "2024-10-01",
    )

    result = combine_monthly_provider_data(
        [september, october],
        start_month="2024-09-01",
        end_month="2024-10-01",
    )

    assert len(result) == 2
    assert len(result.columns) == 23
    assert result["reporting_month"].nunique() == 2


def test_rejects_missing_month(
    tmp_path: Path,
) -> None:
    """Missing reporting months must fail validation."""
    september = tmp_path / "september.csv"
    november = tmp_path / "november.csv"

    write_month(
        september,
        "2024-09-01",
    )
    write_month(
        november,
        "2024-11-01",
    )

    with pytest.raises(
        ValueError,
        match="Reporting-month sequence",
    ):
        combine_monthly_provider_data(
            [september, november],
            start_month="2024-09-01",
            end_month="2024-11-01",
        )


def test_rejects_duplicate_provider_month_key(
    tmp_path: Path,
) -> None:
    """Duplicate provider-month keys must fail validation."""
    first = tmp_path / "first.csv"
    second = tmp_path / "second.csv"

    write_month(
        first,
        "2024-09-01",
    )
    write_month(
        second,
        "2024-09-01",
    )

    with pytest.raises(
        ValueError,
        match="Duplicate provider-month keys",
    ):
        combine_monthly_provider_data(
            [first, second],
            start_month="2024-09-01",
            end_month="2024-09-01",
        )


def test_rejects_inconsistent_schema(
    tmp_path: Path,
) -> None:
    """Monthly schema differences must fail validation."""
    september = tmp_path / "september.csv"
    october = tmp_path / "october.csv"

    write_month(
        september,
        "2024-09-01",
    )
    write_month(
        october,
        "2024-10-01",
    )

    data = pd.read_csv(october)
    data["unexpected_column"] = 1
    data.to_csv(
        october,
        index=False,
    )

    with pytest.raises(
        ValueError,
        match="schemas are inconsistent",
    ):
        combine_monthly_provider_data(
            [september, october],
            start_month="2024-09-01",
            end_month="2024-10-01",
        )
