CREATE OR REPLACE VIEW analytics.monthly_pressure AS

WITH provider_pressure AS (
    SELECT
        reporting_month,

        ae_over_4hrs_type1
        + ae_over_4hrs_type2
        + ae_over_4hrs_other
        + ae_booked_over_4hrs_type1
        + ae_booked_over_4hrs_type2
        + ae_booked_over_4hrs_other
            AS four_hour_breaches,

        dta_wait_4_12hrs AS dta_waits_4_12hrs,

        dta_wait_12plus_hrs AS dta_waits_12plus_hrs,

        dta_wait_4_12hrs
        + dta_wait_12plus_hrs
            AS total_dta_waits_4plus_hrs

    FROM core.provider_monthly
),

monthly AS (
    SELECT
        reporting_month,
        SUM(four_hour_breaches) AS four_hour_breaches,
        SUM(dta_waits_4_12hrs) AS dta_waits_4_12hrs,
        SUM(dta_waits_12plus_hrs) AS dta_waits_12plus_hrs,
        SUM(total_dta_waits_4plus_hrs)
            AS total_dta_waits_4plus_hrs

    FROM provider_pressure
    GROUP BY reporting_month
),

with_lags AS (
    SELECT
        *,

        LAG(four_hour_breaches, 1)
            OVER (ORDER BY reporting_month)
            AS four_hour_breaches_previous_month,

        LAG(four_hour_breaches, 12)
            OVER (ORDER BY reporting_month)
            AS four_hour_breaches_previous_year,

        LAG(dta_waits_4_12hrs, 1)
            OVER (ORDER BY reporting_month)
            AS dta_waits_4_12hrs_previous_month,

        LAG(dta_waits_4_12hrs, 12)
            OVER (ORDER BY reporting_month)
            AS dta_waits_4_12hrs_previous_year,

        LAG(dta_waits_12plus_hrs, 1)
            OVER (ORDER BY reporting_month)
            AS dta_waits_12plus_hrs_previous_month,

        LAG(dta_waits_12plus_hrs, 12)
            OVER (ORDER BY reporting_month)
            AS dta_waits_12plus_hrs_previous_year,

        LAG(total_dta_waits_4plus_hrs, 1)
            OVER (ORDER BY reporting_month)
            AS total_dta_previous_month,

        LAG(total_dta_waits_4plus_hrs, 12)
            OVER (ORDER BY reporting_month)
            AS total_dta_previous_year

    FROM monthly
)

SELECT
    reporting_month,
    four_hour_breaches,
    dta_waits_4_12hrs,
    dta_waits_12plus_hrs,
    total_dta_waits_4plus_hrs,

    four_hour_breaches::DOUBLE
        / NULLIF(four_hour_breaches_previous_month, 0)
        - 1.0
        AS four_hour_breaches_monthly_change,

    four_hour_breaches::DOUBLE
        / NULLIF(four_hour_breaches_previous_year, 0)
        - 1.0
        AS four_hour_breaches_year_on_year_change,

    dta_waits_4_12hrs::DOUBLE
        / NULLIF(dta_waits_4_12hrs_previous_month, 0)
        - 1.0
        AS dta_waits_4_12hrs_monthly_change,

    dta_waits_4_12hrs::DOUBLE
        / NULLIF(dta_waits_4_12hrs_previous_year, 0)
        - 1.0
        AS dta_waits_4_12hrs_year_on_year_change,

    dta_waits_12plus_hrs::DOUBLE
        / NULLIF(dta_waits_12plus_hrs_previous_month, 0)
        - 1.0
        AS dta_waits_12plus_hrs_monthly_change,

    dta_waits_12plus_hrs::DOUBLE
        / NULLIF(dta_waits_12plus_hrs_previous_year, 0)
        - 1.0
        AS dta_waits_12plus_hrs_year_on_year_change,

    total_dta_waits_4plus_hrs::DOUBLE
        / NULLIF(total_dta_previous_month, 0)
        - 1.0
        AS total_dta_waits_4plus_hrs_monthly_change,

    total_dta_waits_4plus_hrs::DOUBLE
        / NULLIF(total_dta_previous_year, 0)
        - 1.0
        AS total_dta_waits_4plus_hrs_year_on_year_change

FROM with_lags
ORDER BY reporting_month;
