"""Models describing registered external data sources."""

from datetime import date
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, HttpUrl


class SourceStatus(StrEnum):
    """Lifecycle status for a registered source."""

    ACTIVE = "active"
    ARCHIVED = "archived"
    PROVISIONAL = "provisional"


class SourceRecord(BaseModel):
    """Metadata describing an external analytical data source."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    source_id: str
    publisher: str
    title: str
    source_url: HttpUrl
    reporting_period: str
    retrieved_on: date | None = None
    local_filename: str | None = None
    sha256: str | None = None
    status: SourceStatus = SourceStatus.PROVISIONAL
    notes: str | None = None
