"""Validation controls for transformed provider data."""

import pandas as pd

from nhs_ae.transformation.columns import STANDARD_MEASURE_COLUMNS


def validate_transformed_provider_data(
    data: pd.DataFrame,
) -> None:
    """Validate transformed provider data before output."""
    required_identifiers = (
        "reporting_period_raw",
        "reporting_month",
        "org_code",
        "org_name",
        "parent_org",
    )

    for column in required_identifiers:
        if data[column].isna().any():
            raise ValueError(
                f"Null values detected in required field: {column}"
            )

    if data.duplicated(
        subset=["reporting_month", "org_code"]
    ).any():
        raise ValueError(
            "Duplicate reporting_month + org_code keys detected."
        )

    if data.loc[:, list(STANDARD_MEASURE_COLUMNS)].lt(0).any().any():
        raise ValueError(
            "Negative analytical measure values detected."
        )

    if data["parent_org"].str.strip().ne(
        data["parent_org"]
    ).any():
        raise ValueError(
            "Unexpected surrounding whitespace in parent_org."
        )
