# Business Requirements Document

## Business need

Turn official A&E statistics into reliable, accessible intelligence that helps a
manager identify changes in demand, admissions and waiting performance and then
select providers or periods for deeper investigation.

## Functional requirements

- **FR-001 Source registration:** Record source owner, title, URL, reporting
  period, retrieval date, licence and file checksum.
- **FR-002 Data ingestion:** Load supported official spreadsheet or CSV files
  without modifying the originals.
- **FR-003 Schema validation:** Detect missing, renamed or unexpected fields.
- **FR-004 Quality controls:** Test completeness, uniqueness, validity,
  consistency and reconciliation.
- **FR-005 Standardisation:** Standardise dates, provider identifiers, service
  types and numeric measures.
- **FR-006 Metric calculation:** Calculate only approved KPI definitions.
- **FR-007 Trend analysis:** Support monthly, year-on-year and rolling analysis.
- **FR-008 Benchmarking:** Compare a selected provider with national and
  appropriate peer distributions.
- **FR-009 Drill-down:** Filter by period, provider, system and A&E type when
  supported by the data.
- **FR-010 Auditability:** Trace a dashboard value back to its analytical table
  and source file.
- **FR-011 Export:** Produce quality reports and curated analytical datasets.
- **FR-012 Refresh control:** Prevent publication when critical checks fail.

## Non-functional requirements

- **NFR-001 Accuracy:** Published values must reconcile to validated outputs.
- **NFR-002 Reproducibility:** A documented command must rebuild curated data.
- **NFR-003 Maintainability:** Python follows PEP 8, typing and modular design.
- **NFR-004 Testability:** Business rules are separated from input/output code.
- **NFR-005 Performance:** Local refreshes should use columnar storage and SQL.
- **NFR-006 Security:** No patient-identifiable or confidential data.
- **NFR-007 Accessibility:** Visuals use clear labels, readable contrast and do
  not rely on colour alone.
- **NFR-008 Transparency:** Definitions, sources and limitations are visible.
- **NFR-009 Portability:** The project runs locally with Python 3.12.
- **NFR-010 Version control:** Code and documentation changes are traceable.

## Acceptance criteria

1. Given a registered source, the pipeline records its lineage metadata.
2. Given an invalid schema, ingestion stops with a clear error.
3. Given duplicate business keys, validation reports failed rows.
4. Given valid curated data, all approved KPI functions return bounded values.
5. Given a selected provider and period, dashboard filters update consistently.
6. Given a critical quality failure, the release status is blocked.
7. Given a dashboard KPI, documentation identifies its formula and caveats.

## Business rules

- Counts cannot be negative.
- Percentages must fall between 0 and 100 inclusive.
- Rates cannot be calculated when their denominator is zero.
- Missing values must not be silently converted to zero.
- Provider names are descriptive; stable identifiers should be used for joins.
- Source totals and calculated totals must be reconciled where possible.
- Year-on-year analysis requires comparable reporting periods.

## Risks and controls

| Risk | Control |
|---|---|
| Source layout changes | Schema contracts and versioned adapters |
| Misinterpreted measures | KPI catalogue and domain review |
| Incorrect provider joins | Reference dimensions and exception reports |
| Missing submissions | Completeness checks and dashboard warnings |
| False causal conclusions | Cautious language and limitations section |
| Portfolio overengineering | Stage gates and prioritised backlog |
