# Creates a KUBERNETES Service with a deployment that has a single pod running a Postgres database

The Postgres database is called `solardata` and it has table called `solar_panels_data` with the following schema:

```sql
CREATE TABLE solar_panels_data (
    panel_id UUID PRIMARY KEY,
    recorded_at TIMESTAMP NOT NULL,
    power_kwh FLOAT NOT NULL,
    latitude FLOAT,
    longitude FLOAT
);
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