"""Tests for the monthly NHS A&E schema contract."""

from nhs_ae.validation.schema import (
    IDENTIFIER_COLUMNS,
    MEASURE_COLUMNS,
    PROVIDER_KEY_COLUMNS,
    REQUIRED_COLUMNS,
    TOTAL_VALUE,
    find_missing_columns,
    find_unexpected_columns,
    has_expected_column_order,
)


def test_schema_contains_expected_column_groups() -> None:
    """Schema must contain 4 identifiers and 18 measures."""
    assert len(IDENTIFIER_COLUMNS) == 4
    assert len(MEASURE_COLUMNS) == 18
    assert len(REQUIRED_COLUMNS) == 22


def test_provider_key_contains_period_and_org_code() -> None:
    """Provider business key must use period and organisation."""
    assert PROVIDER_KEY_COLUMNS == (
        "Period",
        "Org Code",
    )


def test_total_control_value_is_defined() -> None:
    """Published control records must use the TOTAL marker."""
    assert TOTAL_VALUE == "TOTAL"


def test_complete_schema_has_no_missing_columns() -> None:
    """Complete source schema must report no missing fields."""
    columns = list(REQUIRED_COLUMNS)

    assert find_missing_columns(columns) == ()


def test_missing_column_is_detected() -> None:
    """A missing required field must be identified."""
    columns = list(REQUIRED_COLUMNS)
    missing_column = columns.pop()

    assert find_missing_columns(columns) == (missing_column,)


def test_unexpected_column_is_detected() -> None:
    """An additional source field must be identified."""
    columns = [
        *REQUIRED_COLUMNS,
        "Unexpected NHS Field",
    ]

    assert find_unexpected_columns(columns) == ("Unexpected NHS Field",)


def test_expected_column_order_passes() -> None:
    """Original source column order must satisfy contract."""
    columns = list(REQUIRED_COLUMNS)

    assert has_expected_column_order(columns)


def test_changed_column_order_fails() -> None:
    """Reordered source fields must be detectable."""
    columns = list(REQUIRED_COLUMNS)
    columns[0], columns[1] = columns[1], columns[0]

    assert not has_expected_column_order(columns)
