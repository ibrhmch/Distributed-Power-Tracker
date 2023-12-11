# Creates a KUBERNETES Service with a deployment that has a single pod running a Postgres database

The Postgres database is called `solardata` and it has table called `solar_panels_data` with the following schema:

```sql
CREATE TABLE solar_panels (
    panel_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL
);
```

```sql
CREATE TABLE solar_panels_data (
    data_id SERIAL PRIMARY KEY,
    panel_id VARCHAR(255) NOT NULL,
    recorded_at TIMESTAMP NOT NULL,
    power_kwh FLOAT NOT NULL,
    FOREIGN KEY (panel_id) REFERENCES solar_panels(panel_id)
);
```


## To create new solar panels, run:
```sql
INSERT INTO solar_panels (panel_id, name, latitude, longitude)
VALUES 
('EC1', 'Engineering Center', 140.007259752621174, -105.26350055410776),
('C4C1', 'Center For Community', 140.00389502140387, -105.26616659936727);
```

## To create new solar panel data, run:
```sql
DO $$
DECLARE
    i INT;
    time_offset INTERVAL;
BEGIN
    FOR i IN 0..9 LOOP
        time_offset := (i * INTERVAL '5 minutes');

        -- Insert data for 'Engineering Center'
        INSERT INTO solar_panels_data (panel_id, recorded_at, power_kwh)
        VALUES ('EC1', NOW() - time_offset, ROUND((RANDOM() * 100)::numeric, 2));

        -- Insert data for 'Center For Community'
        INSERT INTO solar_panels_data (panel_id, recorded_at, power_kwh)
        VALUES ('C4C1', NOW() - time_offset, ROUND((RANDOM() * 100)::numeric, 2));
    END LOOP;
END
$$;
```


## To create the deployment, run:
```bash
kubectl apply -f psql-deployment.yaml
```

## To start the service, run:
```bash
kubectl apply -f psql-service.yaml
```

## To connect to the database, first forward the port:
```bash
kubectl port-forward service/psql-service 5432:5432
```

followed by:
```bash
psql -h localhost -p 5432 -U postgres -d solardata
```

or you can connect to the pod and run psql from there:
```bash
kubectl exec -it <podname> -- sh

psql -U postgres -d solardata
```

Once connected, you can run SQL commands like:

```sql
select * from solar_panels_data;
```