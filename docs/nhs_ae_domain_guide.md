# NHS A&E Domain Guide

## 1. Purpose

This document defines the NHS urgent and emergency care concepts required to
interpret the project's A&E performance, demand, and flow analysis correctly.

The guide provides the domain context used by the project's data dictionary,
KPI definitions, validation rules, transformation logic, SQL analysis,
statistical analysis, and Power BI reporting.

The guide should be read alongside the technical documentation rather than
used as a substitute for current NHS England definitions and guidance.

---

## 2. Dataset and collection context

The project currently uses the NHS England Monthly A&E Attendances and
Emergency Admissions collection as its primary A&E activity and performance
source.

The collection reports the total number of attendances during the specified
period across A&E types, including urgent treatment centres, minor injury
units, and walk-in centres.

The collection also covers:

- attendances discharged, admitted, or transferred within four hours of
  arrival;
- emergency admissions;
- waits of more than four hours for admission following decision to admit.

The published data are available at provider organisation level and include
NHS trusts, NHS foundation trusts, and independent-sector organisations.

### Analytical significance

The source is aggregate operational reporting data rather than individual
patient-level data.

Consequently, analysis using the Monthly A&E source should focus on
provider-level activity, performance, variation, trends, and benchmarking
that can be supported by the published fields.

Patient-level questions requiring characteristics such as diagnosis or age
cannot be answered from this Monthly A&E source alone.

### Current project source

The initial development source is the September 2026 monthly A&E publication.

The project preserves the downloaded raw source unchanged and records source
provenance, file integrity, schema validation, and reconciliation before
transformation.
---

## 3. A&E department types

NHS A&E activity is reported across different emergency-care department
types. These categories represent different service models and should not be
treated as operationally identical when interpreting activity or performance.

### Type 1 A&E department

A Type 1 department is a consultant-led, 24-hour emergency service with full
resuscitation facilities and designated accommodation for receiving accident
and emergency patients.

Type 1 departments are increasingly referred to as Emergency Departments.

### Type 2 A&E department

A Type 2 department is a consultant-led single-service or specialty Emergency
Department, such as ophthalmology or dental emergency care, with designated
accommodation for receiving patients.

### Type 3 A&E department

Type 3 departments are referred to as Urgent Treatment Centres (UTCs).

UTCs are GP-led, open for at least 12 hours each day, allow appointments to be
booked through NHS 111 or GP referral, and are equipped to diagnose and manage
many common conditions for which people attend A&E.

### Other A&E departments

The NHS England technical specification notes that some non-UTC facilities,
including Minor Injury Units, Urgent Care Centres and Walk-In Centres, may
continue to operate under transitional arrangements.

The project's source data contains fields labelled:

- `A&E attendances Type 1`
- `A&E attendances Type 2`
- `A&E attendances Other A&E Department`

The analytical model will preserve the terminology used by the published
source rather than automatically relabelling `Other A&E Department` as
Type 3 until the relevant source definition and reporting treatment have been
verified.

### Analytical interpretation

Department type is important because different emergency-care service models
may have different activity profiles and operational characteristics.

Therefore:

- Type 1, Type 2 and Other A&E activity should remain separately identifiable;
- comparisons between department types should acknowledge differences in
  service model;
- aggregated activity across department types should be explicitly labelled;
- the source terminology should be preserved through the raw-data layer;
- transformations must not silently substitute one department-type definition
  for another.
---

## 4. A&E attendance concept

An A&E attendance represents an attendance at an emergency-care department
within the scope of the NHS A&E reporting definition.

For the ECDS A&E Activity and Performance specification, an A&E attendance is
defined as an unplanned attendance at an emergency-care department.

Attendances are counted against the date on which the patient departs the
emergency-care department.

Where a patient is streamed between departments on the same site, only the
attendance at the final department is counted. The original arrival date and
time are carried forward through subsequent records.

### Planned follow-up attendances

The ECDS technical specification excludes planned follow-up attendances within
seven days of the first attendance at the same department from the unplanned
attendance measure.

