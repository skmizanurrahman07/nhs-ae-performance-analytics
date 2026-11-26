"""Controlled source-to-analytical column mappings."""

from typing import Final

COLUMN_RENAME_MAP: Final[dict[str, str]] = {
    "Period": "reporting_period_raw",
    "Org Code": "org_code",
    "Parent Org": "parent_org",
    "Org name": "org_name",
    "A&E attendances Type 1": "ae_attendances_type1",
    "A&E attendances Type 2": "ae_attendances_type2",
    "A&E attendances Other A&E Department": "ae_attendances_other",
    "A&E attendances Booked Appointments Type 1": (
        "ae_booked_attendances_type1"
    ),
    "A&E attendances Booked Appointments Type 2": (
        "ae_booked_attendances_type2"
    ),
    "A&E attendances Booked Appointments Other Department": (
        "ae_booked_attendances_other"
    ),
    "Attendances over 4hrs Type 1": "ae_over_4hrs_type1",
    "Attendances over 4hrs Type 2": "ae_over_4hrs_type2",
    "Attendances over 4hrs Other Department": "ae_over_4hrs_other",
    "Attendances over 4hrs Booked Appointments Type 1": (
        "ae_booked_over_4hrs_type1"
    ),
    "Attendances over 4hrs Booked Appointments Type 2": (
        "ae_booked_over_4hrs_type2"
    ),
    "Attendances over 4hrs Booked Appointments Other Department": (
        "ae_booked_over_4hrs_other"
    ),
    "Patients who have waited 4-12 hs from DTA to admission": (
        "dta_wait_4_12hrs"
    ),
    "Patients who have waited 12+ hrs from DTA to admission": (
        "dta_wait_12plus_hrs"
    ),
    "Emergency admissions via A&E - Type 1": (
        "emergency_admissions_ae_type1"
    ),
    "Emergency admissions via A&E - Type 2": (
        "emergency_admissions_ae_type2"
    ),
    "Emergency admissions via A&E - Other A&E department": (
        "emergency_admissions_ae_other"
    ),
    "Other emergency admissions": "other_emergency_admissions",
}


STANDARD_MEASURE_COLUMNS: Final[tuple[str, ...]] = tuple(
    COLUMN_RENAME_MAP[column]
    for column in tuple(COLUMN_RENAME_MAP)[4:]
)
