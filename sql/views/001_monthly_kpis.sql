CREATE SCHEMA IF NOT EXISTS analytics;

CREATE OR REPLACE VIEW analytics.monthly_kpis AS

WITH provider_kpis AS (
    SELECT
        reporting_month,

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

monthly AS (
    SELECT
        reporting_month,
        SUM(total_attendances) AS total_attendances,
        SUM(emergency_admissions) AS emergency_admissions

    FROM provider_kpis
    GROUP BY reporting_month
),

with_lags AS (
    SELECT
        reporting_month,
        total_attendances,
        emergency_admissions,

        LAG(total_attendances, 1)
            OVER (ORDER BY reporting_month)
            AS previous_month_attendances,

        LAG(emergency_admissions, 1)
            OVER (ORDER BY reporting_month)
            AS previous_month_admissions,

        LAG(total_attendances, 12)
            OVER (ORDER BY reporting_month)
            AS previous_year_attendances,

        LAG(emergency_admissions, 12)
            OVER (ORDER BY reporting_month)
            AS previous_year_admissions

    FROM monthly
)

SELECT
    reporting_month,
    total_attendances,
    emergency_admissions,

    (
        total_attendances::DOUBLE
        / NULLIF(previous_month_attendances, 0)
    ) - 1.0 AS attendance_monthly_change,

    (
        emergency_admissions::DOUBLE
        / NULLIF(previous_month_admissions, 0)
    ) - 1.0 AS admission_monthly_change,

    (
        total_attendances::DOUBLE
        / NULLIF(previous_year_attendances, 0)
    ) - 1.0 AS attendance_year_on_year_change,

    (
        emergency_admissions::DOUBLE
        / NULLIF(previous_year_admissions, 0)
    ) - 1.0 AS admission_year_on_year_change

FROM with_lags
ORDER BY reporting_month;
