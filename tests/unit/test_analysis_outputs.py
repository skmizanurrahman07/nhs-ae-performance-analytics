"""Tests for controlled analytical output tables."""

from pathlib import Path

import pandas as pd

from nhs_ae.analysis.outputs import (
    write_analytical_outputs,
)


def test_writes_analytical_outputs(
    tmp_path: Path,
) -> None:
    """Controlled analytical tables must be written to CSV."""
    outputs = {
        "monthly_kpis": pd.DataFrame(
            {
                "reporting_month": [
                    "2026-09-01",
                ],
                "total_attendances": [
                    100,
                ],
            }
        ),
        "provider_summary": pd.DataFrame(
            {
                "org_code": [
                    "AAA",
                ],
                "total_attendances": [
                    100,
                ],
            }
        ),
    }

    paths = write_analytical_outputs(
        outputs,
        tmp_path,
    )

    assert len(paths) == 2

    assert (
        tmp_path / "monthly_kpis.csv"
    ).is_file()

    assert (
        tmp_path / "provider_summary.csv"
    ).is_file()


def test_output_writer_preserves_row_counts(
    tmp_path: Path,
) -> None:
    """Written analytical tables must preserve row counts."""
    outputs = {
        "example": pd.DataFrame(
            {
                "value": [
                    1,
                    2,
                    3,
                ]
            }
        )
    }

    paths = write_analytical_outputs(
        outputs,
        tmp_path,
    )

    result = pd.read_csv(paths[0])

    assert len(result) == 3
