"""Tests for monthly A&E pressure trend analysis."""

import pandas as pd
import pytest

from nhs_ae.analysis.pressure_trends import (
    build_monthly_pressure_trends,
)


def make_pressure_trend_data() -> pd.DataFrame:
    """Create representative provider pressure data."""
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
            "four_hour_breaches": [
                100,
                200,
                110,
                220,
            ],
            "dta_waits_4_12hrs": [
                20,
                40,
                22,
                44,
            ],
            "dta_waits_12plus_hrs": [
                5,
                10,
                6,
                12,
            ],
            "total_dta_waits_4plus_hrs": [
                25,
                50,
                28,
                56,
            ],
        }
    )


def test_builds_monthly_pressure_totals() -> None:
    """Provider pressure values must aggregate by month."""
    result = build_monthly_pressure_trends(
        make_pressure_trend_data()
    )

    assert len(result) == 2
    assert result["four_hour_breaches"].tolist() == [
        300,
        330,
    ]
    assert result["dta_waits_4_12hrs"].tolist() == [
        60,
        66,
    ]
    assert result["dta_waits_12plus_hrs"].tolist() == [
        15,
        18,
    ]
    assert result[
        "total_dta_waits_4plus_hrs"
    ].tolist() == [
        75,
        84,
    ]


def test_calculates_pressure_monthly_change() -> None:
    """Pressure trends must calculate monthly changes."""
    result = build_monthly_pressure_trends(
        make_pressure_trend_data()
    )

    assert pd.isna(
        result.iloc[0][
            "four_hour_breaches_monthly_change"
        ]
    )

    assert result.iloc[1][
        "four_hour_breaches_monthly_change"
    ] == pytest.approx(0.10)

    assert result.iloc[1][
        "dta_waits_4_12hrs_monthly_change"
    ] == pytest.approx(0.10)


def test_rejects_missing_pressure_column() -> None:
    """Missing pressure columns must fail."""
    data = make_pressure_trend_data().drop(
        columns=["four_hour_breaches"]
    )

    with pytest.raises(
        ValueError,
        match="Required pressure trend columns are missing",
    ):
        build_monthly_pressure_trends(data)