The Monthly A&E source used by this project also contains separate booked-
appointment fields. These fields must therefore remain separately identifiable
until their exact relationship with attendance and performance denominators
has been established from the applicable source guidance.

### Project source fields

The current source contains:

- `A&E attendances Type 1`
- `A&E attendances Type 2`
- `A&E attendances Other A&E Department`
- `A&E attendances Booked Appointments Type 1`
- `A&E attendances Booked Appointments Type 2`
- `A&E attendances Booked Appointments Other Department`

### Analytical interpretation

An attendance is an activity event, not necessarily a unique patient.

Therefore, this project must not interpret a count of A&E attendances as a
count of distinct people unless a separate patient-level source explicitly
supports that interpretation.

Attendance measures will remain separated by department type where required.
Any combined attendance KPI must document exactly which source fields are
included.

Booked-appointment activity will not automatically be added to or removed from
other attendance measures until the applicable reporting definition has been
confirmed and encoded in the KPI dictionary.
---

## 5. Four-hour A&E performance

Four-hour A&E performance describes whether applicable A&E attendances are
completed within four hours of arrival.

For the NHS England monthly A&E collection, the published activity includes
the number of attendances discharged, admitted, or transferred within four
hours of arrival.

The project source provides four-hour breach counts rather than a
pre-calculated performance percentage.

### Project source fields

The current source contains:

- `Attendances over 4hrs Type 1`
- `Attendances over 4hrs Type 2`
- `Attendances over 4hrs Other Department`
- `Attendances over 4hrs Booked Appointments Type 1`
- `Attendances over 4hrs Booked Appointments Type 2`
- `Attendances over 4hrs Booked Appointments Other Department`

### Conceptual calculation

Where the numerator and denominator definitions have been confirmed as
compatible, a four-hour performance percentage can be expressed as:

`Four-hour performance (%) = ((Attendances - Four-hour breaches) / Attendances) × 100`

Equivalently:

`Four-hour performance (%) = 100 - Four-hour breach rate (%)`

This formula will not be implemented as an approved project KPI until the
project KPI dictionary confirms exactly which attendance and breach fields
belong in the numerator and denominator.

### Division-by-zero rule

If the applicable attendance denominator is zero, the performance percentage
must not be calculated by dividing by zero.

The project's KPI specification must define an explicit treatment for this
case before implementation.

### Analytical interpretation

Higher four-hour performance indicates a greater proportion of applicable
attendances completed within four hours.

However, the metric should not be interpreted in isolation as a complete
measure of emergency-care quality.

Performance should be analysed alongside measures such as:

- attendance demand;
- emergency admissions;
- long waits following decision to admit;
- provider type and service model;
- relevant operational context.

### Comparability caution

Comparisons across time must account for changes in reporting methodology,
provider footprint, and published definitions.

Where NHS England changes the reporting basis of a performance metric, the
project must document the change before comparing affected periods.
---

## 6. Decision to Admit (DTA) waits

Decision to Admit (DTA) measures relate to the period after a clinical
decision has been made to admit a patient from A&E and before the patient is
admitted.

This represents a different part of the patient pathway from the general
four-hour A&E attendance measure and must therefore be analysed separately.

### Project source fields

The current source contains:

- `Patients who have waited 4-12 hs from DTA to admission`
- `Patients who have waited 12+ hrs from DTA to admission`

These fields represent counts of patients experiencing long waits between the
decision to admit and admission.

### Analytical interpretation

The DTA measures should not be treated as equivalent to general A&E
four-hour breaches.

The distinction is:

`A&E four-hour measure`

relates to time in the A&E pathway from arrival until the relevant departure
outcome.

Whereas:

`DTA wait`

relates specifically to the period following the decision to admit and before
admission.

Therefore, the project will maintain DTA measures separately from general
four-hour A&E performance measures.

### Long-wait categories

The source distinguishes:

- waits of 4 to 12 hours from DTA to admission;
- waits of 12 hours or more from DTA to admission.

