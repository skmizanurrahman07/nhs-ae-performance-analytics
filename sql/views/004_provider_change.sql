CREATE OR REPLACE VIEW analytics.provider_change AS

WITH provider_kpis AS (
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
            AS emergency_admissions

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

    FROM provider_kpis
    GROUP BY org_code
),

current_period AS (
    SELECT
        org_code,
        total_attendances AS current_attendances,
        emergency_admissions AS current_admissions

    FROM provider_kpis
    WHERE reporting_month = DATE '2026-09-01'
),

comparison_period AS (
    SELECT
        org_code,
        total_attendances AS comparison_attendances,
        emergency_admissions AS comparison_admissions

    FROM provider_kpis
    WHERE reporting_month = DATE '2025-09-01'
),

comparison AS (
    SELECT
        current_period.org_code,
        current_period.current_attendances,
        current_period.current_admissions,
        comparison_period.comparison_attendances,
        comparison_period.comparison_admissions,
        metadata.latest_org_name,
        metadata.months_present,
        metadata.organisation_name_count,

        current_period.current_attendances
        - comparison_period.comparison_attendances
            AS attendance_absolute_change,

        current_period.current_admissions
        - comparison_period.comparison_admissions
            AS admission_absolute_change

    FROM current_period

    INNER JOIN comparison_period
        ON current_period.org_code = comparison_period.org_code

    LEFT JOIN metadata
        ON current_period.org_code = metadata.org_code
),

derived AS (
    SELECT
        *,

        attendance_absolute_change::DOUBLE
        / NULLIF(comparison_attendances, 0)
            AS attendance_percentage_change,

        admission_absolute_change::DOUBLE
        / NULLIF(comparison_admissions, 0)
            AS admission_percentage_change,

        LEAST(
            current_attendances,
            comparison_attendances
        ) >= 10000
            AS meets_volume_threshold,

        months_present = 25
            AS full_period_coverage,

        organisation_name_count > 1
            AS provider_name_changed

    FROM comparison
)

SELECT
    org_code,
    current_attendances,
    current_admissions,
    comparison_attendances,
    comparison_admissions,
    latest_org_name,
    months_present,
    organisation_name_count,
    attendance_absolute_change,
    admission_absolute_change,
    attendance_percentage_change,
    admission_percentage_change,
    meets_volume_threshold,
    full_period_coverage,
    provider_name_changed,

    meets_volume_threshold
    AND full_period_coverage
        AS analysis_eligible

FROM derived

ORDER BY
    analysis_eligible DESC,
    attendance_absolute_change DESC;
