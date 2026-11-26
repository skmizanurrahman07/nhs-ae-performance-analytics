"""Tests for project path configuration."""

from pathlib import Path

from nhs_ae.config import ProjectPaths


def test_project_paths_are_derived_from_root(tmp_path: Path) -> None:
    """Data paths must remain relative to the configured project root."""
    paths = ProjectPaths(root=tmp_path)
    assert paths.raw == tmp_path / "data" / "raw"
    assert paths.processed == tmp_path / "data" / "processed"