These categories will remain separately identifiable in the analytical
dataset and reporting model.

### Analytical caution

A DTA long-wait count is an operational flow measure.

The aggregate monthly source does not by itself explain why a DTA delay
occurred. Possible explanatory relationships with demand, admissions, or
capacity must be investigated analytically and should not be interpreted as
causal without appropriate evidence.
---

## 7. Emergency admissions

Emergency admissions represent admissions to hospital that occur on an
emergency rather than planned basis.

The Monthly A&E Attendances and Emergency Admissions collection reports
emergency-admission activity alongside A&E attendance and waiting-time
measures.

### Project source fields

The current project source contains:

- `Emergency admissions via A&E - Type 1`
- `Emergency admissions via A&E - Type 2`
- `Emergency admissions via A&E - Other A&E department`
- `Other emergency admissions`

### Emergency admissions via A&E

The first three fields describe emergency admissions recorded through the
different A&E department categories represented in the published source.

These measures should remain separately identifiable by department type
before any combined emergency-admission measure is produced.

### Other emergency admissions

The source also contains `Other emergency admissions`.

This field must remain separate from admissions explicitly identified as
being via A&E until its applicable NHS reporting definition has been verified
and documented in the project data and KPI dictionaries.

### Analytical interpretation

Emergency-admission activity is related to, but analytically distinct from,
A&E attendance activity.

The project must therefore avoid assuming that:

- every A&E attendance results in an admission;
- every emergency admission comes through an A&E department;
- an emergency-admission count represents a unique patient without
  patient-level evidence.

Any admission-rate KPI will require an explicitly documented numerator and
denominator before implementation.

### Example analytical relationship

A potential measure for later validation is:

`Emergency admission rate (%) = Emergency admissions via A&E / applicable A&E attendances × 100`

This formula is provisional.

The final KPI must be approved in the KPI dictionary only after confirming
which admission and attendance fields are methodologically compatible.
---

## 8. Booked A&E appointments

Booked appointments form part of the NHS A&E reporting context and must be
distinguished explicitly when analysing attendance and four-hour performance.

NHS England introduced booked-appointment reporting into the monthly A&E
collection from August 2020.

From that point, published attendance figures include booked appointments in
emergency departments. Before this change, booked appointments were not
counted within A&E attendance figures.

### Project source fields

The current source includes booked-appointment activity separately for each
published department category:

- `A&E attendances Booked Appointments Type 1`
- `A&E attendances Booked Appointments Type 2`
- `A&E attendances Booked Appointments Other Department`

The source also provides corresponding four-hour breach fields:

- `Attendances over 4hrs Booked Appointments Type 1`
- `Attendances over 4hrs Booked Appointments Type 2`
- `Attendances over 4hrs Booked Appointments Other Department`

### Analytical treatment

Booked appointments must not automatically be added to total A&E attendance
fields.

The published attendance totals may already include booked appointments.
Adding the booked-appointment fields again could therefore double-count
activity.

The same caution applies when constructing four-hour performance measures.

### Project rule

Until the KPI dictionary formally establishes each denominator and numerator:

- booked-appointment fields will remain separately identifiable;
- booked appointments will not be added to published attendance totals;
- booked-appointment breaches will not be added to published breach totals
  without confirming whether they are already included;
- any KPI using booked-appointment fields must document the calculation
  explicitly.

### Historical comparability

Booked appointments create an important historical comparability issue because
the published attendance definition changed from August 2020.

Long-term trend analysis spanning this change must therefore document the
methodological break and avoid assuming that pre-August-2020 and
post-August-2020 attendance figures are directly comparable without
qualification.
---

## 9. Provider and system structure

The Monthly A&E Attendances and Emergency Admissions publication provides
activity and performance information at provider-organisation level and also
publishes information by System.

The provider-level source used by this project contains organisation
identifiers that allow each published provider record to remain separately
identifiable.

### Project source identifiers

The current source contains:

- `Org Code`
- `Org name`
- `Parent Org`

### Organisation code

