"""Reconciliation tests for the monthly KPI SQL view."""

import numpy as np
import pandas as pd

from nhs_ae.database.connection import database_connection


def test_monthly_kpis_match_controlled_python_output() -> None:
    """Reconcile SQL monthly KPIs against the controlled Python output."""
    expected = pd.read_csv(
        "data/analytical/monthly_kpis.csv",
        parse_dates=["reporting_month"],
    )

    with database_connection(read_only=True) as connection:
        actual = connection.execute(
            """
            SELECT *
            FROM analytics.monthly_kpis
            ORDER BY reporting_month
            """
        ).df()

    actual["reporting_month"] = pd.to_datetime(
        actual["reporting_month"]
    )

    assert len(expected) == 25
    assert len(actual) == 25
    assert expected.columns.tolist() == actual.columns.tolist()

    pd.testing.assert_series_equal(
        expected["reporting_month"],
        actual["reporting_month"],
        check_names=False,
    )

    for column in (
        "total_attendances",
        "emergency_admissions",
    ):
        assert np.array_equal(
            expected[column].to_numpy(),
            actual[column].to_numpy(),
        )

    for column in (
        "attendance_monthly_change",
        "admission_monthly_change",
        "attendance_year_on_year_change",
        "admission_year_on_year_change",
    ):
        assert np.allclose(
            expected[column].to_numpy(),
            actual[column].to_numpy(),
            rtol=1e-12,
            atol=1e-12,
            equal_nan=True,
        )


def test_monthly_kpis_initial_change_values_are_null() -> None:
    """Validate expected lag-related null values."""
    with database_connection(read_only=True) as connection:
        first_month = connection.execute(
            """
            SELECT
                attendance_monthly_change,
                admission_monthly_change,
                attendance_year_on_year_change,
                admission_year_on_year_change
            FROM analytics.monthly_kpis
            ORDER BY reporting_month
            LIMIT 1
            """
        ).fetchone()

    assert first_month == (None, None, None, None)
