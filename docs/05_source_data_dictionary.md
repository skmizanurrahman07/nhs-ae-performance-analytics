# NHS A&E Source Data Dictionary

## 1. Purpose

This data dictionary defines the fields in the NHS A&E Monthly Attendances and
Emergency Admissions provider-level source used by this project.

The dictionary provides the controlled bridge between:

`Raw NHS source → ETL transformation → analytical model → SQL → Power BI`

For each source field, the dictionary will document:

- raw source name;
- proposed standardised name;
- analytical meaning;
- source role;
- expected data type;
- null treatment;
- transformation rule;
- validation rule;
- analytical use;
- known limitations.

The raw source field names will remain preserved for traceability. Standardised
names will be introduced only within the controlled transformation layer.

---

## 2. Source structure

The September 2026 development source contains:

- 4 identifier fields;
- 18 measure fields;
- 22 fields in total.

The provider-level analytical grain is:

`Reporting period + Org Code`

The published `TOTAL` record is treated as a reconciliation control rather
than as a provider.

---

## 3. Identifier fields
### 3.1 `Period`

**Raw source field:** `Period`

**Proposed standardised name:** `reporting_period_raw`

**Source role:** Reporting-period identifier

**Raw data type:** String

**Analytical meaning:**  
Identifies the reporting period represented by the source record.

For the September 2026 development source, provider records contain:

`MSitAE-SEPTEMBER-2026`

The published control record contains:

`TOTAL`

**Analytical treatment:**  
Provider records and the published `TOTAL` control record must be distinguished
before the reporting-period value is transformed.

For provider records, the raw reporting-period value will be preserved as
`reporting_period_raw`.

A separate standardised reporting-month field will be derived during ETL for
chronological analysis.

**Proposed derived field:** `reporting_month`

**Proposed derived type:** Date

For the development source:

`MSitAE-SEPTEMBER-2026 → 2026-09-01`

The first day of the month is used as a standard monthly analytical date key.
It does not represent the date on which the underlying A&E activity occurred.

**Null rule:**  
Provider records must not contain a null, blank, or whitespace-only reporting
period.

**Transformation rule:**  

1. Preserve the original value in `reporting_period_raw`.
2. Exclude the published `TOTAL` control record from provider-level
   transformation.
3. Parse the provider reporting-period value into `reporting_month`.
4. Reject or quarantine a provider-period value that cannot be parsed according
   to the controlled reporting-period rule.

**Validation rules:**

- raw provider reporting period is non-null;
- raw provider reporting period is not blank;
- raw provider reporting period contains no surrounding whitespace;
- the reporting period can be parsed successfully;
- `reporting_month` represents the intended source reporting month;
- provider business keys remain unique after date transformation;
- transformation does not alter activity measures.

**Analytical use:**

- chronological sorting;
- month-on-month calculations;
- year-on-year calculations;
- rolling-period calculations;
- joins to the future date dimension;
- SQL time-series analysis;
- Power BI time intelligence.

**Known limitation:**  
The reporting period is not the publication date, download date, or ingestion
timestamp. Those concepts must remain separate.
### 3.2 `Org Code`

**Raw source field:** `Org Code`

**Proposed standardised name:** `org_code`

**Source role:** Provider organisation identifier

**Raw data type:** String

**Analytical meaning:**  
Identifies the provider organisation associated with the published
provider-level A&E record.

Within the September 2026 development source:

- 191 provider records were identified;
- 191 distinct provider organisation codes were observed;
- no duplicate `Period + Org Code` provider business keys were identified.

**Analytical treatment:**  
`Org Code` will be retained as the principal provider identifier in the
provider-level analytical dataset.

`Org name` will be retained as a descriptive label rather than used as a
replacement for the organisation code.

**Null rule:**  
Provider records must not contain a null, blank, or whitespace-only
organisation code.

**Transformation rule:**

1. Preserve the original source value for lineage and audit purposes.
2. Create the standardised analytical field as `org_code`.
3. Treat the value as a string rather than a number.
4. Do not remove leading characters or convert numeric-looking codes to
   integers.
5. Do not impose a single fixed code length without authoritative evidence.

**Observed source profile:**

The September 2026 source contains organisation codes of multiple lengths:

- 153 codes with 3 characters;
- 31 codes with 5 characters;
- 7 codes with 6 characters.

All 191 profiled provider codes contained only uppercase letters and digits
after surrounding-whitespace inspection.

These observations describe the current source and are not treated as a
universal NHS organisation-code specification.

**Validation rules:**

- value is non-null;
- value is not blank;
- value is not whitespace-only;
- value contains no unexpected surrounding whitespace;
- - provider key `reporting_month + org_code` is unique at provider-period
  grain after transformation;
- each `org_code` maps consistently to one organisation name within the
  reporting period;
- each `org_code` maps consistently to one controlled parent organisation
  within the reporting period;
- new or changed organisation-code patterns are flagged for investigation
  rather than automatically rejected solely because their length differs.

**Multi-period validation:**  
When additional months are introduced, the project must investigate:

- organisation-code appearance and disappearance;
- organisation-name changes for an existing code;
- parent-organisation changes;
- provider restructuring;
- code replacement or succession;
- duplicate provider-period records.

A change must not automatically be classified as an error because NHS
organisational structures may change over time.

**Analytical use:**

- provider-level business key;
- provider dimension;
- joins;
- provider-level trend analysis;
- benchmarking;
- ranking and percentile analysis;
- SQL grouping;
- Power BI relationships.

**Known limitation:**  
An organisation code identifies the published organisation record but does not
by itself describe provider type, service configuration, case mix, capacity,
or organisational comparability.

Additional provider attributes are required before constructing more
specialised peer groups.

### 3.3 `Parent Org`

**Raw source field:** `Parent Org`

**Proposed standardised name:** `parent_org`

**Source role:** Higher-level organisational grouping

**Raw data type:** String

**Analytical meaning:**  
Provides the higher-level organisational grouping associated with each
provider record in the published source.

In the September 2026 development source:

- 7 distinct raw `Parent Org` categories were identified;
- provider records were distributed across those 7 categories;
- 167 provider records contained trailing whitespace;
- no leading-whitespace values were identified;
- trimming the surrounding whitespace preserved the same 7 distinct
  categories.

**Analytical treatment:**  
The raw value must remain unchanged in the immutable source file.

During controlled ETL, surrounding whitespace will be removed before the
field is used for grouping, joining, or reporting.

**Transformation rule:**

`parent_org = Parent Org.str.strip()`

Conceptually:

`Raw Parent Org → remove surrounding whitespace → standardised parent_org`

The transformation must operate only on the transformed dataset and must not
overwrite the raw source.

**Null rule:**  
Provider records must not contain a null, blank, or whitespace-only
`Parent Org` value unless a future source-specific rule explicitly permits it.

**Validation rules:**

