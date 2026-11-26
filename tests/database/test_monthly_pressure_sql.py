"""Reconciliation tests for the monthly pressure SQL view."""

import numpy as np
import pandas as pd

from nhs_ae.database.connection import database_connection


def test_monthly_pressure_matches_controlled_python_output() -> None:
    """Reconcile SQL pressure measures against the controlled Python output."""
    expected = pd.read_csv(
        "data/analytical/monthly_pressure.csv",
        parse_dates=["reporting_month"],
    )

    with database_connection(read_only=True) as connection:
        actual = connection.execute(
            """
            SELECT *
            FROM analytics.monthly_pressure
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

    count_columns = (
        "four_hour_breaches",
        "dta_waits_4_12hrs",
        "dta_waits_12plus_hrs",
        "total_dta_waits_4plus_hrs",
    )

    change_columns = tuple(
        column
        for column in expected.columns
        if column.endswith("_monthly_change")
        or column.endswith("_year_on_year_change")
    )

    for column in count_columns:
        assert np.array_equal(
            expected[column].to_numpy(),
            actual[column].to_numpy(),
        )

    for column in change_columns:
        assert np.allclose(
            expected[column].to_numpy(),
            actual[column].to_numpy(),
            rtol=1e-12,
            atol=1e-12,
            equal_nan=True,
        )


def test_monthly_pressure_initial_changes_are_null() -> None:
    """Validate expected lag-related null values."""
    with database_connection(read_only=True) as connection:
        first_month = connection.execute(
            """
            SELECT
                four_hour_breaches_monthly_change,
                four_hour_breaches_year_on_year_change,
                dta_waits_4_12hrs_monthly_change,
                dta_waits_4_12hrs_year_on_year_change,
                dta_waits_12plus_hrs_monthly_change,
                dta_waits_12plus_hrs_year_on_year_change,
                total_dta_waits_4plus_hrs_monthly_change,
                total_dta_waits_4plus_hrs_year_on_year_change
            FROM analytics.monthly_pressure
            ORDER BY reporting_month
            LIMIT 1
            """
        ).fetchone()

    assert first_month == (
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    )
