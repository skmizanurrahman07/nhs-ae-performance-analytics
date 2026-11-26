# Analytical Questions and KPI Catalogue

## Priority analytical questions

### Priority 1: Core performance

1. How has total A&E demand changed over time?
2. How have emergency admissions changed over time?
3. What proportion of applicable attendances meet the four-hour measure?
4. Where are long waits after decision to admit concentrated?
5. Which providers demonstrate sustained improvement or deterioration?

### Priority 2: Benchmarking and variation

6. How does a selected provider compare with the national distribution?
7. Is provider performance stable or unusually variable?
8. Which providers combine high demand with comparatively strong performance?
9. Which months or service types contribute most to observed variation?

### Priority 3: Capacity extension

10. Is capacity pressure associated with A&E performance?
11. Do relationships remain after accounting for seasonality and provider size?
12. Which patterns warrant operational investigation rather than causal claims?

## KPI catalogue

| ID | KPI | Conceptual calculation | Direction | Caveat |
|---|---|---|---|---|
| KPI-001 | Total attendances | Sum of eligible attendances | Context | Define included A&E types |
| KPI-002 | Emergency admissions | Sum of eligible emergency admissions | Context | Confirm admission definition |
| KPI-003 | Admission rate | Admissions from A&E / attendances Ã— 100 | Context | Use matching populations |
| KPI-004 | Four-hour performance | Within-four-hour count / applicable attendances Ã— 100 | Higher | Confirm source denominator |
| KPI-005 | Four-hour breaches | Applicable attendances minus within-four-hour count | Lower | Do not derive if populations differ |
| KPI-006 | Long waits after decision to admit | Sum of published long-wait measure | Lower | Measure is not arrival-to-departure |
| KPI-007 | Long-wait rate | Long waits / appropriate admissions denominator Ã— 100 | Lower | Denominator requires confirmation |
| KPI-008 | Month-on-month change | Current month versus previous month | Context | Seasonal effects possible |
| KPI-009 | Year-on-year change | Current month versus comparable prior-year month | Context | Check comparability |
| KPI-010 | Rolling 12-month activity | Sum over trailing 12 complete months | Context | Requires complete periods |
| KPI-011 | Provider percentile | Provider position in comparable distribution | Context | Peer definition matters |
| KPI-012 | Data quality pass rate | Passed checks / executed checks Ã— 100 | Higher | Severity must also be shown |

## KPI governance status

The initial source profiling and NHS A&E domain audit have now been completed.

KPI approval will therefore progress from conceptual definitions to controlled
technical specifications.

A KPI will not be classified as implementation-ready until the following have
been defined where applicable:

- analytical purpose;
- numerator;
- denominator;
- formula;
- unit;
- direction of interpretation;
- included source fields;
- excluded source fields;
- zero-denominator treatment;
- aggregation rule;
- analytical grain;
- historical comparability requirements;
- validation rule;
- known limitations.

### Current status

- **KPI-001 Total attendances:** requires final source-field inclusion rule.
- **KPI-002 Emergency admissions:** requires final treatment of admissions via
  A&E versus other emergency admissions.
- **KPI-003 Admission rate:** provisional pending compatible numerator and
  denominator specification.
- **KPI-004 Four-hour performance:** provisional pending exact attendance and
  breach denominator specification.
- **KPI-005 Four-hour breaches:** published breach fields are available, but the
  combined KPI requires an explicit inclusion rule.
- **KPI-006 Long waits after decision to admit:** source measures are available;
  the 4-12 hour and 12+ hour categories must remain separately identifiable.
- **KPI-007 Long-wait rate:** provisional pending denominator approval.
- **KPI-008 Month-on-month change:** concept approved; implementation requires
  a multi-month comparable dataset.
- **KPI-009 Year-on-year change:** concept approved; implementation requires
  comparable historical periods.
- **KPI-010 Rolling 12-month activity:** concept approved; implementation
  requires 12 complete comparable reporting months.
- **KPI-011 Provider percentile:** concept approved; implementation requires a
  documented comparable-provider population.
- **KPI-012 Data quality pass rate:** concept approved; severity and critical
  failures must remain visible alongside any overall percentage.

No provisional KPI will be promoted to production Python, SQL, or DAX merely
because its calculation is technically possible.

## Insight-writing standard

Every conclusion must separate:

1. **Observation:** What the validated data shows.
2. **Interpretation:** A cautious explanation of the pattern.
3. **Operational question:** What should be investigated next.
4. **Limitation:** What cannot be concluded from the available data.

---

# Controlled KPI specifications

## KPI-001: Total A&E attendances

### Business question

What is the total volume of published A&E attendance activity for the
selected provider population and reporting period?

### Analytical purpose

This KPI measures A&E demand volume and provides the base activity measure
for trend analysis, provider comparison, and selected performance-rate
calculations.

### Source fields included

- `A&E attendances Type 1`
- `A&E attendances Type 2`
- `A&E attendances Other A&E Department`

### Source fields excluded from additional summation

- `A&E attendances Booked Appointments Type 1`
- `A&E attendances Booked Appointments Type 2`
- `A&E attendances Booked Appointments Other Department`

Booked-appointment fields are not added separately because published A&E
attendance figures include booked appointments under the applicable
post-August-2020 reporting approach.

Adding the booked-appointment fields again would risk double counting.

### Formula

`Total A&E attendances = Type 1 attendances + Type 2 attendances + Other A&E attendances`

Or mathematically:

`A_total = A_type1 + A_type2 + A_other`

### Unit

Count of attendances.

### Direction

Contextual.

Higher attendance volume does not represent inherently better or worse
performance. It represents greater recorded activity.

### Analytical grain

The base calculation is performed at:

`Reporting period + Org Code`

Higher-level totals may subsequently be calculated by aggregating compatible
provider-period records.

### Null treatment

A missing component will not automatically be interpreted as zero.