`Org Code` is retained as the primary provider identifier in the analytical
dataset.

Organisation names are useful descriptive labels, but the project will not
use organisation name alone as the provider key.

### Organisation name

`Org name` provides the published descriptive organisation name associated
with the provider record.

The project has already validated that, within the September 2026 source:

- each provider organisation code maps to one organisation name;
- each organisation name maps to one provider organisation code.

These relationships will be checked again when multiple reporting months are
combined because organisation names and structures may change over time.

### Parent organisation

`Parent Org` provides the higher-level organisation grouping supplied in the
project's provider-level source.

The September 2026 source profiling identified seven distinct `Parent Org`
values across provider records.

The raw `Parent Org` field also contains trailing whitespace in some records.
The raw values will remain unchanged, while the ETL pipeline will apply the
documented controlled whitespace standardisation before analytical grouping
or joining.

### Provider-level analytical grain

For the current single-month source, the candidate provider-level business
key is:

`Period + Org Code`

This key was tested during source profiling and no duplicate provider records
were identified for September 2026.

The key must be revalidated after additional monthly files are introduced.

### Analytical interpretation

Provider-level and higher-level system or organisational analyses answer
different questions.

Provider-level analysis may be used for:

- provider performance assessment;
- provider benchmarking;
- identifying variation between organisations;
- investigating unusually high or low activity or performance.

Higher-level grouping may be used for:

- broader geographical or organisational summaries;
- comparison of aggregated activity;
- contextualising provider performance.

Aggregated results must always preserve the underlying analytical grain and
avoid double counting provider records.
---

## 10. Reporting periods and publication timing

The Monthly A&E Attendances and Emergency Admissions collection reports
activity for a calendar month.

The reporting period must be distinguished from the publication date.

For example, a monthly publication released in October may report A&E
activity for September.

### Project treatment

The analytical dataset will maintain separate concepts for:

- reporting period;
- publication or source-release information where available;
- file retrieval date;
- ingestion timestamp.

These dates serve different purposes and must not be treated as
interchangeable.

### Reporting period

The reporting period represents the period to which the healthcare activity
relates.

For the initial project source, the reporting period is September 2026.

The raw source expresses this as:

`MSitAE-SEPTEMBER-2026`

During controlled transformation, this value will be converted to a
standardised reporting-month field while preserving the raw value for
traceability.

### Publication timing

NHS England schedules regular monthly performance-statistics publications
after the reporting period has ended.

This means the date on which a file was published or downloaded is not the
same as the month represented by the activity data.

### Analytical implications

Time-series analysis must use the reporting period rather than:

- local file creation date;
- download date;
- ingestion timestamp;
- publication date.

Using the wrong date could shift activity into an incorrect month and distort
trend analysis, rolling calculations, month-on-month comparisons, and
year-on-year comparisons.

### Project rule

The future analytical model will contain a controlled reporting-month field
suitable for chronological sorting, joins to a date dimension, SQL time-series
analysis, and Power BI reporting.

The original raw reporting-period value will remain available for lineage and
audit purposes.
---

## 11. ECDS and the Monthly A&E SitRep

The Emergency Care Data Set (ECDS) and the Monthly A&E Attendances and
Emergency Admissions collection are related but distinct NHS data sources.

Understanding the difference is important when selecting data for an
analytical question.

### Monthly A&E SitRep

The Monthly A&E source currently used by this project is an aggregate
operational reporting source.

The project's provider-level monthly file contains aggregated measures such as:

- A&E attendances;
- booked A&E appointments;
- four-hour breaches;
- waits following decision to admit;
- emergency admissions.

The source supports provider-level activity, performance, trend, and
benchmarking analysis using the published aggregate measures.

### Emergency Care Data Set (ECDS)

ECDS is a patient-level emergency-care dataset.

NHS England publishes additional analysis derived from ECDS, including
information that is not available in the project's aggregate Monthly A&E
provider file.

Published ECDS analysis includes 12-hour-from-arrival information and can
include patient characteristics such as age, gender, ethnicity, and chief
complaint where applicable.

