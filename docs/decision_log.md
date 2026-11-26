# Decision Log

| ID | Decision | Rationale | Status |
|---|---|---|---|
| DEC-001 | Use Python 3.12 | Stable modern typing and package support | Approved |
| DEC-002 | Use a `src` package layout | Reduces accidental local imports | Approved |
| DEC-003 | Use DuckDB for local analytics | Suitable for local SQL and columnar files | Approved |
| DEC-004 | Keep KPI source mappings provisional | Real files must be profiled first | Superseded |
| DEC-005 | Prioritise descriptive/diagnostic analysis | Better aligned to initial NHS role evidence | Approved |

| DEC-006 | Lock analytical dataset to 25 consecutive months, September 2024 to September 2026 | Provides a controlled longitudinal window supporting monthly, year-on-year and rolling analysis | Approved |
| DEC-007 | Preserve immutable raw source files and record provenance and SHA-256 checksums | Ensures source integrity, traceability and reproducibility | Approved |
| DEC-008 | Exclude published TOTAL rows from provider-level analytical records and use them for reconciliation | Prevents double counting while retaining an authoritative control total | Approved |
| DEC-009 | Reconcile transformed provider measures against published totals before analytical use | Provides a controlled quality gate between transformation and downstream analysis | Approved |
| DEC-010 | Build a persistent DuckDB analytical database after Python engineering and validation | Separates validated data engineering from the reusable analytical SQL layer | Approved |
| DEC-011 | Implement reusable SQL analytical views for monthly KPIs, monthly pressure, provider summary, provider change and provider pressure | Provides governed and reproducible analytical datasets for downstream analysis | Approved |
| DEC-012 | Reconcile SQL analytical outputs with validated Python outputs | Ensures consistency between engineering and analytical layers | Approved |
| DEC-013 | Use Jupyter notebooks as the exploratory and statistical analysis layer after DuckDB and SQL | Keeps investigation reproducible while preserving the established analytical architecture | Approved |
| DEC-014 | Use a Power BI star-schema semantic model for dashboard reporting | Separates dimensions and facts and supports controlled filtering, KPI reporting and provider analysis | Approved |
| DEC-015 | Use only approved or explicitly controlled KPI definitions in production Python, SQL and Power BI outputs | Prevents provisional measures from being presented as governed analytical results | Approved |
| DEC-016 | Treat provider rankings and pressure indicators as investigation signals rather than causal evidence | Maintains appropriate interpretation of aggregate NHS performance data | Approved |
| DEC-017 | Complete dashboard QA and reconciliation before portfolio documentation and presentation | Ensures portfolio claims are based on validated analytical outputs | Approved |