Missingness must first be treated as a data-quality condition because zero
activity and unavailable activity are different concepts.

### Negative-value rule

Attendance counts must not be negative.

### TOTAL-row treatment

The published `TOTAL` record is excluded from provider-level calculation.

The published `TOTAL` is retained as a reconciliation control against the
sum of provider records.

### Validation rules

KPI-001 is valid only when:

1. required attendance fields are present;
2. component fields are numeric;
3. component values are non-negative;
4. provider business keys are unique at the required grain;
5. the published `TOTAL` control reconciles with provider-level sums;
6. no booked-appointment field has been added separately to the attendance
   components.

### Historical comparability

Trend analysis must account for known methodological changes.

In particular, booked appointments became included in published attendance
figures from August 2020.

Historical comparisons spanning that change require an explicit comparability
caveat.

### Limitations

This KPI measures attendance events rather than distinct patients.

The KPI does not identify:

- why demand changed;
- patient demographics;
- clinical severity;
- diagnosis;
- whether the same person attended multiple times.

### Governance status

**KPI-001: DEFINITION APPROVED**

Implementation in production Python, SQL, and DAX remains subject to
cross-platform reconciliation testing.
---

## KPI-002: Total emergency admissions

### Business question

What is the total volume of emergency admissions recorded for the selected
provider population and reporting period?

### Analytical purpose

This KPI measures total emergency-admission activity across the emergency
admission routes represented in the Monthly A&E source.

The KPI provides a high-level measure of emergency admission demand.

### Source fields included

Emergency admissions via A&E:

- `Emergency admissions via A&E - Type 1`
- `Emergency admissions via A&E - Type 2`
- `Emergency admissions via A&E - Other A&E department`

Other emergency admissions:

- `Other emergency admissions`

### Component measure: Emergency admissions via A&E

Emergency admissions via A&E will remain separately available as a controlled
component measure.

Formula:

`Emergency admissions via A&E = Type 1 + Type 2 + Other A&E department admissions`

Mathematically:

`E_AE = E_type1 + E_type2 + E_other_ae`

### Total emergency-admissions formula

`Total emergency admissions = Emergency admissions via A&E + Other emergency admissions`

Mathematically:

`E_total = E_AE + E_other`

### Unit

Count of emergency admissions.

### Direction

Contextual.

A higher value represents greater recorded emergency-admission activity and is
not inherently a positive or negative performance result.

### Analytical grain

The base calculation is performed at:

`Reporting period + Org Code`

Higher-level totals may subsequently be calculated by aggregating compatible
provider-period records.

### Null treatment

Missing admission components will not automatically be interpreted as zero.

Missingness must first be treated as a data-quality condition.

### Negative-value rule

Emergency-admission counts must not be negative.

### TOTAL-row treatment

The published `TOTAL` record is excluded from provider-level calculation.

The published `TOTAL` remains available as a reconciliation control.

### Validation rules

KPI-002 is valid only when:

1. required admission fields are present;
2. component fields are numeric;
3. component values are non-negative;
4. provider business keys are unique at the required grain;
5. provider-level component sums reconcile with the applicable published
   control totals;
6. emergency admissions via A&E remain separately derivable from other
   emergency admissions.

### Analytical relationship to attendance

Total emergency admissions must not be divided by A&E attendances to produce
an A&E admission rate because total emergency admissions include the separate
`Other emergency admissions` component.

Any A&E admission-rate KPI must instead use a numerator and denominator
representing compatible populations.

### Historical comparability

Trend analysis requires consistent admission definitions, provider coverage,
and reporting methodology across periods.

Known changes in reporting definitions or provider structures must be
documented before interpreting long-term movement.

### Limitations

This KPI does not by itself identify:

- the clinical reason for admission;
- patient demographics;
- severity;
- length of stay;
- whether an admission originated through A&E or another route unless the
  component measures are analysed separately;
- why emergency-admission activity changed.

### Governance status

**KPI-002: DEFINITION APPROVED**

The following controlled component measure is also approved conceptually:

`Emergency admissions via A&E`

Implementation in production Python, SQL, and DAX remains subject to
cross-platform reconciliation testing.
---

## KPI-003: A&E admission rate

### Business question

What proportion of published A&E attendance activity results in an emergency
admission via A&E for the selected provider population and reporting period?

### Analytical purpose

This KPI describes the relationship between A&E attendance volume and
emergency admissions recorded via A&E.

It can support investigation of differences in admission patterns across
providers and reporting periods.

### Numerator

Emergency admissions via A&E:

- `Emergency admissions via A&E - Type 1`
- `Emergency admissions via A&E - Type 2`
- `Emergency admissions via A&E - Other A&E department`

Numerator formula:

`E_AE = E_type1 + E_type2 + E_other_ae`

### Denominator

Total published A&E attendances:

- `A&E attendances Type 1`
- `A&E attendances Type 2`
- `A&E attendances Other A&E Department`

Denominator formula:

`A_total = A_type1 + A_type2 + A_other`

### Excluded field

`Other emergency admissions`

is excluded from the numerator because it represents emergency admissions
outside the admissions-via-A&E component.

### Formula

`A&E admission rate (%) = Emergency admissions via A&E / Total A&E attendances Ã— 100`

Mathematically:

`Admission rate (%) = (E_AE / A_total) Ã— 100`

### Unit

Percentage.

### Direction

Contextual.

A higher admission rate is not automatically better or worse.

The measure may reflect differences in patient need, service configuration,
department type, provider characteristics, or other factors not available in
the aggregate dataset.

### Analytical grain

The base calculation is performed at:

`Reporting period + Org Code`

The rate should be recalculated from aggregated numerator and denominator
values when moving to a higher analytical grain.

Rates should not be aggregated by simply averaging provider percentages
unless that averaging method is explicitly required and justified.

### Zero-denominator treatment

If:

`Total A&E attendances = 0`

then the A&E admission rate is undefined.

