"""Tests for transformed provider-data validation."""

import pandas as pd
import pytest

from nhs_ae.transformation.columns import STANDARD_MEASURE_COLUMNS
from nhs_ae.transformation.validation import (
    validate_transformed_provider_data,
)


def make_valid_data() -> pd.DataFrame:
    """Create minimal valid transformed provider data."""
    row: dict[str, object] = {
        "reporting_period_raw": "MSitAE-SEPTEMBER-2026",
        "reporting_month": pd.Timestamp("2026-09-01"),
        "org_code": "AAA",
        "org_name": "Provider AAA",
        "parent_org": "NHS ENGLAND TEST REGION",
    }

    for column in STANDARD_MEASURE_COLUMNS:
        row[column] = 1

    return pd.DataFrame([row])


def test_valid_transformed_data_passes() -> None:
    """Valid transformed provider data must pass validation."""
    validate_transformed_provider_data(make_valid_data())


def test_duplicate_provider_key_fails() -> None:
    """Duplicate provider-period keys must fail."""
    data = make_valid_data()
    data = pd.concat([data, data], ignore_index=True)

    with pytest.raises(
        ValueError,
        match="Duplicate reporting_month",
    ):
        validate_transformed_provider_data(data)


def test_negative_measure_fails() -> None:
    """Negative analytical measures must fail."""
    data = make_valid_data()
    data.loc[0, STANDARD_MEASURE_COLUMNS[0]] = -1

    with pytest.raises(
        ValueError,
        match="Negative analytical measure",
    ):
        validate_transformed_provider_data(data)


def test_parent_org_whitespace_fails() -> None:
    """Uncontrolled parent organisation whitespace must fail."""
    data = make_valid_data()
    data.loc[0, "parent_org"] = "NHS ENGLAND TEST REGION "

    with pytest.raises(
        ValueError,
        match="surrounding whitespace",
    ):
        validate_transformed_provider_data(data)


def test_null_required_identifier_fails() -> None:
    """Null required identifiers must fail."""
    data = make_valid_data()
    data.loc[0, "org_code"] = None

    with pytest.raises(
        ValueError,
        match="Null values detected",
    ):
        validate_transformed_provider_data(data)
