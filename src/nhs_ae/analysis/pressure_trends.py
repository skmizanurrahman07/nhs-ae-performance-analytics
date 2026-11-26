"""Monthly trend analysis for A&E pressure and patient-flow measures."""

from typing import Final

import pandas as pd

PRESSURE_COLUMNS: Final[tuple[str, ...]] = (
    "four_hour_breaches",
    "dta_waits_4_12hrs",
    "dta_waits_12plus_hrs",
    "total_dta_waits_4plus_hrs",
)


def build_monthly_pressure_trends(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate pressure and flow measures by reporting month."""
    required_columns = (
        "reporting_month",
        *PRESSURE_COLUMNS,
    )

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            "Required pressure trend columns are missing: "
            f"{missing_columns}"
        )

    result = (
        data.groupby(
            "reporting_month",
            as_index=False,
        )
        .agg(
            four_hour_breaches=(
                "four_hour_breaches",
                "sum",
            ),
            dta_waits_4_12hrs=(
                "dta_waits_4_12hrs",
                "sum",
            ),
            dta_waits_12plus_hrs=(
                "dta_waits_12plus_hrs",
                "sum",
            ),
            total_dta_waits_4plus_hrs=(
                "total_dta_waits_4plus_hrs",
                "sum",
            ),
        )
        .sort_values("reporting_month")
        .reset_index(drop=True)
    )

    for column in PRESSURE_COLUMNS:
        result[f"{column}_monthly_change"] = (
            result[column].pct_change()
        )

        result[f"{column}_year_on_year_change"] = (
            result[column].pct_change(periods=12)
        )

    return result
