"""Tests for JSON source registry loading."""

import json
from pathlib import Path

import pytest

from nhs_ae.ingestion.registry_loader import load_source_registry


def test_load_empty_source_registry(
    tmp_path: Path,
) -> None:
    """Empty source list must load successfully."""
    registry_path = tmp_path / "sources.json"

    registry_path.write_text(
        json.dumps({"sources": []}),
        encoding="utf-8",
    )

    registry = load_source_registry(registry_path)

    assert registry.sources == ()


def test_registry_loader_rejects_missing_file(
    tmp_path: Path,
) -> None:
    """Missing registry file must fail explicitly."""
    registry_path = tmp_path / "sources.json"

    with pytest.raises(FileNotFoundError):
        load_source_registry(registry_path)


def test_registry_loader_rejects_directory(
    tmp_path: Path,
) -> None:
    """Directory must not be accepted as registry file."""
    registry_path = tmp_path / "sources.json"
    registry_path.mkdir()

    with pytest.raises(IsADirectoryError):
        load_source_registry(registry_path)

def test_load_valid_source_record(
    tmp_path: Path,
) -> None:
    """Valid registry metadata must load as a SourceRecord."""
    registry_path = tmp_path / "sources.json"

    registry_data = {
        "sources": [
            {
                "source_id": "nhs-ae-2026-09",
                "publisher": "NHS England",
                "title": "A&E Attendances and Emergency Admissions",
                "source_url": "https://www.england.nhs.uk/",
                "reporting_period": "September 2026",
                "local_filename": "September-2026.csv",
                "status": "active",
            }
        ]
    }

    registry_path.write_text(
        json.dumps(registry_data),
        encoding="utf-8",
    )

    registry = load_source_registry(registry_path)

    assert len(registry.sources) == 1
    assert registry.sources[0].source_id == "nhs-ae-2026-09"
    assert registry.sources[0].reporting_period == "September 2026"