### Twelve-hour measures

A 12-hour measure from arrival at A&E is conceptually different from the
Monthly SitRep measure of a 12-hour wait following decision to admit.

These measures start their clocks at different points in the emergency-care
pathway and must not be treated as interchangeable.

### Project scope

The current core analytical pipeline uses the Monthly A&E provider-level
source.

ECDS will not be merged into the core dataset merely because both sources
describe emergency care.

If ECDS is introduced later, it will be treated as a separate source family
with its own:

- provenance;
- schema;
- grain;
- validation rules;
- data-quality assessment;
- KPI definitions;
- analytical limitations.

Only explicitly compatible measures will be compared or integrated.

### Analytical rule

The analytical question should determine the appropriate source.

Aggregate provider-performance questions may be addressed using the Monthly
A&E source.

Questions requiring patient characteristics or patient-level detail require a
source capable of supporting that level of analysis, such as ECDS.
---

## 12. Historical comparability

Long-term A&E analysis must account for changes in collection methodology,
definitions, and reporting structures.

A time series should not be assumed to contain perfectly comparable measures
simply because the same or similar field names appear across reporting
periods.

### Pre-June-2015 monthly data

Monthly A&E figures before June 2015 require particular caution.

NHS England provides estimated monthly figures for periods before June 2015
derived from the earlier weekly collection.

These historical monthly values should therefore be treated as estimates
rather than as directly observed monthly returns.

### Booked appointments

From August 2020, published A&E attendance figures include booked appointments
in emergency departments.

Previously, booked appointments were not counted within A&E attendance
figures.

Analysis spanning this methodological change must document the break in
comparability.

### Decision-to-admit definition changes

Historical guidance also contains changes to the scope of decision-to-admit
delay reporting.

Long-term analysis of DTA measures must therefore confirm that the definition
used in each period is methodologically comparable before calculating trends
or year-on-year changes.

### Provider and reporting structures

Provider structures, organisation names, organisation codes, system mappings,
and reporting footprints can change over time.

A change in provider-level activity may therefore reflect:

- genuine operational change;
- organisational restructuring;
- reporting-boundary changes;
- methodological changes;
- data-quality or coding changes.

These possibilities must be investigated before attributing observed changes
to service performance.

### Project rule

Before constructing a multi-year analytical time series, the project will
maintain a comparability register documenting known methodological and
structural changes.

Measures affected by a comparability break will be:

- clearly flagged;
- analysed within appropriate comparable periods where necessary;
- accompanied by methodological caveats;
- excluded from inappropriate trend calculations when comparability cannot
  be supported.

Historical continuity will never be assumed solely from identical column
names.
---

## 13. Data-quality considerations

NHS A&E analysis must distinguish between a published value and a value that
is analytically suitable for a particular comparison.

Published data should therefore be assessed for completeness, validity,
consistency, comparability, and appropriate coverage before use in performance
analysis.

### Provider completeness

Missing provider data can affect aggregate activity and performance measures.

A national or regional total based on an incomplete provider cohort may not be
directly comparable with a period containing the complete cohort.

The project will therefore assess provider coverage when multiple reporting
months are combined.

### Measure completeness

A provider may submit some activity fields while particular performance
measures are unavailable or affected by a reporting change.

The presence of a provider record must not therefore be interpreted as proof
that every analytical measure is complete and comparable.

### Schema quality

The project validates whether:

- required fields are present;
- unexpected fields are introduced;
- field order changes;
- expected numeric measures remain valid;
- identifiers remain usable.

Schema changes will be investigated before downstream processing.

### Identifier quality

Provider identifiers are assessed for:

- null values;
- blank values;
- whitespace-only values;
- unexpected surrounding whitespace;
- inconsistent organisation-code and organisation-name mappings;
- inconsistent parent-organisation mappings.

The September 2026 source contains a known formatting issue in `Parent Org`,
where trailing whitespace was identified in 167 provider records.

This issue is suitable for deterministic correction during ETL and does not
justify modifying the immutable raw source.

