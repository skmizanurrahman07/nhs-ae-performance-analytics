"""Tests for processed analytical dataset output."""

from pathlib import Path

import pandas as pd

from nhs_ae.transformation.output import write_processed_csv


def test_write_processed_csv(
    tmp_path: Path,
) -> None:
    """Processed dataset must be written without an index."""
    data = pd.DataFrame(
        {
            "org_code": ["AAA", "BBB"],
            "value": [1, 2],
        }
    )

    output_path = tmp_path / "processed" / "providers.csv"

    result = write_processed_csv(
        data,
        output_path,
    )

    assert result == output_path
    assert output_path.exists()

    written = pd.read_csv(output_path)

    assert written.columns.tolist() == [
        "org_code",
        "value",
    ]
    assert len(written) == 2
