-- Connect to the 'solardata' database
\connect solardata;

-- Create 'solar_panels' table
CREATE TABLE solar_panels (
    panel_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL
);

-- Create 'solar_panels_data' table
CREATE TABLE solar_panels_data (
    data_id SERIAL PRIMARY KEY,
    panel_id VARCHAR(255) NOT NULL,
    recorded_at TIMESTAMP NOT NULL,
    power_kw FLOAT NOT NULL,
    FOREIGN KEY (panel_id) REFERENCES solar_panels(panel_id)
);

-- Insert initial data into 'solar_panels'
INSERT INTO solar_panels (panel_id, name, latitude, longitude)
VALUES 
('EC1', 'Engineering Center', 40.007259752621174, -105.26350055410776),
('C4C1', 'Center For Community', 40.00389502140387, -105.26616659936727);

-- Insert initial data into 'solar_panels_data'
DO $$
DECLARE
    i INT;
    time_offset INTERVAL;
BEGIN
    FOR i IN 0..9 LOOP
        time_offset := (i * INTERVAL '5 minutes');

        -- Insert data for 'Engineering Center'
        INSERT INTO solar_panels_data (panel_id, recorded_at, power_kw)
        VALUES ('EC1', NOW() - time_offset, ROUND((RANDOM() * 100)::numeric, 2));

        -- Insert data for 'Center For Community'
        INSERT INTO solar_panels_data (panel_id, recorded_at, power_kw)
        VALUES ('C4C1', NOW() - time_offset, ROUND((RANDOM() * 100)::numeric, 2));
    END LOOP;
END
$$;