- raw value is non-null;
- raw value is not blank;
- raw value is not whitespace-only;
- surrounding whitespace is detected and quantified before transformation;
- standardised `parent_org` contains no leading or trailing whitespace;
- trimming does not unexpectedly alter category meaning;
- provider row count remains unchanged after transformation;
- activity measures remain unchanged;
- organisation-code-to-parent mapping remains internally consistent.

**Post-transformation requirement:**  

For the September 2026 source:

`surrounding whitespace after transformation = 0`

The transformation must also preserve the expected 7 parent-organisation
categories unless an explicitly documented mapping rule explains a change.

**Multi-period treatment:**  
When additional months are introduced, parent-organisation mappings must be
revalidated.

Changes may represent:

- organisational restructuring;
- provider movement;
- reporting-boundary changes;
- naming changes;
- source-data quality issues.

A changed parent organisation must therefore be investigated rather than
automatically corrected to a historical value.

**Analytical use:**

- higher-level grouping;
- contextual provider analysis;
- aggregation;
- filtering;
- SQL grouping;
- Power BI slicing;
- investigation of variation across organisational groups.

**Known limitation:**  
`Parent Org` should not automatically be interpreted as a permanent provider
hierarchy across all reporting periods.

The organisational relationship may change over time and must therefore be
validated longitudinally.

### 3.4 `Org name`

**Raw source field:** `Org name`

**Proposed standardised name:** `org_name`

**Source role:** Provider organisation descriptive label

**Raw data type:** String

**Analytical meaning:**  
Provides the published organisation name associated with each provider
organisation code.

Within the September 2026 development source:

- 191 provider records were identified;
- 191 distinct organisation names were observed;
- no null, blank, or whitespace-only organisation names were identified;
- no surrounding-whitespace issues were identified;
- no organisation names mapped to multiple organisation codes within the
  reporting period;
- no organisation codes mapped to multiple organisation names within the
  reporting period.

**Analytical treatment:**  
`org_name` will be retained as the human-readable provider label.

The organisation name will not replace `org_code` as the provider identifier
because organisation names may change over time.

**Transformation rule:**

1. Preserve the original source value for lineage and audit purposes.
2. Create the standardised analytical field as `org_name`.
3. Treat the field as a string.
4. Do not automatically rename or consolidate organisations without a
   documented mapping rule.

**Null rule:**  
Provider records must not contain a null, blank, or whitespace-only
organisation name unless a future source-specific rule explicitly permits it.

**Validation rules:**

- value is non-null;
- value is not blank;
- value is not whitespace-only;
- value contains no unexpected surrounding whitespace;
- each `org_code` maps to one `org_name` within the reporting period;
- each `org_name` maps to one `org_code` within the reporting period;
- provider row count is unchanged by transformation.

**Multi-period validation:**  
When additional reporting months are introduced, the project must investigate:

- name changes for existing organisation codes;
- identical names associated with different organisation codes;
- organisation mergers or restructuring;
- spelling or formatting changes;
- newly appearing or disappearing providers.

A name change must not automatically be classified as a data-quality error.

**Analytical use:**

- human-readable provider labels;
- tables and reports;
- provider benchmarking displays;
- dashboard filtering;
- chart labels;
- executive reporting.

Provider joins and analytical relationships should use the controlled
organisation identifier rather than organisation name alone.

**Known limitation:**  
Organisation name is a descriptive attribute and may change while the
underlying organisation code remains stable.

Organisation names therefore require longitudinal validation before being
used to infer organisational continuity.

---

## 4. Measure fields

The source contains 18 numeric measure fields describing A&E attendance,
booked-appointment activity, four-hour breaches, decision-to-admit waits,
and emergency admissions.

All measure fields are treated as counts in the raw source.

Unless explicitly stated otherwise:

- measure values must be numeric;
- measure values must not be negative;
- missing values must not automatically be converted to zero;
- provider-level measures exclude the published `TOTAL` control record;
- published `TOTAL` values are retained for reconciliation;
- transformation must not alter valid activity counts;
- derived KPIs must use only methodologically compatible fields.
### 4.1 `A&E attendances Type 1`

**Raw source field:** `A&E attendances Type 1`

**Proposed standardised name:** `ae_attendances_type1`

**Source role:** A&E activity measure

**Raw data type:** Integer

**Unit:** Count of attendances

**Analytical meaning:**  
Represents published A&E attendance activity attributed to Type 1 A&E
departments for the reporting period.

**Department context:**  
Type 1 represents the major consultant-led, 24-hour emergency-department
category documented in the NHS A&E domain guide.

**Transformation rule:**

1. Preserve the source activity count.
2. Rename the analytical field to `ae_attendances_type1`.
3. Store the measure using an appropriate integer type.
4. Do not combine the measure with other attendance categories during the raw
   standardisation step.
5. Do not add the separate booked-appointment Type 1 field to this value.

**Null rule:**  
A missing value must not automatically be interpreted as zero.

Any missing value requires data-quality investigation before downstream use.

**Validation rules:**

- field exists in the controlled schema;
- value is numeric;
- value is integer-compatible;
- value is non-negative;
- transformation preserves the original valid count;
- provider-level sums reconcile with the applicable published `TOTAL` value;
- booked-appointment activity is not added again.

**Analytical use:**

- Type 1 demand analysis;
- provider activity analysis;
- department-type comparison;
- KPI-001 Total A&E attendances;
- KPI-003 A&E admission rate denominator;
- KPI-004 Four-hour performance denominator;
- trend analysis;
- provider benchmarking.

**Aggregation rule:**  
The measure is additive across compatible provider-period records.

Aggregation must not include both provider records and the published `TOTAL`
control record.

**Historical comparability:**  
Comparisons across reporting periods require compatible definitions, provider
coverage, and reporting methodology.

Known methodological changes documented in the NHS A&E Domain Guide must be
considered before long-term interpretation.

**Known limitation:**  
The measure represents attendance events rather than distinct patients.

The count alone does not describe patient characteristics, clinical severity,
diagnosis, or the reason for changes in activity.
### 4.2 `A&E attendances Type 2`

**Raw source field:** `A&E attendances Type 2`

**Proposed standardised name:** `ae_attendances_type2`

**Source role:** A&E activity measure

**Raw data type:** Integer

**Unit:** Count of attendances

**Analytical meaning:**  
Represents published A&E attendance activity attributed to Type 2 A&E
departments for the reporting period.

**Department context:**  
Type 2 represents the consultant-led single-specialty emergency-department
category documented in the NHS A&E Domain Guide.

**Transformation rule:**

1. Preserve the source activity count.
2. Rename the analytical field to `ae_attendances_type2`.
3. Store the measure using an appropriate integer type.
4. Keep Type 2 activity separately identifiable during transformation.
5. Do not add the separate booked-appointment Type 2 field to this value.

**Null rule:**  
A missing value must not automatically be interpreted as zero.

Any missing value requires data-quality investigation before downstream use.

**Validation rules:**

