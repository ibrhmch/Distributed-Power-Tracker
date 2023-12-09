CREATE DATABASE solardata;

\c solardata;

CREATE TABLE solar_panels_data (
    panel_id UUID PRIMARY KEY,
    recorded_at TIMESTAMP NOT NULL,
    power_kwh FLOAT NOT NULL,
    latitude FLOAT,
    longitude FLOAT
);
