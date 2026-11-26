"""Tests for external source registry models."""

from datetime import date

import pytest
from pydantic import HttpUrl, ValidationError

from nhs_ae.ingestion.source_registry import (
    SourceRecord,
    SourceStatus,
)


def test_source_record_accepts_valid_metadata() -> None:
    """A valid source record must preserve provenance metadata."""
    record = SourceRecord(
        source_id="nhs-ae-2026-08",
        publisher="NHS England",
        title="A&E Attendances and Emergency Admissions",
        source_url=HttpUrl("https://www.england.nhs.uk/"),
        reporting_period="August 2026",
        retrieved_on=date(2026, 10, 31),
        local_filename="ae_august_2026.xlsx",
        status=SourceStatus.ACTIVE,
    )

    assert record.source_id == "nhs-ae-2026-08"
    assert record.publisher == "NHS England"
    assert record.status is SourceStatus.ACTIVE


def test_source_record_defaults_to_provisional() -> None:
    """New source records must default to provisional status."""
    record = SourceRecord(
        source_id="nhs-ae-test",
        publisher="NHS England",
        title="Test source",
        source_url=HttpUrl("https://www.england.nhs.uk/"),
        reporting_period="Test period",
    )

    assert record.status is SourceStatus.PROVISIONAL


def test_source_record_rejects_invalid_url() -> None:
    """Invalid source URLs must fail validation."""
    invalid_data: dict[str, object] = {
        "source_id": "nhs-ae-test",
        "publisher": "NHS England",
        "title": "Test source",
        "source_url": "not-a-valid-url",
        "reporting_period": "Test period",
    }

    with pytest.raises(ValidationError):
        SourceRecord.model_validate(invalid_data)


def test_source_record_rejects_unexpected_fields() -> None:
    """Unexpected metadata fields must fail validation."""
    invalid_data: dict[str, object] = {
        "source_id": "nhs-ae-test",
        "publisher": "NHS England",
        "title": "Test source",
        "source_url": "https://www.england.nhs.uk/",
        "reporting_period": "Test period",
        "unexpected_field": "not allowed",
    }

    with pytest.raises(ValidationError):
        SourceRecord.model_validate(invalid_data)
