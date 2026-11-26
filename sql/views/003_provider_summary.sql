CREATE OR REPLACE VIEW analytics.provider_summary AS

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
)

SELECT
    org_code,

    ARG_MAX(org_name, reporting_month)
        AS latest_org_name,

    COUNT(DISTINCT reporting_month)
        AS months_present,

    SUM(total_attendances)
        AS total_attendances,

    AVG(total_attendances)
        AS average_monthly_attendances,

    SUM(emergency_admissions)
        AS emergency_admissions,

    AVG(emergency_admissions)
        AS average_monthly_admissions

FROM provider_kpis

GROUP BY org_code

ORDER BY
    total_attendances DESC,
    org_code;
