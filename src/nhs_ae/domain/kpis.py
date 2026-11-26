"""Canonical KPI specifications for the analytical product."""

from dataclasses import dataclass
from enum import StrEnum


class MetricDirection(StrEnum):
    """Interpretive direction for a metric."""

    CONTEXT = "context"
    HIGHER_IS_BETTER = "higher_is_better"
    LOWER_IS_BETTER = "lower_is_better"


class ApprovalStatus(StrEnum):
    """Governance state of a KPI definition."""

    APPROVED = "approved"
    PROVISIONAL = "provisional"


@dataclass(frozen=True, slots=True)
class KpiSpecification:
    """Business definition of a controlled analytical metric."""

    identifier: str
    name: str
    description: str
    direction: MetricDirection
    status: ApprovalStatus
    numerator: str | None = None
    denominator: str | None = None
    unit: str = "count"

    def __post_init__(self) -> None:
        """Validate required KPI metadata."""
        if not self.identifier.startswith("KPI-"):
            msg = "KPI identifier must start with 'KPI-'."
            raise ValueError(msg)
        if self.denominator and not self.numerator:
            msg = "A denominator requires a numerator."
            raise ValueError(msg)


CORE_KPIS: tuple[KpiSpecification, ...] = (
    KpiSpecification(
        identifier="KPI-001",
        name="Total attendances",
        description="Total eligible A&E attendances in the reporting period.",
        direction=MetricDirection.CONTEXT,
        status=ApprovalStatus.APPROVED,
    ),
    KpiSpecification(
        identifier="KPI-002",
        name="Emergency admissions",
        description="Total eligible emergency admissions in the period.",
        direction=MetricDirection.CONTEXT,
        status=ApprovalStatus.APPROVED,
    ),
    KpiSpecification(
        identifier="KPI-003",
        name="Admission rate",
        description="Emergency admissions divided by eligible attendances.",
        direction=MetricDirection.CONTEXT,
        status=ApprovalStatus.PROVISIONAL,
        numerator="emergency_admissions",
        denominator="eligible_attendances",
        unit="percentage",
    ),
    KpiSpecification(
        identifier="KPI-004",
        name="Four-hour performance",
        description=(
            "Applicable attendances completed within four hours divided by "
            "the confirmed source denominator."
        ),
        direction=MetricDirection.HIGHER_IS_BETTER,
        status=ApprovalStatus.PROVISIONAL,
        numerator="within_four_hours",
        denominator="confirmed_applicable_attendances",
        unit="percentage",
    ),
)


def kpi_by_id(identifier: str) -> KpiSpecification:
    """Return a KPI specification by its controlled identifier.

    Args:
        identifier: Controlled KPI identifier.

    Raises:
        KeyError: If no KPI has the supplied identifier.

    Returns:
        Matching KPI specification.
    """
    for specification in CORE_KPIS:
        if specification.identifier == identifier:
            return specification
    raise KeyError(identifier)
