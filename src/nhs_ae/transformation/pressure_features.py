"""Derive A&E pressure and patient-flow indicators."""

from typing import Final

import pandas as pd

FOUR_HOUR_BREACH_COLUMNS: Final[tuple[str, ...]] = (
    "ae_over_4hrs_type1",
    "ae_over_4hrs_type2",
    "ae_over_4hrs_other",
    "ae_booked_over_4hrs_type1",
    "ae_booked_over_4hrs_type2",
    "ae_booked_over_4hrs_other",
)

DTA_WAIT_COLUMNS: Final[tuple[str, ...]] = (
    "dta_wait_4_12hrs",
    "dta_wait_12plus_hrs",
)


def derive_pressure_features(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Add controlled pressure and patient-flow measures."""
    result = data.copy()

    required_columns = (
        *FOUR_HOUR_BREACH_COLUMNS,
        *DTA_WAIT_COLUMNS,
    )

    missing_columns = [
        column
        for column in required_columns
        if column not in result.columns
    ]

    if missing_columns:
        raise ValueError(
            "Required pressure source columns are missing: "
            f"{missing_columns}"
        )

    numeric_values = result.loc[
        :,
        list(required_columns),
    ]

    if numeric_values.isna().any().any():
        raise ValueError(
            "Pressure source columns contain missing values."
        )

    if numeric_values.lt(0).any().any():
        raise ValueError(
            "Pressure source columns contain negative values."
        )

    result["four_hour_breaches"] = result.loc[
        :,
        list(FOUR_HOUR_BREACH_COLUMNS),
    ].sum(axis=1)

    result["dta_waits_4_12hrs"] = result[
        "dta_wait_4_12hrs"
    ]

    result["dta_waits_12plus_hrs"] = result[
        "dta_wait_12plus_hrs"
    ]

    result["total_dta_waits_4plus_hrs"] = (
        result["dta_waits_4_12hrs"]
        + result["dta_waits_12plus_hrs"]
    )

    return result
