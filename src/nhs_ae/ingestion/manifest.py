"""Manifest models and utilities for ingested source files."""

from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from nhs_ae.ingestion.checksums import (
    calculate_sha256,
    verify_sha256,
)
from nhs_ae.ingestion.source_registry import SourceRecord


class ManifestRecord(BaseModel):
    """Immutable audit record for an ingested source file."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    source_id: str
    file_name: str
    file_path: str
    file_size_bytes: int = Field(ge=0)
    sha256: str = Field(min_length=64, max_length=64)
    reporting_period: str
    ingested_at: datetime


def build_manifest_record(
    source: SourceRecord,
    file_path: Path,
    *,
    ingested_at: datetime | None = None,
) -> ManifestRecord:
    """Build a manifest record for a registered local source file.

    Args:
        source: Registered metadata describing the external source.
        file_path: Local raw file being registered.
        ingested_at: Optional ingestion timestamp for deterministic testing.

    Returns:
        Manifest record containing source and physical file metadata.

    Raises:
        FileNotFoundError: If the supplied file does not exist.
        IsADirectoryError: If the supplied path is not a regular file.
        ValueError: If the registered filename or SHA-256 does not match
            the supplied file.
    """
    if not file_path.exists():
        raise FileNotFoundError(file_path)

    if not file_path.is_file():
        raise IsADirectoryError(file_path)

    if source.local_filename is not None and source.local_filename != file_path.name:
        message = (
            "Registered local filename does not match the supplied file: "
            f"{source.local_filename!r} != {file_path.name!r}"
        )
        raise ValueError(message)

    if source.sha256 is not None and not verify_sha256(
        file_path,
        source.sha256,
    ):
        message = (
            "Source file SHA-256 does not match the registered checksum."
        )
        raise ValueError(message)

    timestamp = ingested_at or datetime.now().astimezone()

    return ManifestRecord(
        source_id=source.source_id,
        file_name=file_path.name,
        file_path=file_path.as_posix(),
        file_size_bytes=file_path.stat().st_size,
        sha256=calculate_sha256(file_path),
        reporting_period=source.reporting_period,
        ingested_at=timestamp,
    )