- field exists in the controlled schema;
- value is numeric;
- value is integer-compatible;
- value is non-negative;
- transformation preserves the original valid count;
- provider-level sums reconcile with the applicable published `TOTAL` value;
- booked-appointment activity is not added again.

**Analytical use:**

- Type 2 demand analysis;
- department-type comparison;
- provider activity analysis;
- KPI-001 Total A&E attendances;
- KPI-003 A&E admission rate denominator;
- KPI-004 Four-hour performance denominator;
- trend analysis;
- provider benchmarking.

**Aggregation rule:**  
The measure is additive across compatible provider-period records.

Aggregation must not include both provider records and the published `TOTAL`
control record.

**Historical comparability:**  
Comparisons across reporting periods require compatible definitions, provider
coverage, and reporting methodology.

Changes in department classification or source methodology must be investigated
before interpreting long-term changes.

**Known limitation:**  
The measure represents attendance events rather than distinct patients.

Type 2 services differ operationally from Type 1 services, so differences in
activity or performance between department types require appropriate context.
### 4.3 `A&E attendances Other A&E Department`

**Raw source field:** `A&E attendances Other A&E Department`

**Proposed standardised name:** `ae_attendances_other`

**Source role:** A&E activity measure

**Raw data type:** Integer

**Unit:** Count of attendances

**Analytical meaning:**  
Represents published A&E attendance activity recorded under `Other A&E
Department` for the reporting period.

**Department context:**  
The project preserves the terminology used by the published source.

`Other A&E Department` will not automatically be renamed to `Type 3` during
transformation.

The NHS A&E Domain Guide documents the relevant Type 3 / Urgent Treatment
Centre context separately.

**Transformation rule:**

1. Preserve the source activity count.
2. Rename the analytical field to `ae_attendances_other`.
3. Store the measure using an appropriate integer type.
4. Keep Other A&E activity separately identifiable during transformation.
5. Do not automatically relabel the category as Type 3.
6. Do not add the separate booked-appointment Other Department field to this
   measure.

**Null rule:**  
A missing value must not automatically be interpreted as zero.

Any missing value requires data-quality investigation before downstream use.

**Validation rules:**

- field exists in the controlled schema;
- value is numeric;
- value is integer-compatible;
- value is non-negative;
- transformation preserves the original valid count;
- provider-level sums reconcile with the applicable published `TOTAL` value;
- booked-appointment activity is not added again;
- the published source category is preserved unless an authoritative mapping
  rule supports a change.

**Analytical use:**

- Other A&E demand analysis;
- department-category comparison;
- provider activity analysis;
- KPI-001 Total A&E attendances;
- KPI-003 A&E admission-rate denominator;
- KPI-004 Four-hour performance denominator;
- trend analysis;
- provider benchmarking.

**Aggregation rule:**  
The measure is additive across compatible provider-period records.

Aggregation must not include both provider records and the published `TOTAL`
control record.

**Historical comparability:**  
Comparisons across reporting periods require compatible definitions, provider
coverage, reporting methodology, and department categorisation.

Changes in classification or attribution must be investigated before
interpreting long-term movement.

**Known limitation:**  
The raw label `Other A&E Department` does not, by itself, justify treating
every underlying service as analytically identical.

Comparisons with Type 1 or Type 2 activity therefore require appropriate
service-model context.
### 4.4 `A&E attendances Booked Appointments Type 1`

**Raw source field:** `A&E attendances Booked Appointments Type 1`

**Proposed standardised name:** `ae_booked_attendances_type1`

**Source role:** Booked A&E attendance activity measure

**Raw data type:** Integer

**Unit:** Count of booked attendances

**Analytical meaning:**  
Represents the published count of booked A&E attendances attributed to Type 1
departments for the reporting period.

**Relationship to total attendance:**  
This field is retained as a separate analytical component.

It must not automatically be added to `A&E attendances Type 1` because the
project's domain and KPI governance rules identify a risk of double counting
where booked attendances are already included in the published attendance
figures.

**Transformation rule:**

1. Preserve the source count.
2. Rename the analytical field to `ae_booked_attendances_type1`.
3. Store the measure using an appropriate integer type.
4. Keep the measure separately identifiable from total Type 1 attendance.
5. Do not automatically add it to `ae_attendances_type1`.

**Null rule:**  
A missing value must not automatically be interpreted as zero.

Any missing value requires data-quality investigation before downstream use.

**Validation rules:**

- field exists in the controlled schema;
- value is numeric;
- value is integer-compatible;
- value is non-negative;
- transformation preserves the original valid count;
- provider-level sums reconcile with the applicable published `TOTAL` value;
- the field is not double counted when constructing KPI-001.

**Analytical use:**

- booked-attendance activity analysis;
- investigation of booked versus broader A&E activity;
- trend analysis;
- provider comparison;
- methodological interpretation of A&E attendance reporting.

**Aggregation rule:**  
The measure is additive across compatible provider-period records.

The published `TOTAL` control record must not be included alongside provider
records in an analytical aggregation.

**Historical comparability:**  
Historical analysis must account for changes in booked-appointment reporting
documented in the NHS A&E Domain Guide.

Booked-appointment activity must not be assumed to have had identical
reporting treatment across all historical periods.

**Known limitation:**  
This component does not represent additional activity on top of the published
Type 1 attendance total unless the applicable source definition explicitly
establishes that treatment.

Its primary value is as a separately reported component of booked attendance
activity.
### 4.5 `A&E attendances Booked Appointments Type 2`

**Raw source field:** `A&E attendances Booked Appointments Type 2`

**Proposed standardised name:** `ae_booked_attendances_type2`

**Source role:** Booked A&E attendance activity measure

**Raw data type:** Integer

**Unit:** Count of booked attendances

**Analytical meaning:**  
Represents the published count of booked A&E attendances attributed to Type 2
departments for the reporting period.

**Relationship to total attendance:**  
This field is retained as a separate analytical component.

It must not automatically be added to `A&E attendances Type 2` because doing
so could double count booked activity already represented within the published
attendance measure.

**Transformation rule:**

1. Preserve the source count.
2. Rename the analytical field to `ae_booked_attendances_type2`.
3. Store the measure using an appropriate integer type.
4. Keep booked Type 2 activity separately identifiable.
5. Do not automatically add it to `ae_attendances_type2`.

**Null rule:**  
A missing value must not automatically be interpreted as zero.

Any missing value requires data-quality investigation before downstream use.

**Validation rules:**

- field exists in the controlled schema;
- value is numeric;
- value is integer-compatible;
- value is non-negative;
- transformation preserves the original valid count;
- provider-level sums reconcile with the applicable published `TOTAL` value;
- the field is not double counted when constructing KPI-001.

**Analytical use:**

- booked Type 2 attendance analysis;
- investigation of booked versus broader Type 2 activity;
- trend analysis;
- provider comparison;
- methodological interpretation of attendance patterns.

**Aggregation rule:**  
The measure is additive across compatible provider-period records.

