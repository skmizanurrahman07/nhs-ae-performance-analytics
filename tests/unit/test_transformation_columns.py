"""Tests for controlled analytical column mappings."""

from nhs_ae.transformation.columns import (
    COLUMN_RENAME_MAP,
    STANDARD_MEASURE_COLUMNS,
)
from nhs_ae.validation.schema import (
    MEASURE_COLUMNS,
    REQUIRED_COLUMNS,
)


def test_column_mapping_covers_source_schema() -> None:
    """Every required raw source column must have a mapping."""
    assert tuple(COLUMN_RENAME_MAP) == REQUIRED_COLUMNS


def test_column_mapping_contains_22_fields() -> None:
    """Mapping must cover all 22 controlled source fields."""
    assert len(COLUMN_RENAME_MAP) == 22


def test_standard_measure_columns_contains_18_fields() -> None:
    """Standardised measure collection must contain 18 measures."""
    assert len(STANDARD_MEASURE_COLUMNS) == 18


def test_standard_measure_columns_match_source_measures() -> None:
    """Each source measure must map to its standardised name."""
    expected = tuple(
        COLUMN_RENAME_MAP[column]
        for column in MEASURE_COLUMNS
    )

    assert expected == STANDARD_MEASURE_COLUMNS


def test_standardised_column_names_are_unique() -> None:
    """Analytical column names must not contain duplicates."""
    names = tuple(COLUMN_RENAME_MAP.values())

    assert len(names) == len(set(names))
