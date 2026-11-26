"""Integration tests for Power BI analytical model outputs."""

from pathlib import Path

import pandas as pd

ANALYTICAL_DIR = Path("data/analytical")


def test_powerbi_model_outputs() -> None:
    """Validate Power BI model tables, keys, and relationships."""
    dim_date = pd.read_csv(
        ANALYTICAL_DIR / "dim_date.csv",
        parse_dates=["date"],
    )

    dim_provider = pd.read_csv(
        ANALYTICAL_DIR / "dim_provider.csv"
    )

    fact_monthly_system = pd.read_csv(
        ANALYTICAL_DIR / "fact_monthly_system.csv",
        parse_dates=["reporting_month"],
    )

    fact_provider_monthly = pd.read_csv(
        ANALYTICAL_DIR
        / "provider_investigation_monthly.csv",
        parse_dates=["reporting_month"],
    )

    fact_provider_investigation = pd.read_csv(
        ANALYTICAL_DIR
        / "provider_investigation_priority.csv"
    )

    assert dim_date.shape == (731, 9)
    assert dim_provider.shape == (18, 4)
    assert fact_monthly_system.shape == (25, 19)
    assert fact_provider_monthly.shape == (450, 11)
    assert fact_provider_investigation.shape == (18, 13)

    assert dim_date["date"].is_unique
    assert dim_provider["org_code"].is_unique
    assert fact_monthly_system["reporting_month"].is_unique
    assert fact_provider_investigation["org_code"].is_unique

    assert not fact_provider_monthly.duplicated(
        ["reporting_month", "org_code"]
    ).any()

    date_keys = set(dim_date["date"])
    provider_keys = set(dim_provider["org_code"])

    assert set(
        fact_monthly_system["reporting_month"]
    ).issubset(date_keys)

    assert set(
        fact_provider_monthly["reporting_month"]
    ).issubset(date_keys)

    assert set(
        fact_provider_monthly["org_code"]
    ).issubset(provider_keys)

    assert set(
        fact_provider_investigation["org_code"]
    ).issubset(provider_keys)

    assert dim_date["date"].min() == pd.Timestamp(
        "2024-09-01"
    )

    assert dim_date["date"].max() == pd.Timestamp(
        "2026-09-01"
    )
