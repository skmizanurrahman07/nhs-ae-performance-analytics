"""Tests for provider-level approved KPI trend analysis."""

import pandas as pd
import pytest

from nhs_ae.analysis.provider_trends import (
    build_provider_kpi_trends,
    summarise_provider_kpis,
)


def make_provider_kpi_data() -> pd.DataFrame:
    """Create representative multi-provider KPI data."""
    return pd.DataFrame(
        {
            "reporting_month": pd.to_datetime(
                [
                    "2024-09-01",
                    "2024-10-01",
                    "2024-09-01",
                    "2024-10-01",
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
                100,
                110,
                200,
                180,
            ],
            "emergency_admissions": [
                20,
                22,
                40,
                36,
            ],
        }
    )


def test_builds_provider_monthly_changes() -> None:
    """Provider trends must calculate changes within provider."""
    result = build_provider_kpi_trends(
        make_provider_kpi_data()
    )

    provider_aaa = result.loc[
        result["org_code"].eq("AAA")
    ].reset_index(drop=True)

    provider_bbb = result.loc[
        result["org_code"].eq("BBB")
    ].reset_index(drop=True)

    assert pd.isna(
        provider_aaa.iloc[0]["attendance_monthly_change"]
    )

    assert provider_aaa.iloc[1][
        "attendance_monthly_change"
    ] == pytest.approx(0.10)

    assert provider_aaa.iloc[1][
        "admission_monthly_change"
    ] == pytest.approx(0.10)

    assert provider_bbb.iloc[1][
        "attendance_monthly_change"
    ] == pytest.approx(-0.10)


def test_provider_change_does_not_cross_provider_boundary() -> None:
    """Percentage changes must reset for each provider."""
    result = build_provider_kpi_trends(
        make_provider_kpi_data()
    )

    first_records = (
        result.groupby("org_code")
        .head(1)
    )

    assert first_records[
        "attendance_monthly_change"
    ].isna().all()

    assert first_records[
        "admission_monthly_change"
    ].isna().all()


def test_summarises_provider_kpis() -> None:
    """Provider summary must aggregate approved KPI values."""
    result = summarise_provider_kpis(
        make_provider_kpi_data()
    )

    provider_aaa = result.loc[
        result["org_code"].eq("AAA")
    ].iloc[0]

    assert provider_aaa["months_present"] == 2
    assert provider_aaa["total_attendances"] == 210
    assert provider_aaa["emergency_admissions"] == 42
    assert provider_aaa[
        "average_monthly_attendances"
    ] == pytest.approx(105)
    assert provider_aaa[
        "average_monthly_admissions"
    ] == pytest.approx(21)


def test_summary_uses_latest_provider_name() -> None:
    """Provider summary must retain the latest organisation name."""
    result = summarise_provider_kpis(
        make_provider_kpi_data()
    )

    provider_aaa = result.loc[
        result["org_code"].eq("AAA")
    ].iloc[0]

    assert provider_aaa["latest_org_name"] == (
        "Provider AAA Renamed"
    )


def test_provider_trends_reject_missing_columns() -> None:
    """Missing controlled KPI columns must fail."""
    data = make_provider_kpi_data().drop(
        columns=["total_attendances"]
    )

    with pytest.raises(
        ValueError,
        match="Required provider KPI columns are missing",
    ):
        build_provider_kpi_trends(data)


def test_provider_summary_rejects_missing_columns() -> None:
    """Provider summary must reject incomplete KPI data."""
    data = make_provider_kpi_data().drop(
        columns=["emergency_admissions"]
    )

    with pytest.raises(
        ValueError,
        match="Required provider KPI columns are missing",
    ):
        summarise_provider_kpis(data)
