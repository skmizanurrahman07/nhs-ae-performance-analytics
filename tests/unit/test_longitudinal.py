"""Tests for longitudinal analytical-data profiling."""

import pandas as pd

from nhs_ae.validation.longitudinal import (
    build_longitudinal_profile,
    monthly_provider_counts,
    provider_month_coverage,
)

MEASURE_COLUMNS = (
    "measure_1",
    "measure_2",
)


def make_longitudinal_data() -> pd.DataFrame:
    """Create representative multi-month provider data."""
    return pd.DataFrame(
        {
            "reporting_month": pd.to_datetime(
                [
                    "2024-09-01",
                    "2024-09-01",
                    "2024-10-01",
                    "2024-10-01",
                    "2024-11-01",
                ]
            ),
            "org_code": [
                "AAA",
                "BBB",
                "AAA",
                "BBB",
                "AAA",
            ],
            "org_name": [
                "Provider AAA",
                "Provider BBB",
                "Provider AAA",
                "Provider BBB",
                "Provider AAA",
            ],
            "measure_1": [
                10,
                20,
                11,
                21,
                12,
            ],
            "measure_2": [
                1,
                2,
                1,
                2,
                1,
            ],
        }
    )


def test_build_longitudinal_profile() -> None:
    """Profile must report expected longitudinal properties."""
    result = build_longitudinal_profile(
        make_longitudinal_data(),
        MEASURE_COLUMNS,
    )

    assert result.row_count == 5
    assert result.column_count == 5
    assert result.month_count == 3
    assert result.provider_count == 2
    assert result.duplicate_provider_month_count == 0
    assert result.missing_value_count == 0
    assert result.negative_measure_count == 0


def test_longitudinal_profile_detects_duplicate_key() -> None:
    """Duplicate provider-month records must be counted."""
    data = make_longitudinal_data()

    duplicate = data.iloc[[0]].copy()
    data = pd.concat(
        [data, duplicate],
        ignore_index=True,
    )

    result = build_longitudinal_profile(
        data,
        MEASURE_COLUMNS,
    )

    assert result.duplicate_provider_month_count == 1


def test_longitudinal_profile_detects_negative_measure() -> None:
    """Negative analytical measures must be counted."""
    data = make_longitudinal_data()
    data.loc[0, "measure_1"] = -1

    result = build_longitudinal_profile(
        data,
        MEASURE_COLUMNS,
    )

    assert result.negative_measure_count == 1


def test_monthly_provider_counts() -> None:
    """Monthly output must report records and unique providers."""
    result = monthly_provider_counts(
        make_longitudinal_data()
    )

    assert len(result) == 3
    assert result["provider_count"].tolist() == [2, 2, 1]
    assert result["record_count"].tolist() == [2, 2, 1]


def test_provider_month_coverage() -> None:
    """Provider coverage must summarise presence by organisation code."""
    result = provider_month_coverage(
        make_longitudinal_data()
    )

    provider_aaa = result.loc[
        result["org_code"].eq("AAA")
    ].iloc[0]

    provider_bbb = result.loc[
        result["org_code"].eq("BBB")
    ].iloc[0]

    assert provider_aaa["months_present"] == 3
    assert provider_aaa["first_month"] == pd.Timestamp(
        "2024-09-01"
    )
    assert provider_aaa["last_month"] == pd.Timestamp(
        "2024-11-01"
    )
    assert provider_aaa["organisation_name_count"] == 1
    assert provider_aaa["latest_org_name"] == "Provider AAA"

    assert provider_bbb["months_present"] == 2

def test_provider_coverage_consolidates_name_changes() -> None:
    """Name changes must not split one organisation code."""
    data = make_longitudinal_data()

    data.loc[
        data["org_code"].eq("AAA")
        & data["reporting_month"].eq(
            pd.Timestamp("2024-11-01")
        ),
        "org_name",
    ] = "Renamed Provider AAA"

    result = provider_month_coverage(data)

    provider_aaa = result.loc[
        result["org_code"].eq("AAA")
    ].iloc[0]

    assert len(result) == 2
    assert provider_aaa["months_present"] == 3
    assert provider_aaa["organisation_name_count"] == 2
    assert provider_aaa["latest_org_name"] == (
        "Renamed Provider AAA"
    )