The analytical implementation must return a missing or null rate rather than
divide by zero or automatically return zero percent.

### Null treatment

Missing numerator or denominator components are not automatically interpreted
as zero.

Missingness must first be investigated as a data-quality condition.

### Validation rules

KPI-003 is valid only when:

1. all required attendance and admission fields are present;
2. numerator and denominator components are numeric;
3. component counts are non-negative;
4. the total attendance denominator is greater than zero;
5. `Other emergency admissions` are excluded from the numerator;
6. provider business keys are unique at the required grain;
7. numerator and denominator are aggregated to the same analytical grain
   before division.

### Aggregation rule

For groups of providers or periods:

`Grouped admission rate = Sum of compatible admissions via A&E / Sum of compatible A&E attendances Ã— 100`

The project will not calculate a national or regional admission rate by
taking an unweighted mean of provider admission-rate percentages.

### Historical comparability

Trend analysis requires comparable attendance and admission definitions,
provider coverage, and reporting methodology.

Known methodological changes must be considered before comparing rates across
different historical periods.

### Limitations

The admission rate does not directly measure:

- patient severity;
- clinical appropriateness of admission;
- case mix;
- individual patient outcomes;
- reason for admission;
- capacity availability.

The aggregate source therefore supports descriptive and comparative analysis
but not unsupported causal interpretation.

### Governance status

**KPI-003: DEFINITION APPROVED**

Implementation in production Python, SQL, and DAX remains subject to
cross-platform reconciliation testing.
---

## KPI-004: Four-hour A&E performance

### Business question

What proportion of applicable published A&E attendances are completed within
four hours for the selected provider population and reporting period?

### Analytical purpose

This KPI measures the proportion of applicable A&E attendance activity that
does not exceed four hours from arrival to the relevant departure outcome.

It is a core performance measure for examining A&E operational performance,
trends, and provider variation.

### Attendance denominator

The denominator uses the applicable published A&E attendance fields:

- `A&E attendances Type 1`
- `A&E attendances Type 2`
- `A&E attendances Other A&E Department`

Formula:

`A_total = A_type1 + A_type2 + A_other`

### Four-hour breaches

The corresponding published breach fields are:

- `Attendances over 4hrs Type 1`
- `Attendances over 4hrs Type 2`
- `Attendances over 4hrs Other Department`

Formula:

`B_total = B_type1 + B_type2 + B_other`

### Booked-appointment fields

The separate booked-appointment attendance and breach fields are not added
again to the denominator or breach total where they are already represented
within the published attendance and performance totals.

Adding them again would risk double counting.

### Within-four-hour count

`Within four hours = Applicable attendances - Four-hour breaches`

Mathematically:

`W_4h = A_total - B_total`

### Formula

`Four-hour performance (%) = Within-four-hour attendances / Applicable attendances Ã— 100`

Therefore:

`Four-hour performance (%) = ((A_total - B_total) / A_total) Ã— 100`

An equivalent expression is:

`Four-hour performance (%) = 100 - ((B_total / A_total) Ã— 100)`

### Unit

Percentage.

### Direction

Higher is better for this defined measure.

### Analytical grain

The base calculation is performed at:

`Reporting period + Org Code`

When moving to a higher analytical grain, the numerator and denominator must
first be aggregated and the percentage recalculated.

### Aggregation rule

For multiple providers or reporting periods:

`Grouped performance (%) = (Sum applicable attendances - Sum breaches) / Sum applicable attendances Ã— 100`

Provider percentages must not be averaged without an explicitly justified
reason because providers have different attendance volumes.

### Zero-denominator treatment

If:

`Applicable attendances = 0`

then four-hour performance is undefined.

The implementation must return a missing or null result rather than dividing
by zero or automatically returning zero percent.

### Null treatment

Missing attendance or breach components are not automatically treated as zero.

Missingness must first be assessed as a data-quality condition.

### Validity rules

For compatible provider-period records:

- attendance counts must be non-negative;
- breach counts must be non-negative;
- four-hour breaches must not exceed their compatible attendance population;
- calculated performance should fall between 0% and 100%.

A failure requires investigation rather than automatic correction.

### TOTAL-row treatment

The published `TOTAL` record is excluded from provider-level calculations.

The published control record remains available for reconciliation.

### Historical comparability

Four-hour performance comparisons require comparable provider coverage and
reporting methodology.

Periods affected by changes in provider cohort, reporting footprint, or
performance-measure methodology must be identified before trend comparison.

### Interpretation

Higher performance means a greater proportion of the applicable attendance
population was completed within four hours.

This KPI should not be interpreted as a complete measure of emergency-care
quality.

Performance should be considered alongside:

- attendance demand;
- emergency admissions;
- DTA long waits;
- provider characteristics;
- relevant operational context.

### Limitations

The aggregate measure does not explain why four-hour performance changed.

The KPI alone cannot establish whether variation was caused by:

- attendance demand;
- staffing;
- bed availability;
- admission pressure;
- case mix;
- internal patient flow;
- other operational factors.

### Governance status

**KPI-004: DEFINITION APPROVED**

Implementation in production Python, SQL, and DAX remains subject to
cross-platform reconciliation and validity testing.
---

## KPI-005: Four-hour A&E breaches

### Business question

How many applicable A&E attendances exceeded four hours for the selected
provider population and reporting period?

### Analytical purpose

This KPI measures the absolute volume of published A&E attendances exceeding
four hours.

It complements the percentage-based four-hour performance KPI by showing the
number of affected attendance events.

### Source fields included

- `Attendances over 4hrs Type 1`
- `Attendances over 4hrs Type 2`
- `Attendances over 4hrs Other Department`

### Formula

`Total four-hour breaches = Type 1 breaches + Type 2 breaches + Other A&E department breaches`

Mathematically:

`B_total = B_type1 + B_type2 + B_other`

### Booked-appointment fields

The separate booked-appointment breach fields are not added again where they
are already represented within the published breach measures.

