"""Transform raw monthly NHS A&E provider records."""

import pandas as pd

from nhs_ae.transformation.columns import (
    COLUMN_RENAME_MAP,
    STANDARD_MEASURE_COLUMNS,
)
from nhs_ae.transformation.validation import (
    validate_transformed_provider_data,
)
from nhs_ae.validation.profiling import provider_records
from nhs_ae.validation.schema import REQUIRED_COLUMNS


def transform_provider_records(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Transform raw provider records into analytical form."""
    unexpected_columns = [
        column
        for column in data.columns
        if column not in REQUIRED_COLUMNS
    ]

    populated_unexpected = [
        column
        for column in unexpected_columns
        if data[column].notna().any()
    ]

    if populated_unexpected:
        message = (
            "Populated unexpected source columns detected: "
            f"{populated_unexpected}"
        )
        raise ValueError(message)

    controlled_source = data.loc[
        :,
        list(REQUIRED_COLUMNS),
    ].copy()


    transformed = provider_records(controlled_source).rename(
        columns=COLUMN_RENAME_MAP
    )

    transformed["reporting_month"] = pd.to_datetime(
        transformed["reporting_period_raw"]
        .str.removeprefix("MSitAE-")
        .str.title(),
        format="%B-%Y",
    )

    transformed["parent_org"] = (
        transformed["parent_org"]
        .astype("string")
        .str.strip()
    )

    transformed["org_code"] = transformed[
        "org_code"
    ].astype("string")

    transformed["org_name"] = transformed[
        "org_name"
    ].astype("string")

    for column in STANDARD_MEASURE_COLUMNS:
        transformed[column] = pd.to_numeric(
            transformed[column],
            errors="raise",
        ).astype("int64")

    ordered_columns = [
        "reporting_period_raw",
        "reporting_month",
        "org_code",
        "org_name",
        "parent_org",
        *STANDARD_MEASURE_COLUMNS,
    ]

    result = transformed.loc[:, ordered_columns].copy()

    validate_transformed_provider_data(result)

    return result
