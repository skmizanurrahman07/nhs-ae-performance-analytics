"""Tests for cryptographic checksum utilities."""

from hashlib import sha256
from pathlib import Path

import pytest

from nhs_ae.ingestion.checksums import (
    calculate_sha256,
    verify_sha256,
)


def test_calculate_sha256_returns_expected_digest(
    tmp_path: Path,
) -> None:
    """Checksum must match the independently calculated digest."""
    content = b"NHS A&E analytics"
    source = tmp_path / "test.csv"
    source.write_bytes(content)

    expected = sha256(content).hexdigest()

    assert calculate_sha256(source) == expected


def test_calculate_sha256_rejects_missing_file(
    tmp_path: Path,
) -> None:
    """Missing source files must fail explicitly."""
    source = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        calculate_sha256(source)

def test_calculate_sha256_rejects_directory(
    tmp_path: Path,
) -> None:
    """Directories must not be accepted as source files."""
    source = tmp_path / "source_directory"
    source.mkdir()

    with pytest.raises(IsADirectoryError):
        calculate_sha256(source)

def test_verify_sha256_accepts_matching_digest(
    tmp_path: Path,
) -> None:
    """Matching SHA-256 digest must pass verification."""
    content = b"NHS A&E analytics"
    source = tmp_path / "test.csv"
    source.write_bytes(content)

    expected = sha256(content).hexdigest()

    assert verify_sha256(source, expected)


def test_verify_sha256_rejects_mismatched_digest(
    tmp_path: Path,
) -> None:
    """Mismatched SHA-256 digest must fail verification."""
    source = tmp_path / "test.csv"
    source.write_bytes(b"NHS A&E analytics")

    wrong_digest = "0" * 64

    assert not verify_sha256(source, wrong_digest)
