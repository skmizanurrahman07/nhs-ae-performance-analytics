"""Cryptographic checksum utilities for raw source files."""

from hashlib import sha256
from pathlib import Path

BUFFER_SIZE = 1024 * 1024


def calculate_sha256(file_path: Path) -> str:
    """Calculate the SHA-256 digest of a file.

    Args:
        file_path: File requiring integrity verification.

    Returns:
        Lowercase hexadecimal SHA-256 digest.

    Raises:
        FileNotFoundError: If the supplied path does not exist.
        IsADirectoryError: If the supplied path is not a file.
    """
    if not file_path.exists():
        raise FileNotFoundError(file_path)

    if not file_path.is_file():
        raise IsADirectoryError(file_path)

    digest = sha256()

    with file_path.open("rb") as source:
        while chunk := source.read(BUFFER_SIZE):
            digest.update(chunk)

    return digest.hexdigest()

def verify_sha256(
    file_path: Path,
    expected_sha256: str,
) -> bool:
    """Verify a file against an expected SHA-256 digest."""
    actual_sha256 = calculate_sha256(file_path)

    return actual_sha256 == expected_sha256.lower()
