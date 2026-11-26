"""Reproducible orchestration of the NHS A&E analytical workflow."""

import json
from pathlib import Path
from typing import Any

from nhs_ae.config import PROJECT_PATHS
from nhs_ae.database.build import build_database
from nhs_ae.transformation.multimonth import combine_monthly_provider_data
from nhs_ae.transformation.output import write_processed_csv
from nhs_ae.transformation.pipeline import run_provider_pipeline

DEFAULT_MANIFEST = (
    PROJECT_PATHS.root / "config" / "source_manifest_2024_09_to_2026_09.json"
)

START_MONTH = "2024-09-01"
END_MONTH = "2026-09-01"


def _load_manifest_sources(manifest_path: Path) -> list[dict[str, Any]]:
    """Load source records from the controlled acquisition manifest."""

    if not manifest_path.exists():
        raise FileNotFoundError(manifest_path)

    with manifest_path.open("r", encoding="utf-8") as source:
        manifest: dict[str, Any] = json.load(source)

    sources = manifest.get("sources")

    if not isinstance(sources, list) or not sources:
        raise ValueError("Manifest contains no source records.")

    return sources


def run_workflow(
    *,
    manifest_path: Path = DEFAULT_MANIFEST,
    master_dataset_path: Path = PROJECT_PATHS.master_dataset,
    database_path: Path = PROJECT_PATHS.database_file,
) -> Path:
    """Build the validated master dataset and analytical database."""

    sources = _load_manifest_sources(manifest_path)

    monthly_paths: list[Path] = []

    for record in sources:
        file_path = record.get("file_path")
        source_id = record.get("source_id")

        if not isinstance(file_path, str) or not file_path:
            raise ValueError("Manifest source is missing file_path.")

        if not isinstance(source_id, str) or not source_id:
            raise ValueError("Manifest source is missing source_id.")

        raw_path = PROJECT_PATHS.root / file_path

        if not raw_path.exists():
            raise FileNotFoundError(raw_path)

        processed_path = PROJECT_PATHS.interim / "provider_monthly" / f"{source_id}.csv"

        monthly_paths.append(
            run_provider_pipeline(
                raw_path,
                processed_path,
            )
        )

    combined = combine_monthly_provider_data(
        monthly_paths,
        start_month=START_MONTH,
        end_month=END_MONTH,
    )

    write_processed_csv(
        combined,
        master_dataset_path,
    )

    return build_database(
        database_path=database_path,
        source_path=master_dataset_path,
    )
