"""Reconciliation tests for the provider summary SQL view."""

import numpy as np
import pandas as pd

from nhs_ae.database.connection import database_connection


def test_provider_summary_matches_controlled_python_output() -> None:
    """Reconcile SQL provider summary against the controlled Python output."""
    expected = pd.read_csv(
        "data/analytical/provider_summary.csv"
    )

    with database_connection(read_only=True) as connection:
        actual = connection.execute(
            """
            SELECT *
            FROM analytics.provider_summary
            """
        ).df()

    assert len(expected) == 207
    assert len(actual) == 207
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
        "months_present",
        "total_attendances",
        "emergency_admissions",
    ):
        assert np.array_equal(
            expected[column].to_numpy(),
            actual[column].to_numpy(),
        )

    for column in (
        "average_monthly_attendances",
        "average_monthly_admissions",
    ):
        assert np.allclose(
            expected[column].to_numpy(),
            actual[column].to_numpy(),
            rtol=1e-12,
            atol=1e-12,
            equal_nan=True,
        )