### Reconciliation

Where the published source contains an aggregate `TOTAL` record, provider-level
measure sums are reconciled against the published total before transformation.

For the September 2026 development source, all 18 controlled numeric measures
reconciled to the published `TOTAL` record.

### Validity checks

Controlled numeric activity measures are checked for invalid values such as
negative counts.

Additional domain-specific validity rules will be added only when supported by
the applicable measure definition.

### Comparability

Data-quality assessment includes whether the same measure remains comparable
across periods.

Changes in:

- definitions;
- provider coverage;
- reporting footprints;
- collection methodology;
- organisational structures;

may create breaks in comparability even where individual values are valid.

### Project principle

Data-quality checks are not intended merely to produce a pass/fail label.

The purpose is to determine whether data are:

1. suitable for analysis as published;
2. suitable after a documented controlled transformation;
3. suitable only with analytical caveats;
4. unsuitable for a particular analysis.

All material quality issues must remain traceable through the project
documentation and downstream reporting.
---

## 14. Analytical interpretation rules

The purpose of this project is not only to calculate A&E measures but to
interpret them appropriately for operational and management decision support.

Analytical conclusions must therefore distinguish between what the data show,
what the data may suggest, and what the available evidence cannot establish.

### Rule 1: Separate observation from explanation

An observed change in a measure does not by itself explain why the change
occurred.

For example:

`Four-hour performance decreased`

is an observation.

It does not automatically establish that the change was caused by:

- increased demand;
- reduced capacity;
- staffing pressures;
- higher admission demand;
- seasonal pressure.

Possible explanations must be investigated using appropriate additional
evidence.

### Rule 2: Association does not establish causation

If two measures move together, the project may describe an association where
supported by the analysis.

The project must not claim that one measure caused another unless the
analytical design and evidence support a causal conclusion.

### Rule 3: Always consider the denominator

Percentages and rates must be interpreted alongside the population or activity
volume from which they were calculated.

A performance percentage without its denominator may hide important
differences in scale between providers or reporting periods.

### Rule 4: Preserve analytical grain

Provider-level, system-level, regional, and national results represent
different analytical grains.

Results must not combine or compare incompatible grains without an explicitly
defined aggregation method.

### Rule 5: Check comparability before trend interpretation

Month-on-month, year-on-year, and long-term trends require comparable
definitions and provider coverage.

Known methodology, reporting-footprint, provider-cohort, or organisational
changes must be assessed before interpreting movement as genuine performance
change.

### Rule 6: Benchmarking requires context

Provider ranking alone does not explain why organisations differ.

Provider comparisons should consider:

- department type;
- activity volume;
- reporting coverage;
- organisational structure;
- methodological comparability;
- relevant operational context.

A ranking may identify where investigation is required, but it does not by
itself identify the cause of performance variation.

### Rule 7: Statistical significance and operational significance are different

A statistically detectable difference is not automatically operationally
important.

Where statistical methods are used, the project will consider both the
statistical evidence and the size and practical relevance of the observed
effect.

### Rule 8: Treat data-quality findings as analytical evidence

Missing records, inconsistent mappings, schema changes, and methodological
breaks are part of the analytical interpretation.

Data-quality limitations must not be hidden simply because a calculation can
still be produced.

### Rule 9: Report uncertainty and limitations

Material findings should state relevant limitations, including:

- source limitations;
- aggregation limitations;
- missing explanatory variables;
- comparability issues;
- assumptions;
- uncertainty in interpretation.

### Rule 10: Translate analysis into an operational question

Where appropriate, significant findings should be communicated using the
following structure:

**Observation**  
What happened?

**Evidence**  
How large was the change or difference?

**Context**  
Compared with what period, provider, benchmark, or distribution?

**Interpretation**  
What might the evidence indicate?

**Operational question**  
What should managers or analysts investigate further?

**Limitation**  
What cannot be concluded from the available data?
---

## 15. Known analytical limitations

The project's findings must be interpreted within the limitations of the
available data and reporting methodology.