The published `TOTAL` control record must not be included alongside provider
records in an analytical aggregation.

**Historical comparability:**  
Historical analysis must account for changes in booked-appointment reporting
documented in the NHS A&E Domain Guide.

Booked-appointment activity must not be assumed to have identical reporting
treatment across all historical periods.

**Known limitation:**  
This component does not represent additional activity on top of the published
Type 2 attendance measure unless the applicable source definition explicitly
establishes that treatment.

It should therefore remain separately identifiable rather than automatically
summed into total attendance.
### 4.6 `A&E attendances Booked Appointments Other Department`

**Raw source field:** `A&E attendances Booked Appointments Other Department`

**Proposed standardised name:** `ae_booked_attendances_other`

**Source role:** Booked A&E attendance activity measure

**Raw data type:** Integer

**Unit:** Count of booked attendances

**Analytical meaning:**  
Represents the published count of booked A&E attendances attributed to the
`Other Department` category for the reporting period.

**Department treatment:**  
The project preserves the published `Other Department` terminology.

The field will not automatically be relabelled as a Type 3 measure unless an
authoritative mapping rule establishes that treatment.

**Relationship to total attendance:**  
This field is retained as a separate analytical component.

It must not automatically be added to `A&E attendances Other A&E Department`
because doing so could double count booked activity already represented in
the published attendance measure.

**Transformation rule:**

1. Preserve the source count.
2. Rename the analytical field to `ae_booked_attendances_other`.
3. Store the measure using an appropriate integer type.
4. Keep booked Other Department activity separately identifiable.
5. Do not automatically add it to `ae_attendances_other`.
6. Do not automatically relabel the department category as Type 3.

**Null rule:**  
A missing value must not automatically be interpreted as zero.

Any missing value requires data-quality investigation before downstream use.

**Validation rules:**

- field exists in the controlled schema;
- value is numeric;
- value is integer-compatible;
- value is non-negative;
- transformation preserves the original valid count;
- provider-level sums reconcile with the applicable published `TOTAL` value;
- the field is not double counted when constructing KPI-001;
- the published department category remains traceable.

**Analytical use:**

- booked Other Department activity analysis;
- booked-attendance composition analysis;
- trend analysis;
- provider comparison;
- methodological interpretation of A&E attendance reporting.

**Aggregation rule:**  
The measure is additive across compatible provider-period records.

The published `TOTAL` control record must not be included alongside provider
records in analytical aggregation.

**Historical comparability:**  
Historical analysis must account for changes in booked-appointment reporting
and department categorisation documented in the NHS A&E Domain Guide.

**Known limitation:**  
This field is a separately published booked-attendance component.

It must not be interpreted as additional activity on top of the broader
published Other A&E attendance measure unless the applicable source definition
explicitly supports that interpretation.
### 4.7 `Attendances over 4hrs Type 1`

**Raw source field:** `Attendances over 4hrs Type 1`

**Proposed standardised name:** `ae_over_4hrs_type1`

**Source role:** A&E performance measure

**Raw data type:** Integer

**Unit:** Count of attendances exceeding four hours

**Analytical meaning:**  
Represents the published count of Type 1 A&E attendances exceeding the
four-hour measure for the reporting period.

**Relationship to attendance:**  
This measure corresponds to the Type 1 attendance population represented by:

`A&E attendances Type 1`

The breach count must therefore be interpreted alongside the compatible
attendance count.

**Transformation rule:**

1. Preserve the source breach count.
2. Rename the analytical field to `ae_over_4hrs_type1`.
3. Store the measure using an appropriate integer type.
4. Keep the Type 1 breach measure separately identifiable.
5. Do not add the separate booked-appointment Type 1 breach field again.

**Null rule:**  
A missing value must not automatically be interpreted as zero.

Any missing value requires data-quality investigation before downstream use.

**Validation rules:**

- field exists in the controlled schema;
- value is numeric;
- value is integer-compatible;
- value is non-negative;
- transformation preserves the original valid count;
- provider-level sums reconcile with the applicable published `TOTAL`;
- the breach count does not exceed the compatible Type 1 attendance count;
- booked-appointment breach activity is not double counted.

**Cross-field validity rule:**

`ae_over_4hrs_type1 <= ae_attendances_type1`

A violation must be flagged for investigation rather than automatically
corrected.

**Analytical use:**

- Type 1 breach-volume analysis;
- KPI-004 Four-hour A&E performance;
- KPI-005 Four-hour A&E breaches;
- trend analysis;
- provider benchmarking;
- investigation of performance variation.

**Aggregation rule:**  
The measure is additive across compatible provider-period records.

For percentage calculations, breach counts and compatible attendance counts
must first be aggregated to the required analytical grain before the
percentage is calculated.

**Historical comparability:**  
Trend analysis requires comparable provider coverage and four-hour reporting
methodology across periods.

Known methodology or cohort changes must be considered before interpreting
long-term movement.

**Known limitation:**  
The count identifies the volume of Type 1 attendances exceeding four hours but
does not explain why those breaches occurred.

Interpretation requires attendance volume and relevant operational context.
### 4.8 `Attendances over 4hrs Type 2`

**Raw source field:** `Attendances over 4hrs Type 2`

**Proposed standardised name:** `ae_over_4hrs_type2`

**Source role:** A&E performance measure

**Raw data type:** Integer

**Unit:** Count of attendances exceeding four hours

**Analytical meaning:**  
Represents the published count of Type 2 A&E attendances exceeding the
four-hour measure for the reporting period.

**Relationship to attendance:**  
This measure corresponds to the Type 2 attendance population represented by:

`A&E attendances Type 2`

The breach count must therefore be interpreted alongside the compatible Type 2
attendance count.

**Transformation rule:**

1. Preserve the source breach count.
2. Rename the analytical field to `ae_over_4hrs_type2`.
3. Store the measure using an appropriate integer type.
4. Keep the Type 2 breach measure separately identifiable.
5. Do not add the separate booked-appointment Type 2 breach field again.

**Null rule:**  
A missing value must not automatically be interpreted as zero.

Any missing value requires data-quality investigation before downstream use.

**Validation rules:**

- field exists in the controlled schema;
- value is numeric;
- value is integer-compatible;
- value is non-negative;
- transformation preserves the original valid count;
- provider-level sums reconcile with the applicable published `TOTAL`;
- the breach count does not exceed the compatible Type 2 attendance count;
- booked-appointment breach activity is not double counted.

**Cross-field validity rule:**

`ae_over_4hrs_type2 <= ae_attendances_type2`

A violation must be flagged for investigation rather than automatically
corrected.

**Analytical use:**

- Type 2 breach-volume analysis;
- KPI-004 Four-hour A&E performance;
- KPI-005 Four-hour A&E breaches;
- department-type comparison;
- trend analysis;
- provider benchmarking.

**Aggregation rule:**  
The measure is additive across compatible provider-period records.

