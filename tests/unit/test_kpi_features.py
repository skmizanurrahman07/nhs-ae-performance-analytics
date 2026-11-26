"""Tests for approved KPI feature derivation."""

import pandas as pd
import pytest

from nhs_ae.transformation.kpi_features import (
    ATTENDANCE_COLUMNS,
    EMERGENCY_ADMISSION_COLUMNS,
    derive_approved_kpis,
)


def make_kpi_data() -> pd.DataFrame:
    """Create representative KPI source measures."""
    data: dict[str, list[int]] = {}

    for column in ATTENDANCE_COLUMNS:
        data[column] = [10]

    for column in EMERGENCY_ADMISSION_COLUMNS:
        data[column] = [2]

    return pd.DataFrame(data)


def test_derives_total_attendances() -> None:
    """KPI-001 must sum all eligible attendance measures."""
    result = derive_approved_kpis(
        make_kpi_data()
    )

    assert result.iloc[0]["total_attendances"] == 60


def test_derives_emergency_admissions() -> None:
    """KPI-002 must sum all emergency-admission measures."""
    result = derive_approved_kpis(
        make_kpi_data()
    )

    assert result.iloc[0]["emergency_admissions"] == 8


def test_derivation_preserves_source_rows() -> None:
    """KPI derivation must not alter row count."""
    data = make_kpi_data()

    result = derive_approved_kpis(data)

    assert len(result) == len(data)


def test_derivation_does_not_mutate_input() -> None:
    """KPI derivation must leave input data unchanged."""
    data = make_kpi_data()

    derive_approved_kpis(data)

    assert "total_attendances" not in data.columns
    assert "emergency_admissions" not in data.columns


def test_derivation_rejects_missing_source_column() -> None:
    """Missing controlled source measures must fail."""
    data = make_kpi_data().drop(
        columns=["ae_attendances_type1"]
    )

    with pytest.raises(
        ValueError,
        match="Required KPI source columns are missing",
    ):
        derive_approved_kpis(data)
