CREATE OR REPLACE VIEW analytics.provider_pressure AS

WITH provider_measures AS (
    SELECT
        reporting_month,
        org_code,
        org_name,

        ae_attendances_type1
        + ae_attendances_type2
        + ae_attendances_other
        + ae_booked_attendances_type1
        + ae_booked_attendances_type2
        + ae_booked_attendances_other
            AS total_attendances,

        emergency_admissions_ae_type1
        + emergency_admissions_ae_type2
        + emergency_admissions_ae_other
        + other_emergency_admissions
            AS emergency_admissions,

        ae_over_4hrs_type1
        + ae_over_4hrs_type2
        + ae_over_4hrs_other
        + ae_booked_over_4hrs_type1
        + ae_booked_over_4hrs_type2
        + ae_booked_over_4hrs_other
            AS four_hour_breaches,

        dta_wait_4_12hrs
            AS dta_waits_4_12hrs,

        dta_wait_12plus_hrs
            AS dta_waits_12plus_hrs,

        dta_wait_4_12hrs
        + dta_wait_12plus_hrs
            AS total_dta_waits_4plus_hrs

    FROM core.provider_monthly
),

metadata AS (
    SELECT
        org_code,
        ARG_MAX(org_name, reporting_month)
            AS latest_org_name,
        COUNT(DISTINCT reporting_month)
            AS months_present,
        COUNT(DISTINCT org_name)
            AS organisation_name_count
    FROM provider_measures
    GROUP BY org_code
),

current_period AS (
    SELECT
        org_code,
        total_attendances
            AS current_total_attendances,
        emergency_admissions
            AS current_emergency_admissions,
        four_hour_breaches
            AS current_four_hour_breaches,
        dta_waits_4_12hrs
            AS current_dta_waits_4_12hrs,
        dta_waits_12plus_hrs
            AS current_dta_waits_12plus_hrs,
        total_dta_waits_4plus_hrs
            AS current_total_dta_waits_4plus_hrs
    FROM provider_measures
    WHERE reporting_month = DATE '2026-09-01'
),

comparison_period AS (
    SELECT
        org_code,
        total_attendances
            AS comparison_total_attendances,
        emergency_admissions
            AS comparison_emergency_admissions,
        four_hour_breaches
            AS comparison_four_hour_breaches,
        dta_waits_4_12hrs
            AS comparison_dta_waits_4_12hrs,
        dta_waits_12plus_hrs
            AS comparison_dta_waits_12plus_hrs,
        total_dta_waits_4plus_hrs
            AS comparison_total_dta_waits_4plus_hrs
    FROM provider_measures
    WHERE reporting_month = DATE '2025-09-01'
),

comparison AS (
    SELECT
        current_period.*,
        comparison_period.* EXCLUDE (org_code),
        metadata.latest_org_name,
        metadata.months_present,
        metadata.organisation_name_count
    FROM current_period
    INNER JOIN comparison_period
        ON current_period.org_code = comparison_period.org_code
    LEFT JOIN metadata
        ON current_period.org_code = metadata.org_code
),

changes AS (
    SELECT
        *,

        current_four_hour_breaches
        - comparison_four_hour_breaches
            AS four_hour_breaches_absolute_change,

        current_dta_waits_4_12hrs
        - comparison_dta_waits_4_12hrs
            AS dta_waits_4_12hrs_absolute_change,

        current_dta_waits_12plus_hrs
        - comparison_dta_waits_12plus_hrs
            AS dta_waits_12plus_hrs_absolute_change,

        current_total_dta_waits_4plus_hrs
        - comparison_total_dta_waits_4plus_hrs
            AS total_dta_waits_4plus_hrs_absolute_change

    FROM comparison
),

derived AS (
    SELECT
        *,

        four_hour_breaches_absolute_change::DOUBLE
        / NULLIF(comparison_four_hour_breaches, 0)
            AS four_hour_breaches_percentage_change,

        dta_waits_4_12hrs_absolute_change::DOUBLE
        / NULLIF(comparison_dta_waits_4_12hrs, 0)
            AS dta_waits_4_12hrs_percentage_change,

        dta_waits_12plus_hrs_absolute_change::DOUBLE
        / NULLIF(comparison_dta_waits_12plus_hrs, 0)
            AS dta_waits_12plus_hrs_percentage_change,

        total_dta_waits_4plus_hrs_absolute_change::DOUBLE
        / NULLIF(comparison_total_dta_waits_4plus_hrs, 0)
            AS total_dta_waits_4plus_hrs_percentage_change,

        LEAST(
            current_total_attendances,
            comparison_total_attendances
        ) >= 10000
            AS meets_attendance_threshold,

        LEAST(
            current_emergency_admissions,
            comparison_emergency_admissions
        ) >= 1000
            AS meets_admission_threshold,

        months_present = 25
            AS full_period_coverage,

        organisation_name_count > 1
            AS provider_name_changed

    FROM changes
)

SELECT
    org_code,
    current_total_attendances,
    current_emergency_admissions,
    current_four_hour_breaches,
    current_dta_waits_4_12hrs,
    current_dta_waits_12plus_hrs,
    current_total_dta_waits_4plus_hrs,
    comparison_total_attendances,
    comparison_emergency_admissions,
    comparison_four_hour_breaches,
    comparison_dta_waits_4_12hrs,
    comparison_dta_waits_12plus_hrs,
    comparison_total_dta_waits_4plus_hrs,
    latest_org_name,
    months_present,
    organisation_name_count,
    four_hour_breaches_absolute_change,
    four_hour_breaches_percentage_change,
    dta_waits_4_12hrs_absolute_change,
    dta_waits_4_12hrs_percentage_change,
    dta_waits_12plus_hrs_absolute_change,
    dta_waits_12plus_hrs_percentage_change,
    total_dta_waits_4plus_hrs_absolute_change,
    total_dta_waits_4plus_hrs_percentage_change,
    meets_attendance_threshold,
    meets_admission_threshold,
    full_period_coverage,
    provider_name_changed,

    meets_attendance_threshold
    AND full_period_coverage
        AS breach_analysis_eligible,

    meets_admission_threshold
    AND full_period_coverage
        AS dta_analysis_eligible

FROM derived
ORDER BY org_code;