For percentage calculations, breach counts and compatible attendance counts
must first be aggregated to the required analytical grain before calculating
the percentage.

**Historical comparability:**  
Trend analysis requires comparable Type 2 provider coverage and four-hour
reporting methodology across periods.

Known reporting changes must be assessed before interpreting long-term
movement.

**Known limitation:**  
The count identifies the volume of Type 2 attendances exceeding four hours but
does not explain why those breaches occurred.

Type 2 services differ from Type 1 services, so comparisons between department
types require appropriate service-model context.
### 4.9 `Attendances over 4hrs Other Department`

**Raw source field:** `Attendances over 4hrs Other Department`

**Proposed standardised name:** `ae_over_4hrs_other`

**Source role:** A&E performance measure

**Raw data type:** Integer

**Unit:** Count of attendances exceeding four hours

**Analytical meaning:**  
Represents the published count of attendances in the `Other Department`
category exceeding the four-hour measure for the reporting period.

**Department treatment:**  
The project preserves the published `Other Department` terminology.

The measure will not automatically be relabelled as a Type 3 measure unless a
controlled, authoritative mapping rule supports that treatment.

**Relationship to attendance:**  
This measure corresponds to the attendance population represented by:

`A&E attendances Other A&E Department`

The breach count must therefore be interpreted alongside the compatible
attendance count.

**Transformation rule:**

1. Preserve the source breach count.
2. Rename the analytical field to `ae_over_4hrs_other`.
3. Store the measure using an appropriate integer type.
4. Keep the Other Department breach measure separately identifiable.
5. Do not add the separate booked-appointment Other Department breach field
   again.
6. Preserve the published department category.

**Null rule:**  
A missing value must not automatically be interpreted as zero.

Any missing value requires data-quality investigation before downstream use.

**Validation rules:**

- field exists in the controlled schema;
- value is numeric;
- value is integer-compatible;
- value is non-negative;
- transformation preserves the original valid count;
- provider-level sums reconcile with the applicable published `TOTAL`;
- the breach count does not exceed the compatible Other A&E attendance count;
- booked-appointment breach activity is not double counted.

**Cross-field validity rule:**

`ae_over_4hrs_other <= ae_attendances_other`

A violation must be flagged for investigation rather than automatically
corrected.

**Analytical use:**

- Other Department breach-volume analysis;
- KPI-004 Four-hour A&E performance;
- KPI-005 Four-hour A&E breaches;
- department-category comparison;
- trend analysis;
- provider benchmarking.

**Aggregation rule:**  
The measure is additive across compatible provider-period records.

For percentage calculations, compatible breach and attendance counts must
first be aggregated to the required analytical grain before calculating the
percentage.

**Historical comparability:**  
Trend analysis requires compatible department categorisation, provider
coverage, and four-hour reporting methodology across periods.

**Known limitation:**  
The measure identifies the number of published Other Department attendances
exceeding four hours but does not explain why the breaches occurred.

The published category may contain services with different operational models,
so interpretation requires appropriate context.
### 4.10 `Attendances over 4hrs Booked Appointments Type 1`

**Raw source field:** `Attendances over 4hrs Booked Appointments Type 1`

**Proposed standardised name:** `ae_booked_over_4hrs_type1`

**Source role:** Booked A&E performance measure

**Raw data type:** Integer

**Unit:** Count of booked attendances exceeding four hours

**Analytical meaning:**  
Represents the published count of booked Type 1 A&E attendances exceeding the
four-hour measure for the reporting period.

**Relationship to booked attendance:**  
This measure corresponds to the separately published booked Type 1 attendance
component:

`A&E attendances Booked Appointments Type 1`

The booked breach measure must remain separately identifiable from the broader
Type 1 breach measure.

**Transformation rule:**

1. Preserve the source count.
2. Rename the analytical field to `ae_booked_over_4hrs_type1`.
3. Store the measure using an appropriate integer type.
4. Keep the booked Type 1 breach measure separately identifiable.
5. Do not automatically add it to `ae_over_4hrs_type1`.

**Null rule:**  
A missing value must not automatically be interpreted as zero.

Any missing value requires data-quality investigation before downstream use.

**Validation rules:**

- field exists in the controlled schema;
- value is numeric;
- value is integer-compatible;
- value is non-negative;
- transformation preserves the original valid count;
- provider-level sums reconcile with the applicable published `TOTAL`;
- the measure is not double counted within KPI-004 or KPI-005.

**Cross-field investigation rule:**  
The relationship between booked Type 1 breaches and booked Type 1 attendances
will be profiled and validated before a booked-appointment-specific performance
rate is introduced.

No new booked-appointment rate is approved merely because both component
fields are available.

**Analytical use:**

- booked Type 1 breach analysis;
- booked-appointment performance investigation;
- trend analysis;
- comparison with broader Type 1 activity where methodologically appropriate;
- data-quality and methodological analysis.

**Aggregation rule:**  
The measure is additive across compatible provider-period records.

The published `TOTAL` control record must not be included alongside provider
records in analytical aggregation.

**Historical comparability:**  
Historical interpretation must account for changes in booked-appointment
reporting documented in the NHS A&E Domain Guide.

**Known limitation:**  
This is a separately published booked-appointment component.

It must not automatically be added to the broader Type 1 breach count because
doing so could double count activity already represented in the published
performance measure.
### 4.11 `Attendances over 4hrs Booked Appointments Type 2`

**Raw source field:** `Attendances over 4hrs Booked Appointments Type 2`

**Proposed standardised name:** `ae_booked_over_4hrs_type2`

**Source role:** Booked A&E performance measure

**Raw data type:** Integer

**Unit:** Count of booked attendances exceeding four hours

**Analytical meaning:**  
Represents the published count of booked Type 2 A&E attendances exceeding the
four-hour measure for the reporting period.

**Relationship to booked attendance:**  
This measure corresponds to the separately published booked Type 2 attendance
component:

`A&E attendances Booked Appointments Type 2`

The booked breach measure must remain separately identifiable from the broader
Type 2 breach measure.

**Transformation rule:**

1. Preserve the source count.
2. Rename the analytical field to `ae_booked_over_4hrs_type2`.
3. Store the measure using an appropriate integer type.
4. Keep the booked Type 2 breach measure separately identifiable.
5. Do not automatically add it to `ae_over_4hrs_type2`.

**Null rule:**  
A missing value must not automatically be interpreted as zero.

Any missing value requires data-quality investigation before downstream use.

**Validation rules:**

- field exists in the controlled schema;
- value is numeric;
- value is integer-compatible;
- value is non-negative;
- transformation preserves the original valid count;
- provider-level sums reconcile with the applicable published `TOTAL`;
- the measure is not double counted within KPI-004 or KPI-005.

**Cross-field investigation rule:**  
The relationship between booked Type 2 breaches and booked Type 2 attendances
will be profiled and validated before a booked-appointment-specific performance
rate is introduced.

No booked-appointment-specific rate is approved solely because both component
fields are available.

