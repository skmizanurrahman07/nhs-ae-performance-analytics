"""Schema contract for monthly NHS A&E source data."""

from typing import Final

IDENTIFIER_COLUMNS: Final[tuple[str, ...]] = (
    "Period",
    "Org Code",
    "Parent Org",
    "Org name",
)

MEASURE_COLUMNS: Final[tuple[str, ...]] = (
    "A&E attendances Type 1",
    "A&E attendances Type 2",
    "A&E attendances Other A&E Department",
    "A&E attendances Booked Appointments Type 1",
    "A&E attendances Booked Appointments Type 2",
    "A&E attendances Booked Appointments Other Department",
    "Attendances over 4hrs Type 1",
    "Attendances over 4hrs Type 2",
    "Attendances over 4hrs Other Department",
    "Attendances over 4hrs Booked Appointments Type 1",
    "Attendances over 4hrs Booked Appointments Type 2",
    "Attendances over 4hrs Booked Appointments Other Department",
    "Patients who have waited 4-12 hs from DTA to admission",
    "Patients who have waited 12+ hrs from DTA to admission",
    "Emergency admissions via A&E - Type 1",
    "Emergency admissions via A&E - Type 2",
    "Emergency admissions via A&E - Other A&E department",
    "Other emergency admissions",
)

REQUIRED_COLUMNS: Final[tuple[str, ...]] = (
    *IDENTIFIER_COLUMNS,
    *MEASURE_COLUMNS,
)

PROVIDER_KEY_COLUMNS: Final[tuple[str, ...]] = (
    "Period",
    "Org Code",
)

TOTAL_VALUE: Final[str] = "TOTAL"


def find_missing_columns(columns: list[str]) -> tuple[str, ...]:
    """Return required columns absent from the source.

    Args:
        columns: Column names found in the source dataset.

    Returns:
        Required columns that are missing from the source.
    """
    available = set(columns)

    return tuple(column for column in REQUIRED_COLUMNS if column not in available)


def find_unexpected_columns(
    columns: list[str],
) -> tuple[str, ...]:
    """Return source columns absent from the schema contract.

    Args:
        columns: Column names found in the source dataset.

    Returns:
        Columns that are not part of the expected schema.
    """
    expected = set(REQUIRED_COLUMNS)

    return tuple(column for column in columns if column not in expected)


def has_expected_column_order(columns: list[str]) -> bool:
    """Return whether source columns exactly match expected order."""
    return tuple(columns) == REQUIRED_COLUMNS
