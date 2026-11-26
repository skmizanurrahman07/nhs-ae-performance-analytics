"""Monthly trend analysis for approved NHS A&E KPIs."""

from typing import Final

import pandas as pd

APPROVED_KPI_COLUMNS: Final[tuple[str, ...]] = (
    "total_attendances",
    "emergency_admissions",
)


def build_monthly_approved_kpis(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate approved KPI values by reporting month."""
    required_columns = (
        "reporting_month",
        *APPROVED_KPI_COLUMNS,
    )

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            "Required monthly KPI columns are missing: "
            f"{missing_columns}"
        )

    result = (
        data.groupby(
            "reporting_month",
            as_index=False,
        )
        .agg(
            total_attendances=(
                "total_attendances",
                "sum",
            ),
            emergency_admissions=(
                "emergency_admissions",
                "sum",
            ),
        )
        .sort_values("reporting_month")
        .reset_index(drop=True)
    )

    result["attendance_monthly_change"] = (
        result["total_attendances"].pct_change()
    )

    result["admission_monthly_change"] = (
        result["emergency_admissions"].pct_change()
    )

    result["attendance_year_on_year_change"] = (
        result["total_attendances"].pct_change(
            periods=12
        )
    )

    result["admission_year_on_year_change"] = (
        result["emergency_admissions"].pct_change(
            periods=12
        )
    )

    return result