**Analytical use:**

- booked Type 2 breach analysis;
- booked-appointment performance investigation;
- trend analysis;
- comparison with broader Type 2 activity where methodologically appropriate;
- data-quality and methodological analysis.

**Aggregation rule:**  
The measure is additive across compatible provider-period records.

The published `TOTAL` control record must not be included alongside provider
records in analytical aggregation.

**Historical comparability:**  
Historical interpretation must account for changes in booked-appointment
reporting documented in the NHS A&E Domain Guide.

**Known limitation:**  
This is a separately published booked-appointment component.

It must not automatically be added to the broader Type 2 breach count because
doing so could double count activity already represented in the published
performance measure.
### 4.12 `Attendances over 4hrs Booked Appointments Other Department`

**Raw source field:** `Attendances over 4hrs Booked Appointments Other Department`

**Proposed standardised name:** `ae_booked_over_4hrs_other`

**Source role:** Booked A&E performance measure

**Raw data type:** Integer

**Unit:** Count of booked attendances exceeding four hours

**Analytical meaning:**  
Represents the published count of booked attendances in the `Other Department`
category exceeding the four-hour measure for the reporting period.

**Department treatment:**  
The published `Other Department` terminology is preserved.

The field will not automatically be relabelled as Type 3 unless an
authoritative and documented mapping rule supports that treatment.

**Relationship to booked attendance:**  
This measure corresponds to the separately published booked-attendance
component:

`A&E attendances Booked Appointments Other Department`

The booked breach measure remains separately identifiable from the broader
Other Department breach measure.

**Transformation rule:**

1. Preserve the source count.
2. Rename the analytical field to `ae_booked_over_4hrs_other`.
3. Store the measure using an appropriate integer type.
4. Keep the booked Other Department breach measure separately identifiable.
5. Do not automatically add it to `ae_over_4hrs_other`.
6. Preserve the published department category.

**Null rule:**  
A missing value must not automatically be interpreted as zero.

Any missing value requires data-quality investigation before downstream use.

**Validation rules:**

- field exists in the controlled schema;
- value is numeric;
- value is integer-compatible;
- value is non-negative;
- transformation preserves the original valid count;
- provider-level sums reconcile with the applicable published `TOTAL`;
- the measure is not double counted within KPI-004 or KPI-005;
- the published department category remains traceable.

**Cross-field investigation rule:**  
The relationship between booked Other Department breaches and booked Other
Department attendances must be validated before any booked-appointment-specific
performance rate is introduced.

Availability of the two component fields alone does not constitute approval
for a new rate.

**Analytical use:**

- booked Other Department breach analysis;
- booked-appointment performance investigation;
- trend analysis;
- comparison with broader Other Department activity where methodologically
  appropriate;
- data-quality and methodological analysis.

**Aggregation rule:**  
The measure is additive across compatible provider-period records.

The published `TOTAL` control record must not be included alongside provider
records in analytical aggregation.

**Historical comparability:**  
Historical interpretation requires consideration of both booked-appointment
reporting changes and department-category changes documented in the NHS A&E
Domain Guide.

**Known limitation:**  
This is a separately published booked-appointment component.

It must not automatically be added to the broader Other Department breach
measure because this could double count activity already represented in the
published performance measure.
### 4.13 `Patients who have waited 4-12 hs from DTA to admission`

**Raw source field:** `Patients who have waited 4-12 hs from DTA to admission`

**Proposed standardised name:** `dta_wait_4_12hrs`

**Source role:** Decision-to-admit waiting-time measure

**Raw data type:** Integer

**Unit:** Count of patients

**Analytical meaning:**  
Represents the published count of patients waiting between 4 and 12 hours from
decision to admit (DTA) to admission for the reporting period.

**Pathway context:**  
This measure relates specifically to waiting time after a decision to admit.

It must remain distinct from the general A&E four-hour measure, which relates
to the broader A&E pathway.

**Transformation rule:**

1. Preserve the source count.
2. Rename the analytical field to `dta_wait_4_12hrs`.
3. Store the measure using an appropriate integer type.
4. Keep the 4-12 hour DTA category separately identifiable.
5. Do not combine it permanently with the 12+ hour DTA category.

**Null rule:**  
A missing value must not automatically be interpreted as zero.

Any missing value requires data-quality investigation before downstream use.

**Validation rules:**

- field exists in the controlled schema;
- value is numeric;
- value is integer-compatible;
- value is non-negative;
- transformation preserves the original valid count;
- provider-level sums reconcile with the applicable published `TOTAL`;
- the measure remains separate from the 12+ hour DTA category.

**Analytical use:**

- DTA delay analysis;
- KPI-006 Long waits after decision to admit;
- provider benchmarking;
- trend analysis;
- identification of providers or periods with elevated DTA waits;
- operational-flow investigation.

**Derived-measure relationship:**  
Where a combined 4+ hour DTA count is required:

`DTA 4+ hour waits = dta_wait_4_12hrs + dta_wait_12plus_hrs`

The two source components must remain separately available even when a combined
measure is calculated.

**Aggregation rule:**  
The measure is additive across compatible provider-period records.

The published `TOTAL` control record must not be included alongside provider
records in analytical aggregation.

**Historical comparability:**  
Long-term analysis requires confirmation that DTA definitions, provider
coverage, and reporting methodology remain comparable across periods.

**Known limitation:**  
The measure identifies the number of reported patients experiencing a 4-12
hour DTA-to-admission wait but does not explain why the delay occurred.

The measure must not be interpreted as equivalent to time spent in A&E from
arrival.
### 4.14 `Patients who have waited 12+ hrs from DTA to admission`

**Raw source field:** `Patients who have waited 12+ hrs from DTA to admission`

**Proposed standardised name:** `dta_wait_12plus_hrs`

**Source role:** Decision-to-admit waiting-time measure

**Raw data type:** Integer

**Unit:** Count of patients

**Analytical meaning:**  
Represents the published count of patients waiting 12 hours or more from
decision to admit (DTA) to admission for the reporting period.

**Pathway context:**  
The waiting-time clock for this measure relates to the period following the
decision to admit.

This measure must not be interpreted as equivalent to a 12-hour wait measured
from arrival at A&E.

**Transformation rule:**

1. Preserve the source count.
2. Rename the analytical field to `dta_wait_12plus_hrs`.
3. Store the measure using an appropriate integer type.
4. Keep the 12+ hour DTA category separately identifiable.
5. Do not permanently combine the measure with the 4-12 hour DTA category.

**Null rule:**  
A missing value must not automatically be interpreted as zero.

Any missing value requires data-quality investigation before downstream use.

**Validation rules:**

- field exists in the controlled schema;
- value is numeric;
- value is integer-compatible;
- value is non-negative;
- transformation preserves the original valid count;
- provider-level sums reconcile with the applicable published `TOTAL`;
- the 12+ hour category remains separately identifiable from the 4-12 hour
  category.

