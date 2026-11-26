"""Write validated analytical datasets to controlled outputs."""

from pathlib import Path

import pandas as pd


def write_processed_csv(
    data: pd.DataFrame,
    output_path: Path,
) -> Path:
    """Write validated analytical data to CSV."""
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data.to_csv(
        output_path,
        index=False,
    )

    return output_path