This prevents double counting.

### Unit

Count of attendance events exceeding four hours.

### Direction

Lower is better for this defined measure.

However, absolute breach counts should be interpreted alongside attendance
volume.

A provider with greater activity may have more breaches even where its
percentage performance is comparatively stronger.

### Analytical grain

The base calculation is performed at:

`Reporting period + Org Code`

### Aggregation rule

Four-hour breach counts are additive across compatible provider-period
records.

For higher analytical grains:

`Grouped breaches = Sum of compatible provider-period breach counts`

### Null treatment

Missing breach components are not automatically interpreted as zero.

Missingness must first be treated as a data-quality condition.

### Negative-value rule

Four-hour breach counts must not be negative.

### Compatibility rule

For each compatible department-type population:

`Four-hour breaches <= applicable A&E attendances`

A breach count greater than its compatible attendance count must be flagged
for investigation.

### TOTAL-row treatment

The published `TOTAL` record is excluded from provider-level analytical
aggregation.

The published control record remains available for reconciliation.

### Validation rules

KPI-005 is valid only when:

1. required breach fields are present;
2. breach fields are numeric;
3. breach counts are non-negative;
4. breach counts do not exceed their compatible attendance populations;
5. provider business keys are unique at the required analytical grain;
6. provider-level breach sums reconcile with applicable published totals;
7. booked-appointment breach fields have not been double counted.

### Relationship to KPI-004

KPI-005 supplies the breach-count component used by:

`KPI-004 Four-hour A&E performance`

where:

`Within four hours = Applicable attendances - Four-hour breaches`

and:

`Four-hour performance (%) = (Applicable attendances - Four-hour breaches) / Applicable attendances Ã— 100`

### Historical comparability

Breach trends require comparable provider coverage and performance-reporting
methodology across periods.

Periods affected by missing performance submissions or changes in reporting
scope must be identified before comparison.

### Limitations

Absolute breach volume is sensitive to attendance volume.

The KPI does not explain why breaches occurred and should be considered
alongside attendance activity, percentage performance, DTA waits, and relevant
operational context.

### Governance status

**KPI-005: DEFINITION APPROVED**

Implementation in production Python, SQL, and DAX remains subject to
cross-platform reconciliation and validity testing.
---

## KPI-006: Long waits after decision to admit

### Business question

How many patients experienced a long wait between the decision to admit and
admission for the selected provider population and reporting period?

### Analytical purpose

This KPI measures delays occurring after the decision to admit.

It provides an indicator of post-decision-to-admit patient-flow pressure and
must remain analytically separate from general four-hour A&E performance.

### Source fields

The source provides two separate DTA waiting-time categories:

- `Patients who have waited 4-12 hs from DTA to admission`
- `Patients who have waited 12+ hrs from DTA to admission`

### Component measures

The project will retain two controlled component measures:

`DTA 4-12 hour waits`

and:

`DTA 12+ hour waits`

These components must remain separately identifiable.

### Combined long-wait measure

Where a combined measure is required:

`Total DTA waits of 4+ hours = DTA 4-12 hour waits + DTA 12+ hour waits`

Mathematically:

`DTA_4plus = DTA_4_12 + DTA_12plus`

### Unit

Count of patients reported in the applicable DTA waiting-time category.

### Direction

Lower is better for this defined measure.

### Analytical grain

The base calculation is performed at:

`Reporting period + Org Code`

### Aggregation rule

DTA waiting counts are additive across compatible provider-period records.

For higher analytical grains:

`Grouped DTA waits = Sum of compatible provider-period DTA waits`

The 4-12 hour and 12+ hour components must also remain available separately
after aggregation.

### Null treatment

Missing DTA values are not automatically interpreted as zero.

Missingness must first be assessed as a data-quality condition.

### Negative-value rule

DTA waiting counts must not be negative.

### TOTAL-row treatment

The published `TOTAL` record is excluded from provider-level analytical
aggregation.

The published control record remains available for reconciliation.

### Validation rules

KPI-006 is valid only when:

1. required DTA fields are present;
2. DTA fields are numeric;
3. DTA counts are non-negative;
4. provider business keys are unique at the required analytical grain;
5. provider-level DTA sums reconcile with applicable published totals;
6. the 4-12 hour and 12+ hour categories remain separately identifiable.

### Relationship to four-hour A&E performance

KPI-006 must not be treated as equivalent to KPI-004 or KPI-005.

The measures use different pathway concepts:

`Four-hour A&E performance`

relates to the A&E pathway from arrival to the relevant departure outcome.

`DTA long waits`

relate specifically to the period after the decision to admit and before
admission.

### Relationship to arrival-based 12-hour measures

`DTA 12+ hour waits`

must not be interpreted as equivalent to:

`12+ hours from arrival`

published from ECDS-derived analysis.

The two measures start their clocks at different stages of the emergency-care
pathway.

### Historical comparability

Long-term DTA analysis must account for applicable changes in reporting
definitions and provider coverage.

Comparability must be established before calculating trends across periods
affected by methodological changes.

### Limitations

The aggregate DTA measure does not identify:

- why a delay occurred;
- the patient's clinical condition;
- bed availability;
- staffing levels;
- individual patient pathways;
- whether a particular operational factor caused the delay.

The measure can identify operational patterns requiring investigation but
cannot establish their cause on its own.

### Governance status

**KPI-006: DEFINITION APPROVED**

The 4-12 hour and 12+ hour component measures remain mandatory analytical
outputs.

Implementation in production Python, SQL, and DAX remains subject to
cross-platform reconciliation and validity testing.
---

## KPI-007: DTA long-wait rate

### Business question

What proportion of the appropriate decision-to-admit population experiences a
long wait between decision to admit and admission?

### Analytical purpose

A rate-based DTA measure could provide additional context to the absolute
long-wait counts defined in KPI-006.

However, a rate is valid only when the denominator represents the same
eligible population as the DTA long-wait numerator.

