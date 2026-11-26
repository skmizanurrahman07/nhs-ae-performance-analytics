# NHS A&E Analytics Reproducibility Runbook

## 1. Purpose

This runbook documents the reproducible execution path for the NHS A&E
Performance, Demand and Capacity Analytics project.

The controlled workflow rebuilds the analytical data layer from registered raw
monthly source files through validated provider-level data, the combined
25-month master dataset, the persistent DuckDB analytical database and the
version-controlled SQL analytical views.

## 2. Controlled analytical period

The analytical dataset covers 25 consecutive reporting months:

- Start: September 2024
- End: September 2026
- Expected months: 25
- Expected provider-month rows: 4,918
- Expected provider codes: 207
- Expected duplicate provider-month keys: 0

The controlled master dataset is:

`data/processed/nhs_ae_provider_2024_09_to_2026_09.csv`

The persistent analytical database is:

`data/database/nhs_ae.duckdb`

## 3. Architecture

The reproducible analytical sequence is:

1. Controlled NHS monthly raw source files
2. Source manifest and provenance controls
3. Python transformation and validation
4. Monthly provider-level reconciliation
5. Validated 25-month master dataset
6. Persistent DuckDB analytical database
7. Version-controlled SQL schema and analytical views
8. Jupyter analytical investigation
9. Power BI decision-support reporting

Python is the engineering and quality-control layer.

DuckDB and SQL provide the reusable analytical layer.

Jupyter notebooks provide the exploratory and statistical analysis layer.

Power BI provides the decision-support presentation layer.

## 4. Controlled source manifest

The workflow uses:

`config/source_manifest_2024_09_to_2026_09.json`

Each registered source includes controlled metadata such as:

- source identifier;
- raw source file path;
- reporting period;
- file size;
- SHA-256 checksum;
- ingestion timestamp.

Raw source files are retained under:

`data/raw/`

## 5. Reusable workflow implementation

The orchestration layer is:

`src/nhs_ae/workflow.py`

The workflow coordinates existing tested project components rather than
duplicating transformation or validation logic.

The controlled processing sequence is:

`run_provider_pipeline()`

→ `combine_monthly_provider_data()`

→ `write_processed_csv()`

→ `build_database()`

Monthly provider processing performs transformation and reconciliation before
writing validated provider data.

The multi-month stage verifies the expected reporting-month sequence, schema
consistency and provider-month key uniqueness.

The database stage recreates the persistent analytical database from the
validated master dataset and executes the version-controlled SQL schema and
views.

## 6. SQL analytical layer

The database build executes:

`sql/schema/001_core_tables.sql`

followed by:

- `sql/views/001_monthly_kpis.sql`
- `sql/views/002_monthly_pressure.sql`
- `sql/views/003_provider_summary.sql`
- `sql/views/004_provider_change.sql`
- `sql/views/005_provider_pressure.sql`

Database construction validates the expected analytical invariants before the
build is accepted.

## 7. Development environment

From the repository root in Windows PowerShell:

1. Create the virtual environment with `py -3.12 -m venv .venv`.
2. Activate it with `.\.venv\Scripts\Activate.ps1`.
3. Upgrade pip with `python -m pip install --upgrade pip`.
4. Install dependencies with `pip install -e ".[dev,analysis]"`.

## 8. Quality gates

Run the following commands from the activated environment:

- `ruff check .`
- `python -m mypy`
- `pytest`

The use of `python -m mypy` is the controlled project command for type checking.

The workflow is covered by unit and integration tests, including an end-to-end
rebuild against temporary outputs.

## 9. Controlled production rebuild

The reusable Python entry point is `run_workflow()` from
`nhs_ae.workflow`.

A controlled rebuild can be invoked from Python as follows:

    from nhs_ae.workflow import run_workflow

    run_workflow()

With default configuration, this uses the controlled 25-month manifest, writes
the validated master dataset to the configured processed-data location and
rebuilds the configured DuckDB analytical database.

A production rebuild should be performed only after the automated quality gates
pass.

## 10. Validation controls

The workflow and analytical database enforce critical controls including:

- monthly transformation validation;
- reconciliation against published TOTAL records;
- consistent analytical schema;
- complete September 2024 to September 2026 reporting sequence;
- unique provider-month business keys;
- 4,918 expected provider-month rows;
- 25 expected reporting months;
- 207 expected provider codes;
- zero duplicate provider-month keys;
- successful SQL schema and analytical-view creation.

A failed critical validation prevents successful completion of the controlled
build.

## 11. Notebook layer

The established analytical notebook sequence is:

1. `notebooks/01_source_data_profile.ipynb`
2. `notebooks/02_system_performance_trends.ipynb`
3. `notebooks/03_provider_variation_and_change.ipynb`
4. `notebooks/04_provider_pressure_investigation.ipynb`

Notebooks consume controlled analytical outputs and are not substitutes for
reusable engineering, validation or SQL logic.

## 12. Power BI layer

Power BI is the decision-support presentation layer built on the governed
analytical model.

KPI definitions implemented in Power BI must remain consistent with approved
Python and SQL definitions.

Material differences between platforms must be investigated rather than
accepted as tooling or rounding differences without evidence.

## 13. Reproducibility principle

PowerShell is used as the execution and quality-control interface.

Reusable analytical implementation belongs in version-controlled project
artefacts such as:

- `src/`
- `sql/`
- `tests/`
- `notebooks/`

Temporary PowerShell analysis must not replace the controlled analytical
implementation.
