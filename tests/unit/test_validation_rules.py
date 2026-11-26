"""Tests for data-quality rule metadata."""

import pytest

from nhs_ae.validation.rules import (
    CORE_RULES,
    Severity,
    ValidationRule,
)


def test_validation_rule_identifiers_are_unique() -> None:
    """Data-quality identifiers must remain unique."""
    identifiers = [rule.identifier for rule in CORE_RULES]

    assert len(identifiers) == len(set(identifiers))


def test_core_rules_have_expected_identifiers() -> None:
    """Core data-quality catalogue must contain DQ-001 to DQ-010."""
    identifiers = tuple(rule.identifier for rule in CORE_RULES)

    assert identifiers == tuple(
        f"DQ-{number:03d}"
        for number in range(1, 11)
    )


def test_validation_rule_requires_dq_prefix() -> None:
    """Rule identifiers outside the controlled DQ format must fail."""
    with pytest.raises(
        ValueError,
        match="must start with 'DQ-'",
    ):
        ValidationRule(
            identifier="INVALID-001",
            name="Invalid rule",
            description="Test invalid rule identifier.",
            severity=Severity.CRITICAL,
        )


def test_core_rules_have_non_empty_metadata() -> None:
    """Every controlled rule must have usable metadata."""
    for rule in CORE_RULES:
        assert rule.name.strip()
        assert rule.description.strip()


def test_core_rules_use_controlled_severity() -> None:
    """Every core rule must use the controlled severity enumeration."""
    for rule in CORE_RULES:
        assert isinstance(rule.severity, Severity)


def test_critical_single_source_rules_have_expected_severity() -> None:
    """Critical single-source controls must remain blocking rules."""
    critical_identifiers = {
        "DQ-001",
        "DQ-002",
        "DQ-003",
        "DQ-005",
        "DQ-006",
        "DQ-007",
        "DQ-009",
        "DQ-010",
    }

    actual = {
        rule.identifier
        for rule in CORE_RULES
        if rule.severity is Severity.CRITICAL
    }

    assert critical_identifiers <= actual


def test_warning_rules_have_expected_severity() -> None:
    """Known warning-level controls must remain warnings."""
    severity_by_identifier = {
        rule.identifier: rule.severity
        for rule in CORE_RULES
    }

    assert severity_by_identifier["DQ-004"] is Severity.WARNING
    assert severity_by_identifier["DQ-008"] is Severity.WARNING
