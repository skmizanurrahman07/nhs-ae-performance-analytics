"""Tests for reproducible workflow orchestration."""

import json
from pathlib import Path

import pandas as pd
import pytest

from nhs_ae.workflow import _load_manifest_sources


def test_load_manifest_sources(tmp_path: Path) -> None:
    """Load valid source records from a controlled manifest."""

    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "sources": [
                    {
                        "source_id": "nhs-ae-2024-09",
                        "file_path": "data/raw/month.csv",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    sources = _load_manifest_sources(manifest_path)

    assert len(sources) == 1
    assert sources[0]["source_id"] == "nhs-ae-2024-09"
    assert sources[0]["file_path"] == "data/raw/month.csv"


def test_load_manifest_sources_rejects_missing_file(
    tmp_path: Path,
) -> None:
    """Reject a manifest path that does not exist."""

    manifest_path = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError):
        _load_manifest_sources(manifest_path)


def test_load_manifest_sources_rejects_empty_sources(
    tmp_path: Path,
) -> None:
    """Reject a manifest without controlled source records."""

    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps({"sources": []}),
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Manifest contains no source records",
    ):
        _load_manifest_sources(manifest_path)


def test_controlled_manifest_has_25_months() -> None:
    """Validate the controlled production manifest scope."""

    manifest_path = Path("config/source_manifest_2024_09_to_2026_09.json")

    sources = _load_manifest_sources(manifest_path)

    assert len(sources) == 25

    periods = pd.to_datetime(
        [source["reporting_period"] for source in sources],
        format="%B %Y",
    )

    expected = pd.date_range(
        "2024-09-01",
        "2026-09-01",
        freq="MS",
    )

    assert periods.equals(expected)
