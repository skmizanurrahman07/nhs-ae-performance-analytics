"""Reusable validation primitives for healthcare aggregate data."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Final


class Severity(StrEnum):
    """Severity level assigned to a data-quality rule."""

    CRITICAL = "critical"
    WARNING = "warning"
    INFORMATION = "information"


@dataclass(frozen=True, slots=True)
class ValidationRule:
    """Metadata describing a controlled data-quality rule."""

    identifier: str
    name: str
    description: str
    severity: Severity

    def __post_init__(self) -> None:
        """Enforce the controlled rule identifier format."""
        if not self.identifier.startswith("DQ-"):
            msg = "Validation rule identifier must start with 'DQ-'."
            raise ValueError(msg)


CORE_RULES: Final[tuple[ValidationRule, ...]] = (
    ValidationRule(
        identifier="DQ-001",
        name="Required fields",
        description="All required source fields are present.",
        severity=Severity.CRITICAL,
    ),
    ValidationRule(
    identifier="DQ-002",
    name="Unique provider-period business key",
    description=(
        "Provider records are unique by Period and Org Code."
    ),
    severity=Severity.CRITICAL,
    ),

    ValidationRule(
        identifier="DQ-003",
        name="Non-negative counts",
        description="Published activity counts are not negative.",
        severity=Severity.CRITICAL,
    ),
    ValidationRule(
        identifier="DQ-004",
        name="Complete monthly series",
        description="Expected reporting months are represented.",
        severity=Severity.WARNING,
    ),
        ValidationRule(
        identifier="DQ-005",
        name="Published total control",
        description=(
            "Exactly one published TOTAL control record is present."
        ),
        severity=Severity.CRITICAL,
    ),
    ValidationRule(
        identifier="DQ-006",
        name="Published total reconciliation",
        description=(
            "Provider-level measure sums reconcile with the "
            "published TOTAL control record."
        ),
        severity=Severity.CRITICAL,
    ),
    ValidationRule(
        identifier="DQ-007",
        name="Identifier completeness",
        description=(
            "Provider identifiers contain no null, blank, or "
            "whitespace-only values."
        ),
        severity=Severity.CRITICAL,
    ),
    ValidationRule(
        identifier="DQ-008",
        name="Identifier whitespace",
        description=(
            "Provider identifiers contain no unexpected surrounding "
            "whitespace after controlled transformation."
        ),
        severity=Severity.WARNING,
    ),
    ValidationRule(
        identifier="DQ-009",
        name="Organisation mapping consistency",
        description=(
            "Provider organisation codes, names, and parent organisations "
            "have internally consistent mappings within a reporting period."
        ),
        severity=Severity.CRITICAL,
    ),
    ValidationRule(
        identifier="DQ-010",
        name="Four-hour breach compatibility",
        description=(
            "Four-hour breach counts do not exceed their compatible "
            "attendance counts."
        ),
        severity=Severity.CRITICAL,
    ),
)
