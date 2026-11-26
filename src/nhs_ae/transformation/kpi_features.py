"""Derive approved analytical KPI features from provider measures."""

from typing import Final

import pandas as pd

ATTENDANCE_COLUMNS: Final[tuple[str, ...]] = (
    "ae_attendances_type1",
    "ae_attendances_type2",
    "ae_attendances_other",
    "ae_booked_attendances_type1",
    "ae_booked_attendances_type2",
    "ae_booked_attendances_other",
)

EMERGENCY_ADMISSION_COLUMNS: Final[tuple[str, ...]] = (
    "emergency_admissions_ae_type1",
    "emergency_admissions_ae_type2",
    "emergency_admissions_ae_other",
    "other_emergency_admissions",
)


def derive_approved_kpis(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Add approved KPI-001 and KPI-002 values."""
    result = data.copy()

    required_columns = (
        *ATTENDANCE_COLUMNS,
        *EMERGENCY_ADMISSION_COLUMNS,
    )

    missing_columns = [
        column
        for column in required_columns
        if column not in result.columns
    ]

    if missing_columns:
        raise ValueError(
            "Required KPI source columns are missing: "
            f"{missing_columns}"
        )

    result["total_attendances"] = result.loc[
        :,
        list(ATTENDANCE_COLUMNS),
    ].sum(axis=1)

    result["emergency_admissions"] = result.loc[
        :,
        list(EMERGENCY_ADMISSION_COLUMNS),
    ].sum(axis=1)

    return result