### Candidate numerators

Potential numerator components available in the current source are:

- `Patients who have waited 4-12 hs from DTA to admission`
- `Patients who have waited 12+ hrs from DTA to admission`

A possible combined numerator is:

`DTA 4+ hour waits = DTA 4-12 hour waits + DTA 12+ hour waits`

### Denominator

**No denominator is approved at this stage.**

The current aggregate source contains emergency-admission measures, but the
project has not yet established from applicable authoritative guidance that
any available admission field is an exact denominator for the population
eligible for these DTA waiting-time counts.

### Prohibited implementation

The project must not automatically calculate:

`DTA long-wait rate = DTA long waits / total A&E attendances`

or:

`DTA long-wait rate = DTA long waits / total emergency admissions`

or:

`DTA long-wait rate = DTA long waits / emergency admissions via A&E`

without confirming that the denominator represents the same eligible
population as the numerator.

### Unit

Percentage, if an authoritative compatible denominator is established.

### Direction

Lower would be better for the defined measure.

### Zero-denominator treatment

If a valid denominator is subsequently approved and the denominator is zero,
the rate will be treated as undefined rather than automatically reported as
zero percent.

### Analytical grain

If approved later, numerator and denominator must be aligned at the same
reporting-period and organisational grain before division.

### Aggregation rule

If the KPI becomes implementation-ready, higher-level rates must be calculated
from aggregated compatible numerator and denominator counts.

Provider percentages must not be averaged as a substitute for this
calculation.

### Validation requirement

Before implementation, the project must document:

1. the authoritative denominator definition;
2. the eligible population;
3. compatibility between numerator and denominator;
4. exclusions;
5. treatment of transfers where applicable;
6. historical comparability;
7. validation rules.

### Current analytical treatment

Until those requirements are satisfied, KPI-006 absolute DTA long-wait counts
will be used for analysis.

The 4-12 hour and 12+ hour components will remain separately available.

### Governance status

**KPI-007: PROVISIONAL - DENOMINATOR NOT APPROVED**

The KPI must not be implemented in production Python, SQL, DAX, or executive
reporting until the denominator is explicitly validated.

---

## KPI-008: Month-on-month change

### Business question

How has a selected A&E measure changed compared with the immediately preceding
comparable reporting month?

### Analytical purpose

Month-on-month change identifies short-term movement in activity or
performance.

It can be applied to approved measures such as:

- total A&E attendances;
- emergency admissions;
- four-hour breaches;
- DTA long waits.

Percentage-point change should be considered separately for percentage KPIs
such as four-hour performance.

### Absolute-change formula

`Absolute change = Current month value - Previous month value`

Mathematically:

`Î”X = X_t - X_(t-1)`

### Percentage-change formula

`Month-on-month change (%) = ((Current month - Previous month) / Previous month) Ã— 100`

Mathematically:

`MoM (%) = ((X_t - X_(t-1)) / X_(t-1)) Ã— 100`

### Interpretation

A positive percentage means the selected measure increased compared with the
previous comparable month.

A negative percentage means the selected measure decreased.

Whether an increase is favourable depends on the measure.

For example:

- increased attendance represents higher recorded demand;
- increased breaches indicates deterioration on that measure;
- increased DTA long waits indicates deterioration on that measure.

### Percentage KPIs

For an existing percentage KPI such as four-hour performance, change should
also be expressed in percentage points where appropriate.

Formula:

`Percentage-point change = Current percentage - Previous percentage`

For example:

`74.0% - 72.5% = +1.5 percentage points`

This must not be described as a 1.5% relative increase.

### Analytical grain

Current and previous values must refer to the same analytical grain.

For provider-level analysis:

`Org Code + current reporting month`

must be compared with:

`Same Org Code + immediately preceding comparable reporting month`

### Previous-period rule

The previous record in a table is not automatically the previous reporting
month.

The implementation must verify chronological reporting-period continuity.

If August is missing, an October record must not automatically treat September
or another available row as the previous month unless that period is the
defined comparison period.

### Zero-baseline treatment

If:

`Previous month value = 0`

percentage change is undefined because division by zero would occur.

In this situation:

- absolute change may still be reported;
- percentage change must return null or another explicitly documented
  undefined state;
- the result must not automatically be reported as 0%.

### Missing-period treatment

If the required previous month is unavailable, MoM percentage change must not
be calculated as though the time series were complete.

The missing comparison period must be flagged.

### Null treatment

Missing current or previous values are not automatically interpreted as zero.

Missingness must first be investigated as a data-quality condition.

### Comparability rule

Month-on-month comparison requires the two periods to use compatible:

- measure definitions;
- provider coverage;
- organisational mappings;
- reporting methodology;
- analytical grain.

A methodological or organisational break may make a mathematically valid
change analytically misleading.

### Aggregation rule

For additive measures, aggregate the compatible underlying counts to the
required analytical grain first and then calculate the change.

For rate or percentage KPIs, recalculate each period's KPI from its approved
numerator and denominator before comparing the two periods.

### Seasonal interpretation

Month-on-month movement can be influenced by seasonal and calendar effects.

A single monthly increase or decrease should therefore not automatically be
interpreted as a sustained trend.

MoM should later be considered alongside:

- year-on-year comparison;
- rolling measures;
- longer-term trends;
- relevant operational context.

### Validation rules

KPI-008 is valid only when:

1. the underlying KPI is approved;
2. reporting periods are chronologically valid;
3. the required previous month exists;
4. current and previous periods are comparable;
5. values are calculated at the same analytical grain;
6. a zero previous value does not produce division by zero;
7. missing values have not been silently converted to zero.

### Limitations

MoM change shows short-term movement but does not establish:

- seasonality;
- sustained improvement or deterioration;
- statistical significance;
- causation;
- the operational reason for the change.

### Governance status

**KPI-008: DEFINITION APPROVED**

Implementation is deferred until the project contains a validated multi-month
analytical dataset.

