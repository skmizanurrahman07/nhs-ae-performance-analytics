"""End-to-end transformation pipeline for monthly NHS A&E data."""

from pathlib import Path

import pandas as pd

from nhs_ae.transformation.output import write_processed_csv
from nhs_ae.transformation.provider import transform_provider_records
from nhs_ae.transformation.reconciliation import (
    reconcile_processed_totals,
)


def run_provider_pipeline(
    source_path: Path,
    output_path: Path,
) -> Path:
    """Transform, reconcile, and write validated provider data."""
    raw_data = pd.read_csv(source_path)

    transformed = transform_provider_records(raw_data)

    reconciliation = reconcile_processed_totals(
        raw_data,
        transformed,
    )

    if not reconciliation["reconciled"].all():
        raise ValueError(
            "Processed measures do not reconcile to published totals."
        )

    return write_processed_csv(
        transformed,
        output_path,
    )