These limitations do not necessarily prevent analysis, but they define what
the analysis can and cannot support.

### Aggregate-data limitation

The core Monthly A&E source contains aggregated provider-level measures rather
than individual patient records.

The source therefore cannot directly answer patient-level questions such as:

- how many distinct individual patients attended;
- patient-level pathways;
- diagnosis-specific outcomes;
- patient-level demographic differences;
- individual waiting-time distributions.

### Explanatory-variable limitation

The Monthly A&E source does not contain every factor that may contribute to
operational performance.

Observed variation may be associated with factors not represented in the
dataset.

The analysis must therefore avoid unsupported causal explanations.

### Provider-comparability limitation

Providers may differ in service configuration, activity volume, department
type, case mix, organisational structure, and reporting footprint.

Provider rankings and comparisons must therefore be interpreted as indicators
for further investigation rather than complete measures of organisational
quality.

### Historical-comparability limitation

Definitions, collection methods, provider cohorts, organisational structures,
and reporting footprints can change over time.

Long-term analysis must identify relevant comparability breaks before
calculating or interpreting trends.

### Missing-provider limitation

Where provider submissions are missing or particular measures are unavailable,
aggregate volumes and performance measures may be affected.

The provider cohort used for a comparison must therefore be checked when
completeness differs across periods or metrics.

### Data-revision limitation

Published NHS data may subsequently be revised.

The project therefore records source provenance and file integrity so that an
analysis can be linked to the exact version of the source that was used.

Where updated published data are adopted, the project should preserve an
auditable record of the change.

### Source-integration limitation

Measures from different NHS sources are not assumed to be interchangeable.

For example:

`12+ hours from decision to admit`

and:

`12+ hours from arrival`

represent different concepts.

Cross-source analysis requires explicit confirmation that definitions,
population coverage, analytical grain, and reporting periods are compatible.

### Statistical limitation

Statistical association does not establish causation.

Statistical significance also does not automatically imply operational
importance.

Where statistical methods are used, assumptions, effect size, uncertainty,
and practical significance will be reported alongside the result.

### Project principle

Every major analytical finding should be accompanied by sufficient context to
answer:

1. What does the data show?
2. What comparison supports the finding?
3. What might the finding indicate?
4. What cannot be concluded?
5. What additional evidence would strengthen the interpretation?
---

## 16. Domain knowledge quality gate

The NHS A&E domain guide is considered suitable to support the next stages of
the project when the following concepts have been documented and understood.

### Collection context

- [x] Purpose and scope of the Monthly A&E collection
- [x] Aggregate provider-level analytical grain
- [x] Difference between aggregate and patient-level data

### Emergency-care concepts

- [x] Type 1 A&E departments
- [x] Type 2 A&E departments
- [x] Type 3 / Urgent Treatment Centre context
- [x] A&E attendance concept
- [x] Booked appointments
- [x] Four-hour performance
- [x] Decision-to-admit waits
- [x] Emergency admissions

### Organisational and temporal context

- [x] Provider and higher-level organisational structure
- [x] Provider-period analytical grain
- [x] Reporting period versus publication date
- [x] Historical comparability considerations

### Source relationships

- [x] Monthly A&E SitRep versus ECDS
- [x] DTA 12-hour waits versus 12 hours from arrival
- [x] Cross-source compatibility must be established before integration

### Analytical governance

- [x] Data-quality considerations
- [x] Provider completeness
- [x] Published-data revisions
- [x] Observation versus explanation
- [x] Association versus causation
- [x] Denominator awareness
- [x] Benchmarking context
- [x] Statistical versus operational significance
- [x] Known analytical limitations

### Decision

**DOMAIN KNOWLEDGE GATE: PASS**

The project has sufficient documented NHS A&E domain context to proceed to
formal data and KPI specification.

Passing this gate does not imply that all future analytical questions are
already defined.

New measures, source families, or methodological changes must be checked
against current authoritative guidance and incorporated into this guide when
they materially affect interpretation.