Production Python, SQL, and DAX implementations must produce reconciled
results.

---

## KPI-009: Year-on-year change

### Business question

How has a selected A&E measure changed compared with the same comparable
reporting month one year earlier?

### Analytical purpose

Year-on-year change compares the same reporting month across consecutive
years.

This can provide better seasonal context than month-on-month comparison
because the comparison is made against the corresponding month in the
previous year.

### Absolute-change formula

`Absolute YoY change = Current-period value - Prior-year comparable value`

Mathematically:

`Î”X_YoY = X_t - X_(t-12)`

### Percentage-change formula

`YoY change (%) = ((Current value - Prior-year value) / Prior-year value) Ã— 100`

Mathematically:

`YoY (%) = ((X_t - X_(t-12)) / X_(t-12)) Ã— 100`

### Example comparison

A September 2026 value should normally be compared with September 2025 for a
standard monthly year-on-year comparison.

It should not simply be compared with the record located 12 rows earlier
unless the time series has first been validated as complete and correctly
ordered.

### Percentage KPIs

For percentage measures such as four-hour performance, change should also be
reported in percentage points where appropriate.

Formula:

`Percentage-point change = Current percentage - Prior-year percentage`

For example:

`76.0% - 73.5% = +2.5 percentage points`

This is different from a relative percentage change of 2.5%.

### Direction

Contextual.

The meaning of an increase depends on the underlying measure.

For example:

- increased attendances indicate higher recorded demand;
- increased four-hour performance indicates improvement on that measure;
- increased four-hour breaches indicate deterioration on that measure;
- increased DTA long waits indicate deterioration on that measure.

### Analytical grain

Current and prior-year values must refer to the same analytical grain.

For provider-level analysis:

`Org Code + reporting month`

must be compared with:

`Same compatible Org Code + same reporting month in the previous year`

where provider and methodological comparability have been established.

### Comparable-period rule

The prior-year observation must represent the corresponding reporting month.

The implementation must validate reporting dates explicitly rather than
assuming row position represents a 12-month interval.

### Zero-baseline treatment

If:

`Prior-year value = 0`

relative percentage change is undefined.

In that situation:

- absolute change may still be reported;
- relative percentage change must return null or another documented undefined
  state;
- the calculation must not automatically return zero percent.

### Missing-period treatment

If the required prior-year reporting month is missing, YoY change must not be
calculated as though a valid comparison exists.

The missing comparison period must be flagged.

### Comparability rule

Year-on-year analysis requires compatible:

- measure definitions;
- provider coverage;
- organisation mappings;
- department classifications;
- reporting methodology;
- analytical grain.

Known methodological changes must be evaluated before a YoY comparison is
approved.

### Aggregation rule

For additive measures, compatible component values should first be aggregated
to the required analytical grain and then compared.

For rates or percentages, each period's KPI should first be recalculated from
its approved numerator and denominator before the change is measured.

### Relationship to seasonality

Year-on-year comparison helps control for some recurring calendar-season
effects by comparing the same month across years.

However, a single YoY comparison does not prove that a change represents a
long-term trend or that seasonality has been fully controlled.

### Validation rules

KPI-009 is valid only when:

1. the underlying KPI is approved;
2. the current reporting period is valid;
3. the corresponding prior-year month exists;
4. provider and methodological comparability have been established;
5. current and prior-year values use the same analytical grain;
6. zero prior-year values are handled without division by zero;
7. missing values are not silently converted to zero;
8. known comparability breaks are documented.

### Limitations

Year-on-year change does not by itself establish:

- sustained improvement or deterioration;
- statistical significance;
- causation;
- the reason for a change;
- complete adjustment for seasonal or calendar effects.

### Governance status

**KPI-009: DEFINITION APPROVED**

Implementation is deferred until the project contains validated, comparable
historical reporting periods.

Production Python, SQL, and DAX implementations must produce reconciled
results.

---

## KPI-010: Rolling 12-month activity

### Business question

What is the total activity recorded across the most recent 12 complete,
comparable reporting months?

### Analytical purpose

Rolling 12-month activity provides a longer-term view of activity than a
single monthly observation.

It can reduce emphasis on individual monthly fluctuations and support
assessment of sustained activity patterns.

### Applicable measures

The rolling calculation may be applied to approved additive count measures,
including:

- KPI-001 Total A&E attendances;
- KPI-002 Total emergency admissions;
- Emergency admissions via A&E;
- KPI-005 Four-hour breaches;
- KPI-006 DTA long-wait counts.

Percentage and rate KPIs require separate treatment and must not simply be
summed across months.

### Formula

For an additive monthly measure:

`Rolling 12-month activity = X_t + X_(t-1) + ... + X_(t-11)`

Mathematically:

`R12_t = Î£ X_(t-i), for i = 0,...,11`

The window therefore contains the current reporting month and the preceding
11 complete months.

### Example

For a rolling 12-month value ending September 2026, the required reporting
window is:

`October 2025 through September 2026`

provided all 12 reporting months are present and comparable.

### Unit

The unit is inherited from the underlying additive measure.

For example:

- attendance count;
- emergency-admission count;
- breach count;
- DTA long-wait count.

### Direction

Contextual.

The interpretation depends on the underlying measure.

For example:

- increased rolling attendance indicates greater recorded activity;
- increased rolling breach volume indicates more breaches;
- increased rolling DTA long waits indicates more long-wait events.

### Analytical grain

At provider level, the rolling window is calculated independently for each
`Org Code`.

The required grain is therefore based on:

`Org Code + reporting month`

before the rolling calculation is applied.

### Complete-window rule

A rolling 12-month value requires 12 complete consecutive reporting months.

The presence of 12 observations is not sufficient if those observations do
not represent 12 consecutive monthly periods.

### Missing-period treatment

If any required month in the 12-month window is missing, the project will not
silently treat the missing month as zero.

