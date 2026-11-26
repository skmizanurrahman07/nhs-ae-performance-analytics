"""Volume-controlled provider change analysis."""

from typing import Final

import pandas as pd

REQUIRED_COLUMNS: Final[tuple[str, ...]] = (
    "reporting_month",
    "org_code",
    "org_name",
    "total_attendances",
    "emergency_admissions",
)


def compare_provider_periods(
    data: pd.DataFrame,
    *,
    current_month: str,
    comparison_month: str,
    minimum_attendance_volume: int = 10_000,
    full_period_months: int = 25,
) -> pd.DataFrame:
    """Compare provider KPIs between two specified months."""
    if minimum_attendance_volume < 0:
        raise ValueError(
            "Minimum attendance volume cannot be negative."
        )

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            "Required provider comparison columns are missing: "
            f"{missing_columns}"
        )

    working = data.copy()
    working["reporting_month"] = pd.to_datetime(
        working["reporting_month"]
    )

    current_timestamp = pd.Timestamp(current_month)
    comparison_timestamp = pd.Timestamp(comparison_month)

    if current_timestamp == comparison_timestamp:
        raise ValueError(
            "Current and comparison months must be different."
        )

    duplicate_keys = working.duplicated(
        subset=["reporting_month", "org_code"],
        keep=False,
    )

    if duplicate_keys.any():
        raise ValueError(
            "Duplicate provider-month keys prevent comparison."
        )

    ordered = working.sort_values(
        ["org_code", "reporting_month"],
        kind="stable",
    )

    metadata = (
        ordered.groupby(
            "org_code",
            as_index=False,
        )
        .agg(
            latest_org_name=("org_name", "last"),
            months_present=("reporting_month", "nunique"),
            organisation_name_count=("org_name", "nunique"),
        )
    )

    current = (
        ordered.loc[
            ordered["reporting_month"].eq(current_timestamp),
            [
                "org_code",
                "total_attendances",
                "emergency_admissions",
            ],
        ]
        .rename(
            columns={
                "total_attendances": "current_attendances",
                "emergency_admissions": "current_admissions",
            }
        )
    )

    comparison = (
        ordered.loc[
            ordered["reporting_month"].eq(
                comparison_timestamp
            ),
            [
                "org_code",
                "total_attendances",
                "emergency_admissions",
            ],
        ]
        .rename(
            columns={
                "total_attendances": "comparison_attendances",
                "emergency_admissions": "comparison_admissions",
            }
        )
    )

    result = current.merge(
        comparison,
        on="org_code",
        how="inner",
        validate="one_to_one",
    ).merge(
        metadata,
        on="org_code",
        how="left",
        validate="one_to_one",
    )

    result["attendance_absolute_change"] = (
        result["current_attendances"]
        - result["comparison_attendances"]
    )

    result["admission_absolute_change"] = (
        result["current_admissions"]
        - result["comparison_admissions"]
    )

    result["attendance_percentage_change"] = (
        result["attendance_absolute_change"]
        .div(
            result["comparison_attendances"].where(
                result["comparison_attendances"].ne(0)
            )
        )
    )

    result["admission_percentage_change"] = (
        result["admission_absolute_change"]
        .div(
            result["comparison_admissions"].where(
                result["comparison_admissions"].ne(0)
            )
        )
    )

    result["meets_volume_threshold"] = (
        result[
            [
                "current_attendances",
                "comparison_attendances",
            ]
        ]
        .min(axis=1)
        .ge(minimum_attendance_volume)
    )

    result["full_period_coverage"] = (
        result["months_present"].eq(full_period_months)
    )

    result["provider_name_changed"] = (
        result["organisation_name_count"].gt(1)
    )

    result["analysis_eligible"] = (
        result["meets_volume_threshold"]
        & result["full_period_coverage"]
    )

    return result.sort_values(
        [
            "analysis_eligible",
            "attendance_absolute_change",
        ],
        ascending=[
            False,
            False,
        ],
        kind="stable",
    ).reset_index(drop=True)
