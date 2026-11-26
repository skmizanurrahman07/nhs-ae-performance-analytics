"""Tests for A&E pressure and patient-flow feature derivation."""

import pandas as pd
import pytest

from nhs_ae.transformation.pressure_features import (
    DTA_WAIT_COLUMNS,
    FOUR_HOUR_BREACH_COLUMNS,
    derive_pressure_features,
)


def make_pressure_data() -> pd.DataFrame:
    """Create representative pressure source measures."""
    data: dict[str, list[int]] = {}

    for column in FOUR_HOUR_BREACH_COLUMNS:
        data[column] = [10]

    data["dta_wait_4_12hrs"] = [20]
    data["dta_wait_12plus_hrs"] = [5]

    return pd.DataFrame(data)


def test_derives_four_hour_breaches() -> None:
    """All six breach measures must be combined."""
    result = derive_pressure_features(
        make_pressure_data()
    )

    assert result.iloc[0]["four_hour_breaches"] == 60


def test_derives_dta_wait_measures() -> None:
    """DTA measures must retain controlled source values."""
    result = derive_pressure_features(
        make_pressure_data()
    )

    assert result.iloc[0]["dta_waits_4_12hrs"] == 20
    assert result.iloc[0]["dta_waits_12plus_hrs"] == 5
    assert result.iloc[0][
        "total_dta_waits_4plus_hrs"
    ] == 25


def test_derivation_preserves_input() -> None:
    """Pressure derivation must not mutate input data."""
    data = make_pressure_data()

    derive_pressure_features(data)

    assert "four_hour_breaches" not in data.columns
    assert "total_dta_waits_4plus_hrs" not in data.columns


def test_rejects_missing_source_column() -> None:
    """Missing controlled source measures must fail."""
    data = make_pressure_data().drop(
        columns=[FOUR_HOUR_BREACH_COLUMNS[0]]
    )

    with pytest.raises(
        ValueError,
        match="Required pressure source columns are missing",
    ):
        derive_pressure_features(data)


def test_rejects_missing_values() -> None:
    """Missing pressure values must fail."""
    data = make_pressure_data()
    data.loc[0, DTA_WAIT_COLUMNS[0]] = pd.NA

    with pytest.raises(
        ValueError,
        match="contain missing values",
    ):
        derive_pressure_features(data)


def test_rejects_negative_values() -> None:
    """Negative pressure values must fail."""
    data = make_pressure_data()
    data.loc[0, FOUR_HOUR_BREACH_COLUMNS[0]] = -1

    with pytest.raises(
        ValueError,
        match="contain negative values",
    ):
        derive_pressure_features(data)


def test_does_not_create_provisional_kpi() -> None:
    """Pressure derivation must not create KPI-004."""
    result = derive_pressure_features(
        make_pressure_data()
    )

    prohibited_columns = {
        "four_hour_performance",
        "four_hour_breach_rate",
        "within_four_hours",
    }

    assert prohibited_columns.isdisjoint(result.columns)
