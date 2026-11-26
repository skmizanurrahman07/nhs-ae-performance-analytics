"""Build controlled analytical output tables."""

from pathlib import Path

import pandas as pd

from nhs_ae.analysis.monthly_trends import (
    build_monthly_approved_kpis,
)
from nhs_ae.analysis.pressure_trends import (
    build_monthly_pressure_trends,
)
from nhs_ae.analysis.provider_changes import (
    compare_provider_periods,
)
from nhs_ae.analysis.provider_pressure import (
    compare_provider_pressure,
)
from nhs_ae.analysis.provider_trends import (
    summarise_provider_kpis,
)
from nhs_ae.transformation.kpi_features import (
    derive_approved_kpis,
)
from nhs_ae.transformation.pressure_features import (
    derive_pressure_features,
)


def build_analytical_outputs(
    data: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """Build controlled tables from the master analytical dataset."""
    enriched = derive_approved_kpis(data)
    enriched = derive_pressure_features(enriched)

    monthly_kpis = build_monthly_approved_kpis(
        enriched
    )

    monthly_pressure = build_monthly_pressure_trends(
        enriched
    )

    provider_summary = summarise_provider_kpis(
        enriched
    )

    provider_change = compare_provider_periods(
        enriched,
        current_month="2026-09-01",
        comparison_month="2025-09-01",
        minimum_attendance_volume=10_000,
        full_period_months=25,
    )

    provider_pressure = compare_provider_pressure(
        enriched,
        current_month="2026-09-01",
        comparison_month="2025-09-01",
        minimum_attendance_volume=10_000,
        minimum_admission_volume=1_000,
        full_period_months=25,
    )

    return {
        "monthly_kpis": monthly_kpis,
        "monthly_pressure": monthly_pressure,
        "provider_summary": provider_summary,
        "provider_change": provider_change,
        "provider_pressure": provider_pressure,
    }


def write_analytical_outputs(
    outputs: dict[str, pd.DataFrame],
    output_dir: Path,
) -> list[Path]:
    """Write controlled analytical tables to CSV."""
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    paths: list[Path] = []

    for name, table in outputs.items():
        path = output_dir / f"{name}.csv"

        table.to_csv(
            path,
            index=False,
        )

        paths.append(path)

    return paths
