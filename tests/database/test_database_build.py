"""Integration tests for reproducible DuckDB construction."""

from pathlib import Path

import duckdb

from nhs_ae.database.build import build_database


def test_database_build_is_reproducible(
    tmp_path: Path,
) -> None:
    """Build and validate a complete analytical database."""
    database_path = tmp_path / "nhs_ae_test.duckdb"

    built_path = build_database(
        database_path=database_path,
    )

    assert built_path == database_path
    assert built_path.exists()

    connection = duckdb.connect(
        str(built_path),
        read_only=True,
    )

    try:
        core_result = connection.execute(
            """
            SELECT
                COUNT(*) AS rows,
                COUNT(DISTINCT reporting_month) AS months,
                COUNT(DISTINCT org_code) AS providers
            FROM core.provider_monthly
            """
        ).fetchone()

        analytical_views = connection.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'analytics'
              AND table_type = 'VIEW'
            ORDER BY table_name
            """
        ).fetchall()

        output_counts = {
            "monthly_kpis": connection.execute(
                "SELECT COUNT(*) FROM analytics.monthly_kpis"
            ).fetchone(),
            "monthly_pressure": connection.execute(
                "SELECT COUNT(*) FROM analytics.monthly_pressure"
            ).fetchone(),
            "provider_summary": connection.execute(
                "SELECT COUNT(*) FROM analytics.provider_summary"
            ).fetchone(),
            "provider_change": connection.execute(
                "SELECT COUNT(*) FROM analytics.provider_change"
            ).fetchone(),
            "provider_pressure": connection.execute(
                "SELECT COUNT(*) FROM analytics.provider_pressure"
            ).fetchone(),
        }

    finally:
        connection.close()

    assert core_result == (4_918, 25, 207)

    assert analytical_views == [
        ("monthly_kpis",),
        ("monthly_pressure",),
        ("provider_change",),
        ("provider_pressure",),
        ("provider_summary",),
    ]

    assert output_counts == {
        "monthly_kpis": (25,),
        "monthly_pressure": (25,),
        "provider_summary": (207,),
        "provider_change": (188,),
        "provider_pressure": (188,),
    }
