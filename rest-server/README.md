Use this curl to add new data for a solar panel to the database:
```shell
curl -X POST http://localhost/add_panel_data \
-H "Content-Type: application/json" \
-d '{"panelId": "EC1", "powerKw": 83.7}'
```

Use this curl to insert a new solar panel to the data base but make sure to add data powerKw data for the solar panel after adding it other wise it will have no power data displayed on the website.

```shell
curl -X POST http://localhost/add_panel \
-H "Content-Type: application/json" \
-d '{"panelId": "CASE1", "name": "Center for Academic Success and Engagement", "latitude": 40.006293039976065, "longitude": -105.27009839853278}'
```