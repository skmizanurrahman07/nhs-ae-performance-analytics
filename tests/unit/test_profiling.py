"""Tests for reusable NHS A&E source profiling."""

import pandas as pd
import pytest

from nhs_ae.validation.profiling import (
    build_source_profile,
    profile_identifier_integrity,
    profile_organisation_mappings,
    provider_records,
    reconcile_published_totals,
    total_records,
    validate_four_hour_breach_compatibility,
)
from nhs_ae.validation.schema import (
    IDENTIFIER_COLUMNS,
    MEASURE_COLUMNS,
)


def make_test_data() -> pd.DataFrame:
    """Create a minimal representative monthly A&E dataset."""
    rows: list[dict[str, object]] = []

    for period, code, multiplier in (
        ("MSitAE-SEPTEMBER-2026", "AAA", 1),
        ("MSitAE-SEPTEMBER-2026", "BBB", 2),
        ("TOTAL", "TOTAL", 3),
    ):
        row: dict[str, object] = {
            "Period": period,
            "Org Code": code,
            "Parent Org": ("TOTAL" if code == "TOTAL" else "NHS ENGLAND TEST REGION"),
            "Org name": ("TOTAL" if code == "TOTAL" else f"Provider {code}"),
        }

        for column in MEASURE_COLUMNS:
            row[column] = multiplier

        rows.append(row)

    return pd.DataFrame(
        rows,
        columns=[
            *IDENTIFIER_COLUMNS,
            *MEASURE_COLUMNS,
        ],
    )


def test_provider_records_exclude_total() -> None:
    """Provider selection must exclude the TOTAL control row."""
    data = make_test_data()

    providers = provider_records(data)

    assert len(providers) == 2
    assert "TOTAL" not in providers["Period"].values


def test_total_records_select_published_total() -> None:
    """TOTAL selection must return the published control row."""
    data = make_test_data()

    totals = total_records(data)

    assert len(totals) == 1
    assert totals.iloc[0]["Org Code"] == "TOTAL"


def test_source_profile_reports_expected_counts() -> None:
    """Profile must report core structural quality measures."""
    profile = build_source_profile(make_test_data())

    assert profile.row_count == 3
    assert profile.column_count == 22
    assert profile.provider_row_count == 2
    assert profile.total_row_count == 1
    assert profile.unique_org_count == 2
    assert profile.missing_value_count == 0
    assert profile.duplicate_provider_key_count == 0
    assert profile.negative_measure_count == 0


def test_published_totals_reconcile() -> None:
    """Provider sums must reconcile to the test TOTAL row."""
    result = reconcile_published_totals(make_test_data())

    assert result["difference"].eq(0).all()
    assert result["reconciled"].all()


def test_reconciliation_requires_one_total_record() -> None:
    """Reconciliation must reject data without one TOTAL row."""
    data = make_test_data()
    data = data.loc[data["Period"].ne("TOTAL")]

    with pytest.raises(
        ValueError,
        match="Expected exactly one published TOTAL record",
    ):
        reconcile_published_totals(data)

def test_identifier_integrity_detects_whitespace() -> None:
    """Identifier profiling must detect surrounding whitespace."""
    data = make_test_data()

    data.loc[
        data["Org Code"].eq("AAA"),
        "Parent Org",
    ] = "NHS ENGLAND TEST REGION "

    result = profile_identifier_integrity(data)

    parent_org = result.loc[
        result["column"].eq("Parent Org")
    ].iloc[0]

    assert parent_org["null_count"] == 0
    assert parent_org["blank_count"] == 0
    assert parent_org["whitespace_only_count"] == 0
    assert parent_org["surrounding_whitespace_count"] == 1

def test_identifier_integrity_detects_blank_value() -> None:
    """Identifier profiling must detect blank provider identifiers."""
    data = make_test_data()

    data.loc[
        data["Org Code"].eq("AAA"),
        "Org name",
    ] = ""

    result = profile_identifier_integrity(data)

    org_name = result.loc[
        result["column"].eq("Org name")
    ].iloc[0]

    assert org_name["blank_count"] == 1

