"""Tests for source file manifest creation."""

from datetime import UTC, date, datetime
from hashlib import sha256
from pathlib import Path

import pytest
from pydantic import HttpUrl

from nhs_ae.ingestion.manifest import build_manifest_record
from nhs_ae.ingestion.source_registry import (
    SourceRecord,
    SourceStatus,
)


@pytest.fixture
def registered_source() -> SourceRecord:
    """Return valid source metadata for manifest tests."""
    return SourceRecord(
        source_id="nhs-ae-test-001",
        publisher="NHS England",
        title="A&E Attendances and Emergency Admissions",
        source_url=HttpUrl("https://www.england.nhs.uk/"),
        reporting_period="Test period",
        retrieved_on=date(2026, 10, 31),
        local_filename="ae_test.xlsx",
        status=SourceStatus.ACTIVE,
    )


def test_build_manifest_record(
    tmp_path: Path,
    registered_source: SourceRecord,
) -> None:
    """Manifest must contain reproducible physical file metadata."""
    content = b"test NHS aggregate data"
    source_file = tmp_path / "ae_test.xlsx"
    source_file.write_bytes(content)

    ingestion_time = datetime(
        2026,
        10,
        31,
        12,
        0,
        tzinfo=UTC,
    )

    manifest = build_manifest_record(
        registered_source,
        source_file,
        ingested_at=ingestion_time,
    )

    assert manifest.source_id == "nhs-ae-test-001"
    assert manifest.file_name == "ae_test.xlsx"
    assert manifest.file_size_bytes == len(content)
    assert manifest.sha256 == sha256(content).hexdigest()
    assert manifest.reporting_period == "Test period"
    assert manifest.ingested_at == ingestion_time


def test_manifest_rejects_missing_file(
    tmp_path: Path,
    registered_source: SourceRecord,
) -> None:
    """Manifest creation must fail for a missing file."""
    missing_file = tmp_path / "ae_test.xlsx"

    with pytest.raises(FileNotFoundError):
        build_manifest_record(
            registered_source,
            missing_file,
        )


def test_manifest_rejects_directory(
    tmp_path: Path,
    registered_source: SourceRecord,
) -> None:
    """Manifest creation must reject directories."""
    directory = tmp_path / "ae_test.xlsx"
    directory.mkdir()

    with pytest.raises(IsADirectoryError):
        build_manifest_record(
            registered_source,
            directory,
        )


def test_manifest_rejects_filename_mismatch(
    tmp_path: Path,
    registered_source: SourceRecord,
) -> None:
    """Registered and physical filenames must agree."""
    source_file = tmp_path / "different_name.xlsx"
    source_file.write_bytes(b"test")

    with pytest.raises(
        ValueError,
        match="Registered local filename does not match",
    ):
        build_manifest_record(
            registered_source,
            source_file,
        )

def test_manifest_rejects_checksum_mismatch(
    tmp_path: Path,
    registered_source: SourceRecord,
) -> None:
    """Manifest creation must reject a mismatched registered checksum."""
    source_file = tmp_path / "ae_test.xlsx"
    source_file.write_bytes(b"test NHS aggregate data")

    source_with_wrong_checksum = registered_source.model_copy(
        update={
            "sha256": "0" * 64,
        }
    )

    with pytest.raises(
        ValueError,
        match="SHA-256 does not match",
    ):
        build_manifest_record(
            source_with_wrong_checksum,
            source_file,
        )
