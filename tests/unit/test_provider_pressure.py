"""Tests for provider-level pressure and flow analysis."""

import pandas as pd
import pytest

from nhs_ae.analysis.provider_pressure import (
    compare_provider_pressure,
)


def make_provider_pressure_data() -> pd.DataFrame:
    """Create representative provider pressure data."""
    return pd.DataFrame(
        {
            "reporting_month": pd.to_datetime(
                [
                    "2025-09-01",
                    "2026-09-01",
                    "2025-09-01",
                    "2026-09-01",
                ]
            ),
            "org_code": ["AAA", "AAA", "BBB", "BBB"],
            "org_name": [
                "Provider AAA",
                "Provider AAA",
                "Provider BBB",
                "Provider BBB",
            ],
            "total_attendances": [
                20_000,
                22_000,
                500,
                600,
            ],
            "emergency_admissions": [
                4_000,
                4_200,
                100,
                120,
            ],
            "four_hour_breaches": [
                5_000,
                5_500,
                50,
                60,
            ],
            "dta_waits_4_12hrs": [
                600,
                540,
                10,
                12,
            ],
            "dta_waits_12plus_hrs": [
                100,
                150,
                2,
                3,
            ],
            "total_dta_waits_4plus_hrs": [
                700,
                690,
                12,
                15,
            ],
        }
    )


def test_calculates_pressure_changes() -> None:
    """Pressure changes must be calculated correctly."""
    result = compare_provider_pressure(
        make_provider_pressure_data(),
        current_month="2026-09-01",
        comparison_month="2025-09-01",
        full_period_months=2,
    )

    provider = result.loc[
        result["org_code"].eq("AAA")
    ].iloc[0]

    assert provider[
        "four_hour_breaches_absolute_change"
    ] == 500

    assert provider[
        "four_hour_breaches_percentage_change"
    ] == pytest.approx(0.10)

    assert provider[
        "dta_waits_4_12hrs_absolute_change"
    ] == -60

    assert provider[
        "dta_waits_12plus_hrs_absolute_change"
    ] == 50

    assert provider[
        "total_dta_waits_4plus_hrs_absolute_change"
    ] == -10


def test_sets_separate_analysis_eligibility() -> None:
    """Breach and DTA eligibility must use appropriate volumes."""
    result = compare_provider_pressure(
        make_provider_pressure_data(),
        current_month="2026-09-01",
        comparison_month="2025-09-01",
        minimum_attendance_volume=10_000,
        minimum_admission_volume=1_000,
        full_period_months=2,
    )

    provider_aaa = result.loc[
        result["org_code"].eq("AAA")
    ].iloc[0]

    provider_bbb = result.loc[
        result["org_code"].eq("BBB")
    ].iloc[0]

    assert bool(
        provider_aaa["breach_analysis_eligible"]
    )
    assert bool(
        provider_aaa["dta_analysis_eligible"]
    )

    assert not bool(
        provider_bbb["breach_analysis_eligible"]
    )
    assert not bool(
        provider_bbb["dta_analysis_eligible"]
    )


def test_zero_baseline_does_not_create_infinity() -> None:
    """Zero historical pressure must return missing percentage change."""
    data = make_provider_pressure_data()

    data.loc[
        data["org_code"].eq("AAA")
        & data["reporting_month"].eq(
            pd.Timestamp("2025-09-01")
        ),
        "dta_waits_12plus_hrs",
    ] = 0

    result = compare_provider_pressure(
        data,
        current_month="2026-09-01",
        comparison_month="2025-09-01",
        full_period_months=2,
    )

    provider = result.loc[
        result["org_code"].eq("AAA")
    ].iloc[0]

    assert pd.isna(
        provider[
            "dta_waits_12plus_hrs_percentage_change"
        ]
    )


def test_rejects_missing_pressure_columns() -> None:
    """Incomplete pressure data must fail."""
    data = make_provider_pressure_data().drop(
        columns=["four_hour_breaches"]
    )

    with pytest.raises(
        ValueError,
        match="Required provider pressure columns are missing",
    ):
        compare_provider_pressure(
            data,
            current_month="2026-09-01",
            comparison_month="2025-09-01",
        )


def test_rejects_duplicate_provider_month_keys() -> None:
    """Duplicate provider-month records must fail."""
    data = make_provider_pressure_data()

    data = pd.concat(
        [
            data,
            data.iloc[[0]],
        ],
        ignore_index=True,
    )

    with pytest.raises(
        ValueError,
        match="Duplicate provider-month keys",
    ):
        compare_provider_pressure(
            data,
            current_month="2026-09-01",
            comparison_month="2025-09-01",
        )


def test_rejects_negative_thresholds() -> None:
    """Negative volume thresholds must fail."""
    with pytest.raises(
        ValueError,
        match="attendance volume cannot be negative",
    ):
        compare_provider_pressure(
            make_provider_pressure_data(),
            current_month="2026-09-01",
            comparison_month="2025-09-01",
            minimum_attendance_volume=-1,
        )

    with pytest.raises(
        ValueError,
        match="admission volume cannot be negative",
    ):
        compare_provider_pressure(
            make_provider_pressure_data(),
            current_month="2026-09-01",
            comparison_month="2025-09-01",
            minimum_admission_volume=-1,
        )
