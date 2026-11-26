"""Provider-level pressure and patient-flow analysis."""

from typing import Final

import pandas as pd

REQUIRED_COLUMNS: Final[tuple[str, ...]] = (
    "reporting_month",
    "org_code",
    "org_name",
    "total_attendances",
    "emergency_admissions",
    "four_hour_breaches",
    "dta_waits_4_12hrs",
    "dta_waits_12plus_hrs",
    "total_dta_waits_4plus_hrs",
)


def compare_provider_pressure(
    data: pd.DataFrame,
    *,
    current_month: str,
    comparison_month: str,
    minimum_attendance_volume: int = 10_000,
    minimum_admission_volume: int = 1_000,
    full_period_months: int = 25,
) -> pd.DataFrame:
    """Compare provider pressure measures between two months."""
    if minimum_attendance_volume < 0:
        raise ValueError(
            "Minimum attendance volume cannot be negative."
        )

    if minimum_admission_volume < 0:
        raise ValueError(
            "Minimum admission volume cannot be negative."
        )

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            "Required provider pressure columns are missing: "
            f"{missing_columns}"
        )

    working = data.copy()
    working["reporting_month"] = pd.to_datetime(
        working["reporting_month"]
    )

    duplicate_keys = working.duplicated(
        subset=["reporting_month", "org_code"],
        keep=False,
    )

    if duplicate_keys.any():
        raise ValueError(
            "Duplicate provider-month keys prevent comparison."
        )

    current_timestamp = pd.Timestamp(current_month)
    comparison_timestamp = pd.Timestamp(comparison_month)

    if current_timestamp == comparison_timestamp:
        raise ValueError(
            "Current and comparison months must be different."
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

    measure_columns = [
        "total_attendances",
        "emergency_admissions",
        "four_hour_breaches",
        "dta_waits_4_12hrs",
        "dta_waits_12plus_hrs",
        "total_dta_waits_4plus_hrs",
    ]

    current = ordered.loc[
        ordered["reporting_month"].eq(current_timestamp),
        ["org_code", *measure_columns],
    ].copy()

    comparison = ordered.loc[
        ordered["reporting_month"].eq(
            comparison_timestamp
        ),
        ["org_code", *measure_columns],
    ].copy()

    current = current.rename(
        columns={
            column: f"current_{column}"
            for column in measure_columns
        }
    )

    comparison = comparison.rename(
        columns={
            column: f"comparison_{column}"
            for column in measure_columns
        }
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

    pressure_measures = (
        "four_hour_breaches",
        "dta_waits_4_12hrs",
        "dta_waits_12plus_hrs",
        "total_dta_waits_4plus_hrs",
    )

    for measure in pressure_measures:
        current_column = f"current_{measure}"
        comparison_column = f"comparison_{measure}"

        result[f"{measure}_absolute_change"] = (
            result[current_column]
            - result[comparison_column]
        )

        denominator = result[
            comparison_column
        ].where(
            result[comparison_column].ne(0)
        )

        result[f"{measure}_percentage_change"] = (
            result[
                f"{measure}_absolute_change"
            ].div(denominator)
        )

    result["meets_attendance_threshold"] = (
        result[
            [
                "current_total_attendances",
                "comparison_total_attendances",
            ]
        ]
        .min(axis=1)
        .ge(minimum_attendance_volume)
    )

    result["meets_admission_threshold"] = (
        result[
            [
                "current_emergency_admissions",
                "comparison_emergency_admissions",
            ]
        ]
        .min(axis=1)
        .ge(minimum_admission_volume)
    )

    result["full_period_coverage"] = (
        result["months_present"].eq(full_period_months)
    )

    result["provider_name_changed"] = (
        result["organisation_name_count"].gt(1)
    )

    result["breach_analysis_eligible"] = (
        result["meets_attendance_threshold"]
        & result["full_period_coverage"]
    )

    result["dta_analysis_eligible"] = (
        result["meets_admission_threshold"]
        & result["full_period_coverage"]
    )

    return result.sort_values(
        "org_code"
    ).reset_index(drop=True)
