DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'solardata') THEN
        CREATE DATABASE solardata;
    END IF;
END
$$;

\connect solardata;

CREATE TABLE IF NOT EXISTS solar_panels_data (
    panel_id UUID PRIMARY KEY,
    recorded_at TIMESTAMP NOT NULL,
    power_kwh FLOAT NOT NULL,
    latitude FLOAT,
    longitude FLOAT
);
