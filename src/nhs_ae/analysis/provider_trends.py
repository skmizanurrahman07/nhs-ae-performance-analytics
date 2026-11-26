"""Provider-level trend analysis for approved NHS A&E KPIs."""

from typing import Final

import pandas as pd

PROVIDER_TREND_COLUMNS: Final[tuple[str, ...]] = (
    "reporting_month",
    "org_code",
    "org_name",
    "total_attendances",
    "emergency_admissions",
)


def build_provider_kpi_trends(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Build monthly approved KPI trends by provider code."""
    missing_columns = [
        column
        for column in PROVIDER_TREND_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            "Required provider KPI columns are missing: "
            f"{missing_columns}"
        )

    result = (
        data.loc[:, list(PROVIDER_TREND_COLUMNS)]
        .sort_values(
            [
                "org_code",
                "reporting_month",
            ],
            kind="stable",
        )
        .reset_index(drop=True)
    )

    result["attendance_monthly_change"] = (
        result.groupby("org_code")[
            "total_attendances"
        ].pct_change()
    )

    result["admission_monthly_change"] = (
        result.groupby("org_code")[
            "emergency_admissions"
        ].pct_change()
    )

    result["attendance_year_on_year_change"] = (
        result.groupby("org_code")[
            "total_attendances"
        ].pct_change(periods=12)
    )

    result["admission_year_on_year_change"] = (
        result.groupby("org_code")[
            "emergency_admissions"
        ].pct_change(periods=12)
    )

    return result


def summarise_provider_kpis(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Summarise approved KPI volume and coverage by provider."""
    required_columns = (
        "reporting_month",
        "org_code",
        "org_name",
        "total_attendances",
        "emergency_admissions",
    )

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            "Required provider KPI columns are missing: "
            f"{missing_columns}"
        )

    ordered = data.sort_values(
        [
            "org_code",
            "reporting_month",
        ],
        kind="stable",
    )

    result = (
        ordered.groupby(
            "org_code",
            as_index=False,
        )
        .agg(
            latest_org_name=(
                "org_name",
                "last",
            ),
            months_present=(
                "reporting_month",
                "nunique",
            ),
            total_attendances=(
                "total_attendances",
                "sum",
            ),
            average_monthly_attendances=(
                "total_attendances",
                "mean",
            ),
            emergency_admissions=(
                "emergency_admissions",
                "sum",
            ),
            average_monthly_admissions=(
                "emergency_admissions",
                "mean",
            ),
        )
        .sort_values(
            "total_attendances",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    return result
