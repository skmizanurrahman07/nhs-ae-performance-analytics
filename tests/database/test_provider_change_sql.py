"""Reconciliation tests for the provider change SQL view."""

import numpy as np
import pandas as pd

from nhs_ae.database.connection import database_connection


def test_provider_change_matches_controlled_python_output() -> None:
    """Reconcile SQL provider change against the controlled Python output."""
    expected = pd.read_csv(
        "data/analytical/provider_change.csv"
    )

    with database_connection(read_only=True) as connection:
        actual = connection.execute(
            """
            SELECT *
            FROM analytics.provider_change
            """
        ).df()

    assert len(expected) == 188
    assert len(actual) == 188
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
        "current_attendances",
        "current_admissions",
        "comparison_attendances",
        "comparison_admissions",
        "months_present",
        "organisation_name_count",
        "attendance_absolute_change",
        "admission_absolute_change",
    ):
        assert np.array_equal(
            expected[column].to_numpy(),
            actual[column].to_numpy(),
        )

    for column in (
        "attendance_percentage_change",
        "admission_percentage_change",
    ):
        assert np.allclose(
            expected[column].to_numpy(),
            actual[column].to_numpy(),
            rtol=1e-12,
            atol=1e-12,
            equal_nan=True,
        )

    for column in (
        "meets_volume_threshold",
        "full_period_coverage",
        "provider_name_changed",
        "analysis_eligible",
    ):
        assert np.array_equal(
            expected[column].to_numpy(),
            actual[column].to_numpy(),
        )