The rolling result must be treated as incomplete unless a separately
documented and justified rule is established.

### Provider-continuity rule

Provider-level rolling analysis requires investigation of organisation-code,
organisation-name, organisational-structure, and reporting-footprint changes
within the rolling window.

A provider restructuring or code change must not be treated automatically as
continuous provider history.

### Comparability rule

All months within the rolling window must use sufficiently comparable:

- measure definitions;
- provider coverage;
- reporting methodology;
- analytical grain.

A methodological break within the window must be identified before the
rolling result is approved for interpretation.

### Aggregation rule

For an additive measure:

`Rolling 12-month total = Sum of the 12 compatible monthly values`

The calculation must not include the published `TOTAL` control record in
addition to provider-level records.

### Rate and percentage measures

Rates and percentages must not be summed across the 12-month window.

Where a rolling rate is required, the approved underlying numerator and
denominator must be aggregated across the compatible 12-month period and the
rate recalculated.

For example:

`Rolling rate = Sum of 12-month numerator / Sum of 12-month denominator Ã— 100`

### Validation rules

KPI-010 is valid only when:

1. the underlying measure is approved;
2. exactly 12 required consecutive reporting months are available;
3. the reporting months are correctly ordered;
4. no required month has been silently replaced by zero;
5. provider continuity has been assessed where applicable;
6. the underlying measure is methodologically comparable across the window;
7. the calculation uses only compatible analytical records;
8. percentage and rate measures are not summed directly.

### Relationship to other trend measures

KPI-010 complements:

- KPI-008 Month-on-month change;
- KPI-009 Year-on-year change.

These measures answer different analytical questions.

MoM describes short-term movement.

YoY compares corresponding months across years.

Rolling 12-month activity describes aggregate activity across a moving
12-month window.

### Limitations

A rolling 12-month total can smooth short-term variation and may therefore
hide recent deterioration or improvement.

It also does not establish:

- causation;
- seasonality on its own;
- statistical significance;
- the operational reason for a trend.

Monthly values should remain available alongside rolling measures.

### Governance status

**KPI-010: DEFINITION APPROVED**

Implementation is deferred until the project contains at least 12 complete,
consecutive, validated and comparable reporting months.

Production Python, SQL, and DAX implementations must produce reconciled
results.

---

## KPI-011: Provider percentile

### Business question

Where does a provider's value for an approved A&E measure sit within a defined
comparable-provider distribution for the same reporting period?

### Analytical purpose

Provider percentile provides contextual benchmarking by describing a
provider's relative position within a defined comparison population.

It can help identify providers whose activity or performance is unusually high
or low relative to the selected cohort.

### Eligible underlying measures

Provider percentile may be calculated only for an approved and comparable
underlying measure.

Examples may include:

- total A&E attendances;
- four-hour performance;
- four-hour breaches;
- A&E admission rate;
- DTA long-wait counts.

The interpretation depends on the direction of the underlying measure.

### Comparison cohort

A percentile is meaningful only after the comparison population has been
defined.

The cohort must use provider records that are compatible in relation to:

- reporting period;
- KPI definition;
- analytical grain;
- provider coverage;
- relevant service configuration;
- applicable reporting methodology;
- data-quality eligibility.

Providers must not automatically be pooled into one comparison population
simply because they appear in the same source file.

### Conceptual calculation

For a provider value `x`, its percentile describes its relative position within
the values of the approved comparison cohort.

The exact percentile algorithm and tie-handling method must be documented
before implementation.

### Unit

Percentile position, conventionally represented on a 0 to 100 scale.

### Direction

Context depends on the underlying KPI.

For example:

- a high percentile for four-hour performance may indicate comparatively
  stronger performance;
- a high percentile for four-hour breaches may indicate comparatively greater
  breach volume;
- a high percentile for attendance volume indicates comparatively high demand,
  not necessarily better or worse performance.

The dashboard must not assume that a higher percentile is universally better.

### Analytical grain

Percentiles are calculated across the approved provider cohort for the same
reporting period and underlying KPI definition.

A provider must not be compared against values from different reporting
periods within the same cross-sectional percentile calculation.

### Missing-value treatment

Providers without a valid value for the selected KPI are excluded from the
percentile calculation.

A missing value must not be interpreted as zero.

The number of providers included in the comparison cohort should remain
visible or auditable.

### Tie handling

Providers may have identical KPI values.

The chosen percentile/ranking implementation must define how ties are treated
and use the same approach in Python, SQL, and Power BI where equivalent
outputs are required.

### Comparability rule

Before percentile calculation, the project must confirm that providers are
sufficiently comparable for the selected analytical question.

Where service configuration or methodology materially affects comparability,
the cohort should be restricted or the limitation made explicit.

### Relationship to ranking

Percentile and rank are related but different outputs.

A rank describes ordered position.

A percentile describes relative position within the defined distribution.

The project may present both where useful, but their definitions must remain
explicit.

### Validation rules

KPI-011 is valid only when:

1. the underlying KPI is approved;
2. all provider values relate to the same compatible reporting period;
3. the comparison cohort is explicitly defined;
4. invalid or missing KPI values are handled consistently;
5. the number of eligible providers is known;
6. tie handling is documented;
7. the percentile method is consistent across analytical implementations;
8. methodological or provider-footprint differences have been assessed.

### Interpretation

A percentile is a benchmarking signal rather than an explanation.

An unusual percentile may identify a provider requiring further analytical
investigation.

It does not establish why the provider differs from the comparison group.

### Limitations

Provider percentile does not automatically account for:

- case mix;
- department mix;
- provider size;
- local population characteristics;
- capacity;
- staffing;
- service configuration;
- other operational factors.

The result should therefore be interpreted alongside contextual and
provider-level analysis.

### Governance status

**KPI-011: DEFINITION APPROVED WITH IMPLEMENTATION METHOD PENDING**

The conceptual KPI is approved.

