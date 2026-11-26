# NHS A&E Performance, Demand and Capacity Analytics Case Study

## 1. Executive summary

This project demonstrates an end-to-end analytical solution for NHS Accident
and Emergency performance, demand and operational-pressure analysis using
official aggregate monthly data.

The solution covers 25 consecutive reporting months from September 2024
through September 2026 and combines controlled Python data engineering, data
quality assurance, DuckDB, reusable SQL, Jupyter analytical investigation and
Power BI decision-support reporting.

The objective is not simply to produce a dashboard. The project establishes a
traceable analytical chain from source data through validated transformation,
governed KPI logic, longitudinal analysis, provider investigation and
presentation.

## 2. Business problem

Urgent and emergency care decision-makers require reliable information about:

- changes in A&E demand;
- emergency admission activity;
- four-hour breaches;
- waits following a decision to admit;
- variation between providers;
- changes in operational pressure over time.

Aggregate operational data can support investigation and prioritisation, but
provider variation must not automatically be interpreted as evidence of
causation or individual-provider failure.

Accordingly, this project separates descriptive and diagnostic analytical
signals from causal conclusions.

## 3. Analytical scope

The controlled analytical period is September 2024 through September 2026.

The validated provider-month dataset contains:

- 25 reporting months;
- 4,918 provider-month records;
- 207 provider codes;
- 23 analytical columns;
- zero duplicate provider-month business keys.

Published TOTAL records are excluded from provider-level analytical records
and retained for reconciliation control.

## 4. Analytical architecture

The implemented architecture is:

NHS monthly source files

→ Python engineering and quality assurance

→ validated 25-month provider dataset

→ DuckDB analytical database

→ reusable SQL analytical views

→ Jupyter analytical investigation

→ Power BI decision-support reporting

Python provides the engineering and quality-control layer.

DuckDB and SQL provide the reusable analytical layer.

Jupyter provides the exploratory and statistical investigation layer.

Power BI provides the decision-support presentation layer.

## 5. Data engineering and governance

The project implements controlled processes for:

- source registration and provenance;
- SHA-256 integrity checks;
- immutable raw-data retention;
- schema validation;
- identifier validation;
- controlled numeric transformation;
- provider-month key validation;
- negative-value controls;
- published-total reconciliation;
- multi-month dataset assembly;
- automated testing;
- database validation.

A reusable workflow coordinates the controlled 25-month rebuild through
existing tested transformation, reconciliation, combination and database
components.

## 6. System-level analytical findings

### Demand

Total A&E attendances increased from 2,214,217 in September 2024 to 2,444,743
in September 2026.

For September 2026, total attendances were 5.82% higher than September 2025
and 4.34% higher than the immediately preceding month.

This indicates substantially stronger attendance growth at the end of the
analytical period than the corresponding growth in emergency admissions.

### Emergency admissions

Emergency admissions were 530,824 in September 2024 and 536,158 in September
2026.

For September 2026, emergency admissions were approximately 0.11% higher than
September 2025 and 3.53% higher than the immediately preceding month.

The demand and admission series therefore show different longitudinal
patterns and should not be treated as interchangeable indicators of pressure.

## 7. Waiting and operational-pressure findings

Four-hour breaches were 570,888 in September 2024 and 626,751 in September
2026.

September 2026 four-hour breaches were approximately:

- 8.74% higher than September 2025;
- 7.18% higher than the immediately preceding month.

Decision-to-admit waits of 12 hours or more increased from 38,880 in September
2024 to 50,582 in September 2026.

For September 2026, 12-hour-plus decision-to-admit waits were approximately:

- 12.99% higher than September 2025;
- 12.53% higher than the immediately preceding month.

By contrast, decision-to-admit waits between 4 and 12 hours were 6.67% lower
than September 2025.

Total decision-to-admit waits of four hours or more were broadly stable
year-on-year in September 2026, increasing by approximately 0.15%, while their
composition shifted toward the 12-hour-plus category.

This distinction demonstrates why aggregate waiting totals alone can conceal
changes in the severity profile of operational pressure.

## 8. Provider investigation

The controlled provider-investigation output contains 18 prioritised provider
records.

The investigation framework uses indicators including:

- absolute changes in four-hour breaches;
- absolute changes in 12-hour-plus decision-to-admit waits;
- recent six-month slopes;
- persistence above analytical medians;
- robust-outlier indicators;
- investigation-priority scoring.

The highest-priority records include providers classified as experiencing
dual pressure, where both breach and long-wait indicators support further
investigation.

The priority output is an analytical triage mechanism. It does not establish
causation, quality failure or organisational performance judgement.

Provider context, reporting characteristics, service configuration and other
relevant evidence would be required before drawing operational conclusions.

## 9. Example investigation signals

Mid and South Essex NHS Foundation Trust is classified in the controlled
output as a High-priority dual-pressure investigation candidate.

Its analytical record contains:

- four-hour breach absolute change: +2,446;
- 12-hour-plus DTA wait absolute change: +888;
- 12 months above the breach median;
- 12 months above the DTA median;
- robust-outlier flag: true;
- investigation-priority score: 7.

Bristol NHS Foundation Trust, Maidstone and Tunbridge Wells NHS Trust and
Nottingham University Hospitals NHS Trust also appear in the High-priority
dual-pressure segment in the controlled investigation output.

These records identify where analysts may investigate further. They are not
causal conclusions.

## 10. Analytical model and reporting

The Power BI reporting layer is supported by a dimensional model containing
system-level and provider-level analytical structures.

The dashboard supports analysis of:

- system performance;
- demand and admissions;
- trends and change;
- waits and flow;
- provider variation;
- investigation signals.

KPI definitions are governed so that Python, SQL and Power BI implementations
remain analytically consistent.

## 11. Reproducibility and testing

The project includes a reusable orchestration layer capable of rebuilding the
controlled analytical stack from the registered monthly raw files.

Automated validation includes unit, integration and database testing.

At the final orchestration QA checkpoint:

- Ruff linting passed;
- mypy reported no issues across 72 source files;
- 138 automated tests passed;
- the end-to-end workflow successfully rebuilt temporary analytical outputs.

The production analytical dataset and database remain protected from temporary
workflow-validation outputs.

## 12. Analytical limitations

The project uses aggregate monthly information.

Consequently:

- results cannot explain individual patient outcomes;
- provider comparisons require contextual interpretation;
- organisational changes may affect longitudinal comparison;
- association does not demonstrate causation;
- investigation-priority scores are analytical signals rather than performance
  judgements;
- controlled KPI definitions must be respected when interpreting outputs.

The analysis therefore supports structured investigation and decision support
rather than unsupported causal attribution.

## 13. Skills demonstrated

The project demonstrates practical capability in:

- healthcare analytics;
- Python engineering;
- pandas data transformation;
- data-quality design;
- validation and reconciliation;
- longitudinal analysis;
- DuckDB;
- SQL analytical modelling;
- Jupyter notebooks;
- provider-level investigation;
- Power BI;
- DAX governance;
- automated testing;
- analytical documentation;
- reproducible workflow design;
- stakeholder-focused communication.

## 14. Portfolio value

This project demonstrates the ability to take an analytical problem from
business requirements through controlled data engineering, validated analysis
and decision-support reporting.

Its emphasis is on evidence quality, reproducibility and analytical
traceability rather than producing visualisations in isolation.

The resulting portfolio case study provides practical evidence of capability
across the analytical lifecycle while maintaining appropriate governance and
interpretation of aggregate NHS data.
