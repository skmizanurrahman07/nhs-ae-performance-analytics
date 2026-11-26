"""Reconciliation tests for the provider pressure SQL view."""

import numpy as np
import pandas as pd

from nhs_ae.database.connection import database_connection


def test_provider_pressure_matches_controlled_python_output() -> None:
    """Reconcile SQL provider pressure against the controlled Python output."""
    expected = pd.read_csv(
        "data/analytical/provider_pressure.csv"
    )

    with database_connection(read_only=True) as connection:
        actual = connection.execute(
            """
            SELECT *
            FROM analytics.provider_pressure
            """
        ).df()

    assert len(expected) == 188
    assert len(actual) == 188
    assert len(expected.columns) == 30
    assert len(actual.columns) == 30
    assert expected.columns.tolist() == actual.columns.tolist()

    assert expected["org_code"].is_unique
    assert actual["org_code"].is_unique

    expected = (
        expected
        .sort_values("org_code")
        .reset_index(drop=True)
    )

    actual = (
        actual
        .sort_values("org_code")
        .reset_index(drop=True)
    )

    for column in (
        "org_code",
        "latest_org_name",
    ):
        assert np.array_equal(
            expected[column].to_numpy(),
            actual[column].to_numpy(),
        )

    for column in (
        "current_total_attendances",
        "current_emergency_admissions",
        "current_four_hour_breaches",
        "current_dta_waits_4_12hrs",
        "current_dta_waits_12plus_hrs",
        "current_total_dta_waits_4plus_hrs",
        "comparison_total_attendances",
        "comparison_emergency_admissions",
        "comparison_four_hour_breaches",
        "comparison_dta_waits_4_12hrs",
        "comparison_dta_waits_12plus_hrs",
        "comparison_total_dta_waits_4plus_hrs",
        "months_present",
        "organisation_name_count",
        "four_hour_breaches_absolute_change",
        "dta_waits_4_12hrs_absolute_change",
        "dta_waits_12plus_hrs_absolute_change",
        "total_dta_waits_4plus_hrs_absolute_change",
    ):
        assert np.array_equal(
            expected[column].to_numpy(),
            actual[column].to_numpy(),
        )

    for column in (
        "four_hour_breaches_percentage_change",
        "dta_waits_4_12hrs_percentage_change",
        "dta_waits_12plus_hrs_percentage_change",
        "total_dta_waits_4plus_hrs_percentage_change",
    ):
        assert np.allclose(
            expected[column].to_numpy(),
            actual[column].to_numpy(),
            rtol=1e-12,
            atol=1e-12,
            equal_nan=True,
        )

    for column in (
        "meets_attendance_threshold",
        "meets_admission_threshold",
        "full_period_coverage",
        "provider_name_changed",
        "breach_analysis_eligible",
        "dta_analysis_eligible",
    ):
        assert np.array_equal(
            expected[column].to_numpy(),
            actual[column].to_numpy(),
        )
