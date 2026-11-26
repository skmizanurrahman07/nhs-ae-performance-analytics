"""Tests for the end-to-end provider transformation pipeline."""

from pathlib import Path

import pandas as pd
import pytest

from nhs_ae.transformation.pipeline import run_provider_pipeline
from nhs_ae.validation.schema import (
    IDENTIFIER_COLUMNS,
    MEASURE_COLUMNS,
)


def make_test_data() -> pd.DataFrame:
    """Create minimal raw provider and TOTAL records."""
    rows: list[dict[str, object]] = []

    for period, code in (
        ("MSitAE-SEPTEMBER-2026", "AAA"),
        ("TOTAL", "TOTAL"),
    ):
        row: dict[str, object] = {
            "Period": period,
            "Org Code": code,
            "Parent Org": (
                "TOTAL"
                if code == "TOTAL"
                else "NHS ENGLAND TEST REGION "
            ),
            "Org name": (
                "TOTAL"
                if code == "TOTAL"
                else "Provider AAA"
            ),
        }

        for column in MEASURE_COLUMNS:
            row[column] = 1

        rows.append(row)

    return pd.DataFrame(
        rows,
        columns=[
            *IDENTIFIER_COLUMNS,
            *MEASURE_COLUMNS,
        ],
    )


def test_run_provider_pipeline(
    tmp_path: Path,
) -> None:
    """Pipeline must produce validated processed provider data."""
    source_path = tmp_path / "raw.csv"
    output_path = tmp_path / "processed" / "providers.csv"

    make_test_data().to_csv(
        source_path,
        index=False,
    )

    result = run_provider_pipeline(
        source_path,
        output_path,
    )

    assert result == output_path
    assert output_path.exists()

    processed = pd.read_csv(output_path)

    assert processed.shape == (1, 23)
    assert processed.iloc[0]["org_code"] == "AAA"
    assert processed.iloc[0]["parent_org"] == (
        "NHS ENGLAND TEST REGION"
    )
def test_pipeline_rejects_reconciliation_failure(
    tmp_path: Path,
) -> None:
    """Pipeline must not write output when reconciliation fails."""
    data = make_test_data()

    data.loc[
        data["Period"].eq("TOTAL"),
        "A&E attendances Type 1",
    ] = 999

    source_path = tmp_path / "raw.csv"
    output_path = tmp_path / "processed" / "providers.csv"

    data.to_csv(
        source_path,
        index=False,
    )

    with pytest.raises(
        ValueError,
        match="do not reconcile",
    ):
        run_provider_pipeline(
            source_path,
            output_path,
        )

    assert not output_path.exists()
