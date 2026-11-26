"""Tests for the DuckDB core analytical database."""

from nhs_ae.database.connection import database_connection


def test_provider_monthly_database_scope() -> None:
    """Validate the expected provider-month analytical grain."""
    with database_connection(read_only=True) as connection:
        result = connection.execute(
            """
            SELECT
                COUNT(*) AS row_count,
                COUNT(DISTINCT reporting_month) AS month_count,
                COUNT(DISTINCT org_code) AS provider_count,
                MIN(reporting_month) AS start_month,
                MAX(reporting_month) AS end_month,
                COUNT(*) - COUNT(
                    DISTINCT (reporting_month, org_code)
                ) AS duplicate_keys
            FROM core.provider_monthly
            """
        ).fetchone()

    assert result is not None

    (
        row_count,
        month_count,
        provider_count,
        start_month,
        end_month,
        duplicate_keys,
    ) = result

    assert row_count == 4_918
    assert month_count == 25
    assert provider_count == 207
    assert str(start_month) == "2024-09-01"
    assert str(end_month) == "2026-09-01"
    assert duplicate_keys == 0
