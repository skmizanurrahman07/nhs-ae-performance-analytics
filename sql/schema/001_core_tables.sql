CREATE SCHEMA IF NOT EXISTS core;

CREATE TABLE IF NOT EXISTS core.provider_monthly (
    reporting_period_raw VARCHAR NOT NULL,
    reporting_month DATE NOT NULL,
    org_code VARCHAR NOT NULL,
    org_name VARCHAR NOT NULL,
    parent_org VARCHAR NOT NULL,

    ae_attendances_type1 BIGINT NOT NULL,
    ae_attendances_type2 BIGINT NOT NULL,
    ae_attendances_other BIGINT NOT NULL,

    ae_booked_attendances_type1 BIGINT NOT NULL,
    ae_booked_attendances_type2 BIGINT NOT NULL,
    ae_booked_attendances_other BIGINT NOT NULL,

    ae_over_4hrs_type1 BIGINT NOT NULL,
    ae_over_4hrs_type2 BIGINT NOT NULL,
    ae_over_4hrs_other BIGINT NOT NULL,

    ae_booked_over_4hrs_type1 BIGINT NOT NULL,
    ae_booked_over_4hrs_type2 BIGINT NOT NULL,
    ae_booked_over_4hrs_other BIGINT NOT NULL,

    dta_wait_4_12hrs BIGINT NOT NULL,
    dta_wait_12plus_hrs BIGINT NOT NULL,

    emergency_admissions_ae_type1 BIGINT NOT NULL,
    emergency_admissions_ae_type2 BIGINT NOT NULL,
    emergency_admissions_ae_other BIGINT NOT NULL,
    other_emergency_admissions BIGINT NOT NULL,

    PRIMARY KEY (reporting_month, org_code)
);