**Analytical use:**

- severe DTA long-wait analysis;
- KPI-006 Long waits after decision to admit;
- provider benchmarking;
- trend analysis;
- identification of providers or periods with elevated 12+ hour DTA waits;
- operational-flow investigation.

**Derived-measure relationship:**  
Where a combined 4+ hour DTA count is required:

`DTA 4+ hour waits = dta_wait_4_12hrs + dta_wait_12plus_hrs`

Both component measures must remain available after the combined measure is
calculated.

**Aggregation rule:**  
The measure is additive across compatible provider-period records.

The published `TOTAL` control record must not be included alongside provider
records in analytical aggregation.

**Historical comparability:**  
Long-term analysis requires confirmation that DTA definitions, provider
coverage, and reporting methodology remain comparable across periods.

**Known limitation:**  
The measure identifies the number of reported patients experiencing a 12+
hour wait from decision to admit to admission.

The aggregate measure does not explain why the delay occurred and must not be
treated as equivalent to an ECDS-derived 12-hour-from-arrival measure.
### 4.15 `Emergency admissions via A&E - Type 1`

**Raw source field:** `Emergency admissions via A&E - Type 1`

**Proposed standardised name:** `emergency_admissions_ae_type1`

**Source role:** Emergency-admission activity measure

**Raw data type:** Integer

**Unit:** Count of emergency admissions

**Analytical meaning:**  
Represents the published count of emergency admissions via Type 1 A&E for the
reporting period.

**Relationship to A&E attendance:**  
This measure is associated with emergency admissions via A&E and must remain
separate from `Other emergency admissions`.

It forms the Type 1 component of the project's controlled
`Emergency admissions via A&E` measure.

**Transformation rule:**

1. Preserve the source admission count.
2. Rename the analytical field to `emergency_admissions_ae_type1`.
3. Store the measure using an appropriate integer type.
4. Keep Type 1 admissions separately identifiable.
5. Do not combine the measure with `Other emergency admissions` when
   calculating an A&E admission rate.

**Null rule:**  
A missing value must not automatically be interpreted as zero.

Any missing value requires data-quality investigation before downstream use.

**Validation rules:**

- field exists in the controlled schema;
- value is numeric;
- value is integer-compatible;
- value is non-negative;
- transformation preserves the original valid count;
- provider-level sums reconcile with the applicable published `TOTAL`;
- the measure remains separately identifiable from non-A&E emergency
  admissions.

**Derived-measure relationship:**  
The measure contributes to:

`Emergency admissions via A&E = Type 1 + Type 2 + Other A&E department admissions`

It also contributes to:

- KPI-002 Total emergency admissions;
- KPI-003 A&E admission rate.

**Analytical use:**

- Type 1 emergency-admission analysis;
- A&E admission-pattern analysis;
- trend analysis;
- provider benchmarking;
- KPI-002 Total emergency admissions;
- KPI-003 A&E admission rate.

**Aggregation rule:**  
The measure is additive across compatible provider-period records.

For an admission-rate calculation, compatible admission and attendance counts
must first be aggregated to the required analytical grain before division.

**Historical comparability:**  
Trend analysis requires comparable admission definitions, provider coverage,
department categorisation, and reporting methodology across periods.

**Known limitation:**  
This aggregate count does not describe patient-level clinical characteristics,
severity, diagnosis, length of stay, or why admission activity changed.

The measure should therefore support descriptive and comparative analysis
rather than unsupported causal conclusions.
### 4.16 `Emergency admissions via A&E - Type 2`

**Raw source field:** `Emergency admissions via A&E - Type 2`

**Proposed standardised name:** `emergency_admissions_ae_type2`

**Source role:** Emergency-admission activity measure

**Raw data type:** Integer

**Unit:** Count of emergency admissions

**Analytical meaning:**  
Represents the published count of emergency admissions via Type 2 A&E for the
reporting period.

**Relationship to A&E attendance:**  
This measure is associated with emergency admissions via A&E and remains
separate from `Other emergency admissions`.

It forms the Type 2 component of the controlled
`Emergency admissions via A&E` measure.

**Transformation rule:**

1. Preserve the source admission count.
2. Rename the analytical field to `emergency_admissions_ae_type2`.
3. Store the measure using an appropriate integer type.
4. Keep Type 2 emergency admissions separately identifiable.
5. Do not combine this field with `Other emergency admissions` when
   calculating the A&E admission rate.

**Null rule:**  
A missing value must not automatically be interpreted as zero.

Any missing value requires data-quality investigation before downstream use.

**Validation rules:**

- field exists in the controlled schema;
- value is numeric;
- value is integer-compatible;
- value is non-negative;
- transformation preserves the original valid count;
- provider-level sums reconcile with the applicable published `TOTAL`;
- the measure remains separately identifiable from non-A&E emergency
  admissions.

**Derived-measure relationship:**  
This field contributes to:

`Emergency admissions via A&E = Type 1 + Type 2 + Other A&E department admissions`

It also contributes to:

- KPI-002 Total emergency admissions;
- KPI-003 A&E admission rate.

**Analytical use:**

- Type 2 emergency-admission analysis;
- A&E admission-pattern analysis;
- department-type comparison;
- trend analysis;
- provider benchmarking;
- KPI-002 Total emergency admissions;
- KPI-003 A&E admission rate.

**Aggregation rule:**  
The measure is additive across compatible provider-period records.

For an admission-rate calculation, compatible admission and attendance counts
must first be aggregated to the required analytical grain before division.

**Historical comparability:**  
Trend analysis requires compatible admission definitions, Type 2 provider
coverage, department categorisation, and reporting methodology across periods.

**Known limitation:**  
The aggregate count does not describe patient-level clinical characteristics,
severity, diagnosis, length of stay, or the reason for changes in emergency
admission activity.

Type 2 services may also differ operationally from Type 1 services, so
department-type comparisons require appropriate context.
### 4.17 `Emergency admissions via A&E - Other A&E department`

**Raw source field:** `Emergency admissions via A&E - Other A&E department`

**Proposed standardised name:** `emergency_admissions_ae_other`

**Source role:** Emergency-admission activity measure

**Raw data type:** Integer

**Unit:** Count of emergency admissions

**Analytical meaning:**  
Represents the published count of emergency admissions via the `Other A&E
department` category for the reporting period.

**Department treatment:**  
The project preserves the published `Other A&E department` terminology.

The field will not automatically be relabelled as Type 3 unless a controlled,
authoritative mapping rule supports that treatment.

**Relationship to A&E attendance:**  
This measure forms the Other A&E department component of the controlled
`Emergency admissions via A&E` measure.

It remains separate from `Other emergency admissions`, which represents a
different admission route.

**Transformation rule:**

1. Preserve the source admission count.
2. Rename the analytical field to `emergency_admissions_ae_other`.
3. Store the measure using an appropriate integer type.
4. Keep Other A&E department admissions separately identifiable.
5. Preserve the published department category.
6. Do not combine this field with `Other emergency admissions` when
   calculating KPI-003 A&E admission rate.

