"""Reusable profiling utilities for monthly NHS A&E source data."""

from dataclasses import dataclass

import pandas as pd

from nhs_ae.validation.schema import (
    IDENTIFIER_COLUMNS,
    MEASURE_COLUMNS,
    PROVIDER_KEY_COLUMNS,
    TOTAL_VALUE,
)


@dataclass(frozen=True, slots=True)
class SourceProfile:
    """Summary of structural and data-quality characteristics."""

    row_count: int
    column_count: int
    provider_row_count: int
    total_row_count: int
    unique_org_count: int
    missing_value_count: int
    duplicate_provider_key_count: int
    negative_measure_count: int

@dataclass(frozen=True, slots=True)
class IdentifierProfile:
    """Summary of provider identifier integrity."""

    column: str
    null_count: int
    blank_count: int
    whitespace_only_count: int
    surrounding_whitespace_count: int


def _total_record_mask(data: pd.DataFrame) -> pd.Series:
    """Identify published TOTAL control records across source variants."""
    period_is_total = (
        data["Period"]
        .astype("string")
        .str.strip()
        .str.casefold()
        .eq(TOTAL_VALUE.casefold())
    )

    identifiers_are_total = (
        data["Org Code"]
        .astype("string")
        .str.strip()
        .str.casefold()
        .eq(TOTAL_VALUE.casefold())
        & data["Parent Org"]
        .astype("string")
        .str.strip()
        .str.casefold()
        .eq(TOTAL_VALUE.casefold())
        & data["Org name"]
        .astype("string")
        .str.strip()
        .str.casefold()
        .eq(TOTAL_VALUE.casefold())
    )

    return period_is_total | identifiers_are_total


def provider_records(data: pd.DataFrame) -> pd.DataFrame:
    """Return provider records excluding published TOTAL rows.

    Args:
        data: Monthly A&E source data.

    Returns:
        Copy containing provider-level records only.
    """
    return data.loc[~_total_record_mask(data)].copy()


def total_records(data: pd.DataFrame) -> pd.DataFrame:
    """Return published TOTAL control records.

    Args:
        data: Monthly A&E source data.

    Returns:
        Copy containing published TOTAL records only.
    """
    return data.loc[_total_record_mask(data)].copy()


def build_source_profile(data: pd.DataFrame) -> SourceProfile:
    """Build structural and data-quality summary statistics.

    Args:
        data: Monthly A&E source data.

    Returns:
        Immutable source profile.
    """
    providers = provider_records(data)
    totals = total_records(data)

    duplicate_count = int(providers.duplicated(subset=list(PROVIDER_KEY_COLUMNS)).sum())

    negative_count = int(providers.loc[:, list(MEASURE_COLUMNS)].lt(0).sum().sum())

    return SourceProfile(
        row_count=len(data),
        column_count=len(data.columns),
        provider_row_count=len(providers),
        total_row_count=len(totals),
        unique_org_count=providers["Org Code"].nunique(),
        missing_value_count=int(data.isna().sum().sum()),
        duplicate_provider_key_count=duplicate_count,
        negative_measure_count=negative_count,
    )

def profile_identifier_integrity(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Profile null, blank, and whitespace issues in identifiers.

    Args:
        data: Monthly A&E source data.

    Returns:
        Table containing identifier-integrity counts for provider records.
    """
    providers = provider_records(data)
    rows: list[dict[str, object]] = []

    for column in IDENTIFIER_COLUMNS:

        values = providers[column].astype("string")

        null_count = int(values.isna().sum())

        blank_count = int(
            values.fillna("").eq("").sum()
        )

        whitespace_only_count = int(
            values.fillna("")
            .str.fullmatch(r"\s+")
            .fillna(False)
            .sum()
        )

        surrounding_whitespace_count = int(
            values.fillna("")
            .ne(values.fillna("").str.strip())
            .sum()
        )

        rows.append(
            {
                "column": column,
                "null_count": null_count,
                "blank_count": blank_count,
                "whitespace_only_count": (
                    whitespace_only_count
                ),
                "surrounding_whitespace_count": (
                    surrounding_whitespace_count
                ),
            }
        )

    return pd.DataFrame(rows)

def profile_organisation_mappings(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Profile consistency of provider organisation mappings.

    Args:
        data: Monthly A&E source data.

    Returns:
        Table containing the number of mapping exceptions.
    """
    providers = provider_records(data).copy()

    providers["Parent Org"] = (
        providers["Parent Org"]
        .astype("string")
        .str.strip()
    )

    code_to_name = (
        providers.groupby("Org Code", dropna=False)["Org name"]
        .nunique(dropna=False)
        .gt(1)
        .sum()
    )

    name_to_code = (
        providers.groupby("Org name", dropna=False)["Org Code"]
        .nunique(dropna=False)
        .gt(1)
        .sum()
    )

    code_to_parent = (
        providers.groupby("Org Code", dropna=False)["Parent Org"]
        .nunique(dropna=False)
        .gt(1)
        .sum()
    )

    return pd.DataFrame(
        {
            "check": [
                "Org Code maps to multiple Org names",
                "Org name maps to multiple Org Codes",
                "Org Code maps to multiple Parent Orgs",
            ],
            "exceptions": [
                int(code_to_name),
                int(name_to_code),
                int(code_to_parent),
            ],
        }
    )

def validate_four_hour_breach_compatibility(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Check breaches do not exceed compatible attendance counts.

    Args:
        data: Monthly A&E source data.

    Returns:
        Table containing cross-field compatibility results.
    """
    providers = provider_records(data)

    field_pairs = (
        (
            "Type 1",
            "A&E attendances Type 1",
            "Attendances over 4hrs Type 1",
        ),
        (
            "Type 2",
            "A&E attendances Type 2",
            "Attendances over 4hrs Type 2",
        ),
        (
            "Other A&E Department",
            "A&E attendances Other A&E Department",
            "Attendances over 4hrs Other Department",
        ),
    )

    rows: list[dict[str, object]] = []

    for category, attendance_column, breach_column in field_pairs:
        invalid = providers[breach_column].gt(
            providers[attendance_column]
        )

        rows.append(
            {
                "category": category,
                "attendance_column": attendance_column,
                "breach_column": breach_column,
                "invalid_record_count": int(invalid.sum()),
                "passed": not bool(invalid.any()),
            }
        )

    return pd.DataFrame(rows)

def reconcile_published_totals(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Compare provider sums against the published TOTAL record.

    Args:
        data: Monthly A&E source data.

    Returns:
        Table containing calculated totals, published totals,
        differences, and reconciliation results.

    Raises:
        ValueError: If exactly one published TOTAL record is
            not present.
    """
    providers = provider_records(data)
    totals = total_records(data)

    if len(totals) != 1:
        message = f"Expected exactly one published TOTAL record; found {len(totals)}."
        raise ValueError(message)

    published = totals.iloc[0]

    result = pd.DataFrame(
        {
            "provider_sum": providers[list(MEASURE_COLUMNS)].sum(),
            "published_total": published[list(MEASURE_COLUMNS)],
        }
    )

    result["difference"] = result["provider_sum"] - result["published_total"]

    result["reconciled"] = result["difference"].eq(0)

    return result
