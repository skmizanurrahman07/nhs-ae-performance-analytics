"""Reproducible construction of the NHS A&E analytical database."""

from pathlib import Path

import duckdb

from nhs_ae.config import PROJECT_PATHS
from nhs_ae.database.connection import connect_database

SCHEMA_SQL = PROJECT_PATHS.sql / "schema" / "001_core_tables.sql"

VIEW_SQL_FILES = (
    PROJECT_PATHS.sql / "views" / "001_monthly_kpis.sql",
    PROJECT_PATHS.sql / "views" / "002_monthly_pressure.sql",
    PROJECT_PATHS.sql / "views" / "003_provider_summary.sql",
    PROJECT_PATHS.sql / "views" / "004_provider_change.sql",
    PROJECT_PATHS.sql / "views" / "005_provider_pressure.sql",
)


def _execute_sql_file(
    connection: duckdb.DuckDBPyConnection,
    sql_path: Path,
) -> None:
    """Execute a version-controlled SQL file."""
    connection.execute(
        sql_path.read_text(encoding="utf-8")
    )


def _load_master_dataset(
    connection: duckdb.DuckDBPyConnection,
    source_path: Path,
) -> None:
    """Load the validated master dataset into the core table."""
    connection.execute(
        """
        INSERT INTO core.provider_monthly
        SELECT
            reporting_period_raw,
            CAST(reporting_month AS DATE),
            org_code,
            org_name,
            parent_org,
            ae_attendances_type1,
            ae_attendances_type2,
            ae_attendances_other,
            ae_booked_attendances_type1,
            ae_booked_attendances_type2,
            ae_booked_attendances_other,
            ae_over_4hrs_type1,
            ae_over_4hrs_type2,
            ae_over_4hrs_other,
            ae_booked_over_4hrs_type1,
            ae_booked_over_4hrs_type2,
            ae_booked_over_4hrs_other,
            dta_wait_4_12hrs,
            dta_wait_12plus_hrs,
            emergency_admissions_ae_type1,
            emergency_admissions_ae_type2,
            emergency_admissions_ae_other,
            other_emergency_admissions
        FROM read_csv(?, header = true)
        """,
        [str(source_path)],
    )


def _validate_database(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    """Validate critical database invariants after construction."""
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

    if result is None:
        raise RuntimeError(
            "Database validation returned no result."
        )

    (
        row_count,
        month_count,
        provider_count,
        start_month,
        end_month,
        duplicate_keys,
    ) = result

    expected = (
        4_918,
        25,
        207,
        "2024-09-01",
        "2026-09-01",
        0,
    )

    actual = (
        row_count,
        month_count,
        provider_count,
        str(start_month),
        str(end_month),
        duplicate_keys,
    )

    if actual != expected:
        raise RuntimeError(
            "Database validation failed: "
            f"expected={expected}, actual={actual}"
        )


def build_database(
    *,
    database_path: Path = PROJECT_PATHS.database_file,
    source_path: Path = PROJECT_PATHS.master_dataset,
) -> Path:
    """Build the complete analytical DuckDB database reproducibly."""
    if not source_path.exists():
        raise FileNotFoundError(source_path)

    database_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if database_path.exists():
        database_path.unlink()

    connection = connect_database(database_path)

    try:
        connection.execute("BEGIN TRANSACTION")

        _execute_sql_file(
            connection,
            SCHEMA_SQL,
        )

        _load_master_dataset(
            connection,
            source_path,
        )

        for sql_path in VIEW_SQL_FILES:
            _execute_sql_file(
                connection,
                sql_path,
            )

        _validate_database(connection)

        connection.execute("COMMIT")

    except Exception:
        connection.execute("ROLLBACK")
        connection.close()

        if database_path.exists():
            database_path.unlink()

        raise

    else:
        connection.close()

    return database_path
