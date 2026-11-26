"""Integration tests for the complete analytical workflow."""

from pathlib import Path

import duckdb
import pandas as pd

from nhs_ae.workflow import run_workflow


def test_complete_workflow(tmp_path: Path) -> None:
    """Rebuild and validate the complete analytical workflow."""

    master_path = tmp_path / "nhs_ae_provider_validation.csv"
    database_path = tmp_path / "nhs_ae_validation.duckdb"

    result = run_workflow(
        master_dataset_path=master_path,
        database_path=database_path,
    )

    assert result == database_path
    assert master_path.exists()
    assert database_path.exists()

    master = pd.read_csv(
        master_path,
        parse_dates=["reporting_month"],
    )

    assert len(master) == 4_918
    assert len(master.columns) == 23
    assert master["reporting_month"].nunique() == 25
    assert master["org_code"].nunique() == 207

    duplicate_keys = master.duplicated(
        subset=["reporting_month", "org_code"],
    )

    assert not duplicate_keys.any()

    connection = duckdb.connect(str(database_path), read_only=True)

    try:
        result_row = connection.execute(
            """
            SELECT
                COUNT(*) AS row_count,
                COUNT(DISTINCT reporting_month) AS month_count,
                COUNT(DISTINCT org_code) AS provider_count,
                MIN(reporting_month) AS start_month,
                MAX(reporting_month) AS end_month
            FROM core.provider_monthly
            """
        ).fetchone()
    finally:
        connection.close()

    assert result_row == (
        4_918,
        25,
        207,
        pd.Timestamp("2024-09-01").date(),
        pd.Timestamp("2026-09-01").date(),
    )