Before production implementation, the project must select and document the
precise percentile algorithm, tie-handling method, and comparable-provider
cohort rules.

Python, SQL, and Power BI outputs must use equivalent definitions before
cross-platform reconciliation is considered successful.

---

## KPI-012: Data quality pass rate

### Business question

What proportion of executed data-quality checks passed for the selected source,
dataset, or pipeline stage?

### Analytical purpose

This KPI provides a concise summary of executed data-quality checks.

It supports monitoring of data-quality assurance but does not replace detailed
exception reporting or critical-failure controls.

### Numerator

Number of executed data-quality checks with a passing result.

### Denominator

Total number of executed data-quality checks included in the defined quality
assessment.

### Formula

`Data quality pass rate (%) = Passed checks / Executed checks Ã— 100`

Mathematically:

`DQ_pass (%) = (N_pass / N_executed) Ã— 100`

### Unit

Percentage.

### Direction

Higher is generally better.

However, the percentage must always be interpreted alongside check severity
and individual critical failures.

### Zero-denominator treatment

If:

`Executed checks = 0`

then the data-quality pass rate is undefined.

The implementation must return null or another explicitly documented
undefined state rather than reporting 0% or 100%.

### Check eligibility

Only checks actually executed within the defined quality assessment belong in
the denominator.

Checks that are:

- not applicable;
- not executed;
- technically unavailable;

must not automatically be counted as failures or passes.

Their status should remain separately visible.

### Severity rule

The overall percentage must not override critical quality controls.

For example, a dataset could theoretically pass most checks while failing a
critical schema, uniqueness, or reconciliation check.

Therefore, the project must display:

- overall pass rate;
- number of passed checks;
- number of failed checks;
- critical failures;
- warning-level failures where applicable;
- checks not executed or not applicable.

### Critical-failure rule

A critical failure can cause the source or pipeline stage to fail its quality
gate even where the overall pass rate is high.

The quality-gate decision and the pass-rate percentage are therefore related
but distinct outputs.

### Analytical grain

The KPI may be calculated at defined quality-assessment levels such as:

- source file;
- reporting month;
- pipeline stage;
- transformed dataset.

The analytical level must be identified explicitly whenever the KPI is
reported.

### Aggregation rule

Data-quality pass rates must not automatically be averaged across files,
months, or pipeline stages.

Where an overall rate is required:

`Overall DQ pass rate = Sum of passed eligible checks / Sum of executed eligible checks Ã— 100`

provided the included checks form a meaningful combined assessment.

### Validation rules

KPI-012 is valid only when:

1. each included check has a defined result;
2. passed and failed states are consistently encoded;
3. non-executed checks are distinguishable from failed checks;
4. not-applicable checks are distinguishable from failed checks;
5. denominator construction is documented;
6. severity is retained;
7. critical failures remain independently visible;
8. no division by zero occurs.

### Relationship to quality gates

This KPI summarises check outcomes.

It does not independently decide whether data are analytically usable.

A separate quality gate determines whether the source or pipeline stage may
proceed.

For example:

`High pass rate + critical reconciliation failure = quality gate failure`

### Limitations

A single percentage can conceal important differences in:

- severity;
- analytical impact;
- check coverage;
- quality dimensions;
- pipeline stage;
- source complexity.

The pass rate must therefore be accompanied by detailed quality information.

### Governance status

**KPI-012: DEFINITION APPROVED**

Implementation will use the controlled data-quality framework and must retain
severity and individual check results alongside the summary percentage.
---

# KPI catalogue quality gate

The controlled KPI catalogue has been reviewed against the NHS A&E domain
guide and the currently available Monthly A&E source.

## Definition coverage

- [x] KPI-001 Total A&E attendances
- [x] KPI-002 Total emergency admissions
- [x] KPI-003 A&E admission rate
- [x] KPI-004 Four-hour A&E performance
- [x] KPI-005 Four-hour A&E breaches
- [x] KPI-006 DTA long waits
- [x] KPI-007 DTA long-wait rate reviewed
- [x] KPI-008 Month-on-month change
- [x] KPI-009 Year-on-year change
- [x] KPI-010 Rolling 12-month activity
- [x] KPI-011 Provider percentile
- [x] KPI-012 Data quality pass rate

## Governance exceptions

### KPI-007

**PROVISIONAL - DENOMINATOR NOT APPROVED**

No production implementation is permitted until an authoritative compatible
denominator has been established.

### KPI-011

**DEFINITION APPROVED WITH IMPLEMENTATION METHOD PENDING**

The exact percentile algorithm, tie-handling rule, and comparable-provider
cohort definition must be documented before production implementation.

### Time-dependent KPIs

KPI-008, KPI-009, and KPI-010 are supported by the validated 25-month analytical
dataset covering September 2024 through September 2026.

Their implementation remains subject to the controlled definitions,
comparability rules, complete-period requirements, null and zero-baseline
treatment, and validation requirements documented in the individual KPI
specifications.

## Cross-platform implementation requirement

Where a KPI is implemented across multiple analytical platforms, the
definition must remain consistent across:

- Python;
- SQL;
- Power BI DAX.

Material differences between implementations must be investigated rather than
accepted as rounding or tooling differences without evidence.

## Analytical safeguards

The catalogue explicitly controls:

- numerator and denominator compatibility;
- analytical grain;
- aggregation;
- null handling;
- zero-denominator handling;
- double-counting risk;
- provider comparability;
- historical comparability;
- validation rules;
- limitations.

## Decision

**KPI CATALOGUE QUALITY GATE: PASS WITH CONTROLLED EXCEPTIONS**

The KPI catalogue is sufficiently defined to support data modelling and ETL
design for approved measures.

Provisional or implementation-dependent KPIs remain subject to their documented
governance restrictions.

### Governance status

**KPI-012: DEFINITION APPROVED**

Implementation will use the controlled data-quality framework and must retain
severity and individual check results alongside the summary percentage.
---

# KPI catalogue quality gate

