"""Longitudinal quality checks for multi-month analytical data."""

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True, slots=True)
class LongitudinalProfile:
    """Summary of multi-month analytical dataset integrity."""

    row_count: int
    column_count: int
    month_count: int
    provider_count: int
    duplicate_provider_month_count: int
    missing_value_count: int
    negative_measure_count: int


def build_longitudinal_profile(
    data: pd.DataFrame,
    measure_columns: tuple[str, ...],
) -> LongitudinalProfile:
    """Build quality statistics for the combined analytical dataset."""
    duplicate_count = int(
        data.duplicated(
            subset=["reporting_month", "org_code"]
        ).sum()
    )

    negative_count = int(
        data.loc[:, list(measure_columns)]
        .lt(0)
        .sum()
        .sum()
    )

    return LongitudinalProfile(
        row_count=len(data),
        column_count=len(data.columns),
        month_count=data["reporting_month"].nunique(),
        provider_count=data["org_code"].nunique(),
        duplicate_provider_month_count=duplicate_count,
        missing_value_count=int(data.isna().sum().sum()),
        negative_measure_count=negative_count,
    )


def monthly_provider_counts(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Return provider-record counts by reporting month."""
    result = (
        data.groupby(
            "reporting_month",
            as_index=False,
        )
        .agg(
            provider_count=(
                "org_code",
                "nunique",
            ),
            record_count=(
                "org_code",
                "size",
            ),
        )
        .sort_values("reporting_month")
        .reset_index(drop=True)
    )

    return result


def provider_month_coverage(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Summarise longitudinal month coverage by provider code."""
    result = (
        data.groupby(
            "org_code",
            as_index=False,
        )
        .agg(
            months_present=(
                "reporting_month",
                "nunique",
            ),
            first_month=(
                "reporting_month",
                "min",
            ),
            last_month=(
                "reporting_month",
                "max",
            ),
            organisation_name_count=(
                "org_name",
                "nunique",
            ),
            latest_org_name=(
                "org_name",
                "last",
            ),
        )
        .sort_values(
            [
                "months_present",
                "org_code",
            ],
            ascending=[
                False,
                True,
            ],
        )
        .reset_index(drop=True)
    )

    return result
