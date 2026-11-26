"""Tests for volume-controlled provider change analysis."""

import pandas as pd
import pytest

from nhs_ae.analysis.provider_changes import (
    compare_provider_periods,
)


def make_provider_change_data() -> pd.DataFrame:
    """Create representative provider-period KPI data."""
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
            "org_code": [
                "AAA",
                "AAA",
                "BBB",
                "BBB",
            ],
            "org_name": [
                "Provider AAA",
                "Provider AAA Renamed",
                "Provider BBB",
                "Provider BBB",
            ],
            "total_attendances": [
                20_000,
                23_000,
                500,
                1_000,
            ],
            "emergency_admissions": [
                4_000,
                4_400,
                100,
                150,
            ],
        }
    )


def test_compares_absolute_and_percentage_changes() -> None:
    """Comparison must calculate absolute and percentage changes."""
    result = compare_provider_periods(
        make_provider_change_data(),
        current_month="2026-09-01",
        comparison_month="2025-09-01",
        minimum_attendance_volume=10_000,
        full_period_months=2,
    )

    provider_aaa = result.loc[
        result["org_code"].eq("AAA")
    ].iloc[0]

    assert provider_aaa["attendance_absolute_change"] == 3_000
    assert provider_aaa[
        "attendance_percentage_change"
    ] == pytest.approx(0.15)
    assert provider_aaa["admission_absolute_change"] == 400
    assert provider_aaa[
        "admission_percentage_change"
    ] == pytest.approx(0.10)


def test_flags_low_volume_provider() -> None:
    """Low-volume providers must be excluded from main ranking."""
    result = compare_provider_periods(
        make_provider_change_data(),
        current_month="2026-09-01",
        comparison_month="2025-09-01",
        minimum_attendance_volume=10_000,
        full_period_months=2,
    )

    provider_bbb = result.loc[
        result["org_code"].eq("BBB")
    ].iloc[0]

    assert not bool(
        provider_bbb["meets_volume_threshold"]
    )
    assert not bool(provider_bbb["analysis_eligible"])


def test_flags_provider_name_change() -> None:
    """Organisation-name changes must be flagged."""
    result = compare_provider_periods(
        make_provider_change_data(),
        current_month="2026-09-01",
        comparison_month="2025-09-01",
        minimum_attendance_volume=0,
        full_period_months=2,
    )

    provider_aaa = result.loc[
        result["org_code"].eq("AAA")
    ].iloc[0]

    assert bool(provider_aaa["provider_name_changed"])
    assert provider_aaa["latest_org_name"] == (
        "Provider AAA Renamed"
    )


def test_zero_comparison_volume_returns_missing_rate() -> None:
    """Zero comparison volume must not create infinite change."""
    data = make_provider_change_data()
    data.loc[
        data["org_code"].eq("BBB")
        & data["reporting_month"].eq(
            pd.Timestamp("2025-09-01")
        ),
        "total_attendances",
    ] = 0

    result = compare_provider_periods(
        data,
        current_month="2026-09-01",
        comparison_month="2025-09-01",
        minimum_attendance_volume=0,
        full_period_months=2,
    )

    provider_bbb = result.loc[
        result["org_code"].eq("BBB")
    ].iloc[0]

    assert pd.isna(
        provider_bbb["attendance_percentage_change"]
    )


def test_rejects_duplicate_provider_month_keys() -> None:
    """Duplicate provider-month keys must fail."""
    data = make_provider_change_data()
    data = pd.concat(
        [data, data.iloc[[0]]],
        ignore_index=True,
    )

    with pytest.raises(
        ValueError,
        match="Duplicate provider-month keys",
    ):
        compare_provider_periods(
            data,
            current_month="2026-09-01",
            comparison_month="2025-09-01",
        )


def test_rejects_negative_volume_threshold() -> None:
    """Negative minimum-volume thresholds must fail."""
    with pytest.raises(
        ValueError,
        match="cannot be negative",
    ):
        compare_provider_periods(
            make_provider_change_data(),
            current_month="2026-09-01",
            comparison_month="2025-09-01",
            minimum_attendance_volume=-1,
        )
