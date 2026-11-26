"""Tests for controlled KPI specifications."""

import pytest

from nhs_ae.domain.kpis import (
    CORE_KPIS,
    ApprovalStatus,
    KpiSpecification,
    MetricDirection,
    kpi_by_id,
)


def test_kpi_identifiers_are_unique() -> None:
    """KPI identifiers must remain unique."""
    identifiers = [item.identifier for item in CORE_KPIS]
    assert len(identifiers) == len(set(identifiers))


def test_kpi_lookup_returns_expected_specification() -> None:
    """A known identifier returns the controlled KPI."""
    assert kpi_by_id("KPI-001").name == "Total attendances"


def test_unknown_kpi_raises_key_error() -> None:
    """Unknown identifiers must fail clearly."""
    with pytest.raises(KeyError):
        kpi_by_id("KPI-999")


def test_denominator_requires_numerator() -> None:
    """Ratio definitions cannot contain an orphan denominator."""
    with pytest.raises(ValueError, match="denominator requires a numerator"):
        KpiSpecification(
            identifier="KPI-999",
            name="Invalid metric",
            description="Test-only invalid metric.",
            direction=MetricDirection.CONTEXT,
            status=ApprovalStatus.PROVISIONAL,
            denominator="invalid_denominator",
        )
