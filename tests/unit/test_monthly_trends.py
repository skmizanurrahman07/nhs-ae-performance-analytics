"""Tests for approved monthly KPI trend analysis."""

import pandas as pd
import pytest

from nhs_ae.analysis.monthly_trends import (
    build_monthly_approved_kpis,
)


def make_monthly_kpi_data() -> pd.DataFrame:
    """Create representative provider-level KPI data."""
    return pd.DataFrame(
        {
            "reporting_month": pd.to_datetime(
                [
                    "2024-09-01",
                    "2024-09-01",
                    "2024-10-01",
                    "2024-10-01",
                ]
            ),
            "total_attendances": [
                100,
                200,
                110,
                220,
            ],
            "emergency_admissions": [
                20,
                40,
                22,
                44,
            ],
        }
    )


def test_builds_monthly_approved_kpis() -> None:
    """Provider KPI values must aggregate by month."""
    result = build_monthly_approved_kpis(
        make_monthly_kpi_data()
    )

    assert len(result) == 2
    assert result["total_attendances"].tolist() == [
        300,
        330,
    ]
    assert result["emergency_admissions"].tolist() == [
        60,
        66,
    ]


def test_calculates_monthly_change() -> None:
    """Monthly percentage changes must be calculated."""
    result = build_monthly_approved_kpis(
        make_monthly_kpi_data()
    )

    assert pd.isna(
        result.iloc[0]["attendance_monthly_change"]
    )
    assert result.iloc[1][
        "attendance_monthly_change"
    ] == pytest.approx(0.10)

    assert result.iloc[1][
        "admission_monthly_change"
    ] == pytest.approx(0.10)


def test_rejects_missing_kpi_column() -> None:
    """Missing approved KPI columns must fail."""
    data = make_monthly_kpi_data().drop(
        columns=["emergency_admissions"]
    )

    with pytest.raises(
        ValueError,
        match="Required monthly KPI columns are missing",
    ):
        build_monthly_approved_kpis(data)