def test_organisation_mappings_are_consistent() -> None:
    """Consistent provider mappings must report no exceptions."""
    result = profile_organisation_mappings(
        make_test_data()
    )

    assert result["exceptions"].eq(0).all()

def test_organisation_mapping_detects_code_to_name_issue() -> None:
    """One organisation code mapping to multiple names must be detected."""
    data = make_test_data()

    duplicate = data.loc[
        data["Org Code"].eq("AAA")
    ].copy()

    duplicate.loc[:, "Org name"] = (
        "Different Provider Name"
    )

    data = pd.concat(
        [
            data,
            duplicate,
        ],
        ignore_index=True,
    )

    result = profile_organisation_mappings(data)

    exceptions = result.loc[
        result["check"].eq(
            "Org Code maps to multiple Org names"
        ),
        "exceptions",
    ].iloc[0]

    assert exceptions == 1

def test_parent_org_mapping_ignores_surrounding_whitespace() -> None:
    """Controlled whitespace must not create false parent mappings."""
    data = make_test_data()

    duplicate = data.loc[
        data["Org Code"].eq("AAA")
    ].copy()

    duplicate.loc[:, "Parent Org"] = (
        "NHS ENGLAND TEST REGION "
    )

    data = pd.concat(
        [
            data,
            duplicate,
        ],
        ignore_index=True,
    )

    result = profile_organisation_mappings(data)

    exceptions = result.loc[
        result["check"].eq(
            "Org Code maps to multiple Parent Orgs"
        ),
        "exceptions",
    ].iloc[0]

    assert exceptions == 0

def test_four_hour_breaches_are_compatible() -> None:
    """Breaches within attendance counts must pass."""
    data = make_test_data()

    result = validate_four_hour_breach_compatibility(data)

    assert result["invalid_record_count"].eq(0).all()
    assert result["passed"].all()

def test_four_hour_breach_exceeding_attendance_is_detected() -> None:
    """A breach count above attendance count must fail."""
    data = make_test_data()

    data.loc[
        data["Org Code"].eq("AAA"),
        "A&E attendances Type 1",
    ] = 1

    data.loc[
        data["Org Code"].eq("AAA"),
        "Attendances over 4hrs Type 1",
    ] = 2

    result = validate_four_hour_breach_compatibility(data)

    type1 = result.loc[
        result["category"].eq("Type 1")
    ].iloc[0]

    assert type1["invalid_record_count"] == 1
    assert not bool(type1["passed"])

def test_total_record_detection_is_case_insensitive() -> None:
    """Published TOTAL identification must support historical casing."""
    data = pd.DataFrame(
        {
            "Period": [
                "MSitAE-SEPTEMBER-2024",
                "Total",
                "TOTAL",
            ],
            "Org Code": [
                "AAA",
                "Total",
                "TOTAL",
            ],
            "Parent Org": [
                "NHS ENGLAND TEST REGION",
                "Total",
                "TOTAL",
            ],
            "Org name": [
                "Provider AAA",
                "Total",
                "TOTAL",
            ],
        }
    )

    providers = provider_records(data)
    totals = total_records(data)

    assert len(providers) == 1
    assert len(totals) == 2
    assert providers.iloc[0]["Period"] == "MSitAE-SEPTEMBER-2024"


def test_total_record_detection_when_period_is_not_total() -> None:
    """TOTAL identifiers must identify the published control row."""
    data = pd.DataFrame(
        {
            "Period": [
                "MSitAE-FEBRUARY-2026",
                "MSitAE-FEBRUARY-2026",
            ],
            "Org Code": [
                "AAA",
                "TOTAL",
            ],
            "Parent Org": [
                "NHS ENGLAND TEST REGION",
                "TOTAL",
            ],
            "Org name": [
                "Provider AAA",
                "TOTAL",
            ],
        }
    )

    providers = provider_records(data)
    totals = total_records(data)

    assert len(providers) == 1
    assert len(totals) == 1
    assert providers.iloc[0]["Org Code"] == "AAA"
    assert totals.iloc[0]["Org Code"] == "TOTAL"