**Null rule:**  
A missing value must not automatically be interpreted as zero.

Any missing value requires data-quality investigation before downstream use.

**Validation rules:**

- field exists in the controlled schema;
- value is numeric;
- value is integer-compatible;
- value is non-negative;
- transformation preserves the original valid count;
- provider-level sums reconcile with the applicable published `TOTAL`;
- the measure remains separately identifiable from `Other emergency
  admissions`;
- the published department category remains traceable.

**Derived-measure relationship:**  
This field contributes to:

`Emergency admissions via A&E = Type 1 + Type 2 + Other A&E department admissions`

It also contributes to:

- KPI-002 Total emergency admissions;
- KPI-003 A&E admission rate.

**Analytical use:**

- Other A&E department emergency-admission analysis;
- A&E admission-pattern analysis;
- department-category comparison;
- trend analysis;
- provider benchmarking;
- KPI-002 Total emergency admissions;
- KPI-003 A&E admission rate.

**Aggregation rule:**  
The measure is additive across compatible provider-period records.

For admission-rate calculations, compatible admissions and attendance counts
must first be aggregated to the required analytical grain before division.

**Historical comparability:**  
Trend analysis requires compatible admission definitions, provider coverage,
department categorisation, and reporting methodology across periods.

**Known limitation:**  
The aggregate count does not explain the clinical or operational reasons for
admission.

The `Other A&E department` category may represent services with differing
operational characteristics, so comparisons require appropriate context.
### 4.18 `Other emergency admissions`

**Raw source field:** `Other emergency admissions`

**Proposed standardised name:** `other_emergency_admissions`

**Source role:** Emergency-admission activity measure

**Raw data type:** Integer

**Unit:** Count of emergency admissions

**Analytical meaning:**  
Represents published emergency admissions recorded separately from emergency
admissions via A&E.

This field must therefore remain distinct from the three
`Emergency admissions via A&E` measures.

**Relationship to emergency admissions via A&E:**  
The project distinguishes:

`Emergency admissions via A&E`

from:

`Other emergency admissions`

For KPI-002 Total emergency admissions, the two components may be combined
according to the approved KPI definition.

For KPI-003 A&E admission rate, `Other emergency admissions` is excluded
because the numerator must represent admissions via the A&E pathway.

**Transformation rule:**

1. Preserve the source admission count.
2. Rename the analytical field to `other_emergency_admissions`.
3. Store the measure using an appropriate integer type.
4. Keep the field separately identifiable from admissions via A&E.
5. Do not include the field in the numerator of KPI-003 A&E admission rate.

**Null rule:**  
A missing value must not automatically be interpreted as zero.

Any missing value requires data-quality investigation before downstream use.

**Validation rules:**

- field exists in the controlled schema;
- value is numeric;
- value is integer-compatible;
- value is non-negative;
- transformation preserves the original valid count;
- provider-level sums reconcile with the applicable published `TOTAL`;
- the measure remains separately identifiable from emergency admissions via
  A&E.

**Derived-measure relationship:**  
This field contributes to KPI-002:

`Total emergency admissions = Emergency admissions via A&E + Other emergency admissions`

It does not contribute to the numerator of KPI-003 A&E admission rate.

**Analytical use:**

- total emergency-admission analysis;
- comparison of admissions via A&E with other emergency-admission routes;
- trend analysis;
- provider-level activity analysis;
- KPI-002 Total emergency admissions.

**Aggregation rule:**  
The measure is additive across compatible provider-period records.

The published `TOTAL` control record must not be included alongside provider
records in analytical aggregation.

**Historical comparability:**  
Trend analysis requires compatible emergency-admission definitions, provider
coverage, and reporting methodology across periods.

**Known limitation:**  
This aggregate field does not identify the detailed route, clinical reason,
patient characteristics, severity, or outcomes associated with the
admission.

The measure must therefore not be interpreted as A&E-originated admission
activity.
---

## 5. Source Data Dictionary Quality Gate

The source data dictionary has been reviewed against the controlled
September 2026 NHS A&E source structure, source-profiling results, NHS A&E
Domain Guide, and approved KPI definitions.

### Field coverage

- [x] 4 identifier fields documented
- [x] 18 measure fields documented
- [x] 22 source fields documented in total

### Identifier coverage

- [x] `Period`
- [x] `Org Code`
- [x] `Parent Org`
- [x] `Org name`

### Attendance measures

- [x] Type 1 attendances
- [x] Type 2 attendances
- [x] Other A&E Department attendances
- [x] Booked Type 1 attendances
- [x] Booked Type 2 attendances
- [x] Booked Other Department attendances

### Four-hour measures

- [x] Type 1 breaches
- [x] Type 2 breaches
- [x] Other Department breaches
- [x] Booked Type 1 breaches
- [x] Booked Type 2 breaches
- [x] Booked Other Department breaches

### Decision-to-admit measures

- [x] DTA 4-12 hour waits
- [x] DTA 12+ hour waits

### Emergency-admission measures

- [x] Emergency admissions via A&E - Type 1
- [x] Emergency admissions via A&E - Type 2
- [x] Emergency admissions via A&E - Other A&E department
- [x] Other emergency admissions

### Transformation governance

For each source field, the dictionary defines where applicable:

- [x] raw source field name
- [x] proposed standardised analytical name
- [x] source role
- [x] expected data type
- [x] analytical meaning
- [x] transformation treatment
- [x] null treatment
- [x] validation rules
- [x] analytical use
- [x] aggregation treatment
- [x] historical-comparability considerations
- [x] known limitations

### Controlled transformation requirements

The dictionary preserves the following project rules:

1. The immutable raw source must not be overwritten.
2. Raw reporting-period information must remain traceable.
3. `Parent Org` surrounding whitespace must be removed only within the
   controlled transformation layer.
4. Booked-appointment measures must remain separately identifiable and must
   not be added again where doing so would double count published totals.
5. `Other A&E Department` terminology must not automatically be relabelled as
   Type 3 without an authoritative mapping rule.
6. DTA waiting measures must remain distinct from arrival-based waiting-time
   measures.
7. Emergency admissions via A&E must remain distinguishable from
   `Other emergency admissions`.
8. Missing measure values must not automatically be converted to zero.
9. Published `TOTAL` records must not be treated as provider records.
10. Published totals must remain available for reconciliation.

### Analytical grain

The controlled provider-period analytical grain is:

`reporting_month + org_code`

The raw-source equivalent is:

`Period + Org Code`

Business-key uniqueness must be revalidated after transformation and whenever
additional monthly sources are introduced.

### Quality decision

**SOURCE DATA DICTIONARY QUALITY GATE: PASS**

The 22-field dictionary is sufficiently specified to support controlled ETL
design.

Any future source-schema change, new field, changed definition, or new source
family must be assessed before being incorporated into the analytical model.
