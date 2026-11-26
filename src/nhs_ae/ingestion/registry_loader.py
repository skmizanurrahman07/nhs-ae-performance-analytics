"""Load and validate registered external data sources."""

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from nhs_ae.ingestion.source_registry import SourceRecord


class SourceRegistry(BaseModel):
    """Validated collection of registered data sources."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    sources: tuple[SourceRecord, ...]


def load_source_registry(
    registry_path: Path,
) -> SourceRegistry:
    """Load and validate a JSON source registry."""
    if not registry_path.exists():
        raise FileNotFoundError(registry_path)

    if not registry_path.is_file():
        raise IsADirectoryError(registry_path)

    with registry_path.open(
        "r",
        encoding="utf-8",
    ) as source:
        raw_registry = json.load(source)

    return SourceRegistry.model_validate(raw_registry)
