# Project Charter

## Project title

NHS England A&E Performance, Demand and Capacity Intelligence Platform

## Career objective

Create an interview-ready portfolio case study demonstrating that SK Mizanur
Rahman can apply existing business analysis, Python, SQL, Power BI, statistics,
data-quality, project-delivery and stakeholder-communication skills in an NHS
analytics context.

## Business context

Urgent and emergency care leaders require clear, timely and trustworthy
information about demand, emergency admissions, waiting performance, provider
variation and operational pressure. This portfolio project will use official,
publicly available aggregate data to create reproducible analysis and management
information.

## Problem statement

Published A&E information spans reporting periods, provider organisations and
service types. Decision-makers need the information transformed into consistent
metrics that reveal trends, benchmark providers and highlight areas requiring
further operational investigation.

## Project aim

Develop a reproducible analytics solution that measures A&E demand, admissions,
waiting-time performance and provider variation, with capacity analysis added
only after the core data model and quality controls are reliable.

## Objectives

1. Acquire and catalogue official aggregate data with full provenance.
2. Build repeatable Python ingestion, cleaning and validation components.
3. Create a tested SQL analytical layer and dimensional model.
4. Analyse national trends, seasonality and provider variation.
5. Build an accessible Power BI decision-support dashboard.
6. Communicate findings without making unsupported causal claims.
7. Maintain an evidence log for NHS applications and interviews.

## Primary users

- Urgent and emergency care operational managers
- Trust performance and information teams
- Business intelligence analysts
- Service-improvement teams
- Executive users requiring concise performance summaries

## In scope

- Official public aggregate NHS England A&E data
- Monthly provider and system-level analysis
- A&E demand, emergency admissions and waiting performance
- Provider benchmarking and time-series analysis
- Data profiling, validation and reconciliation
- Python, SQL, DuckDB and Power BI deliverables
- Methodology, data dictionary and limitations documentation

## Out of scope for the first release

- Patient-level records
- Clinical decision-making
- Individual patient risk prediction
- Causal attribution
- Real-time operational deployment
- Automated trading-style prediction or deep learning
- Unvalidated capacity or workforce integration

## Deliverables

- Project and stakeholder documentation
- Dataset register and data dictionary
- Python ETL and data-quality package
- DuckDB analytical database and SQL views
- Exploratory and statistical notebooks
- Power BI semantic model and dashboard
- Executive insight report
- Technical README and reproducibility guide
- NHS competency evidence log

## Success criteria

- Every published KPI has a documented definition and calculation.
- Raw data remains immutable and traceable to its source.
- Critical validation checks pass before analytical outputs are refreshed.
- Transformations are reproducible from documented commands.
- Automated tests cover critical business rules.
- Dashboard figures reconcile to validated analytical outputs.
- Insights distinguish observation, interpretation and recommendation.
- A hiring manager can understand the project without reading source code.

## Constraints and assumptions

- Source formats and column names may change between publications.
- Source mappings are controlled through the profiled source-data dictionary, transformation rules and validation framework.
- Aggregate statistics cannot explain individual patient outcomes.
- Comparisons require attention to reporting changes and missing submissions.
- Capacity associations must not be described as causal effects.

## Governance principles

- Use only lawful, public, aggregate information.
- Retain source URLs, publication dates and retrieval dates.
- Do not store personal or confidential information.
- Document revisions, limitations and transformation decisions.
- Apply data minimisation and purpose limitation.

## Initial-stage exit criteria

- Repository structure created.
- Charter approved as the working baseline.
- Functional and non-functional requirements documented.
- Stakeholder personas and user stories recorded.
- Analytical questions prioritised.
- KPI catalogue represented in documentation and tested Python objects.

## Current implementation status

The core analytical solution has progressed beyond the initial project-definition stage.

Implemented components include:

- controlled acquisition and provenance of 25 consecutive monthly source files from September 2024 through September 2026;
- repeatable Python ingestion, transformation, validation and reconciliation;
- immutable raw-data retention and processed provider-month analytical data;
- a persistent DuckDB analytical database;
- tested SQL schema and analytical views;
- reproducible Jupyter notebooks for system trends, provider variation and operational-pressure investigation;
- a Power BI star-schema semantic model and decision-support dashboard;
- automated unit, database and integration testing;
- reconciliation and dashboard QA before portfolio documentation.

The remaining work is focused on documentation reconciliation, reproducibility guidance, executive communication and final portfolio presentation.
