import os
from datetime import datetime

import psycopg2
import redis
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS
CORS(app)

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=os.getenv("PSQL_HOST") or "localhost",
    database="solardata",
    user="postgres",
    password="12345678",
    port=os.getenv("PSQL_PORT") or "5433",
)

r = redis.Redis(host=os.getenv("REDIS_HOST") or "localhost", port=6379, db=0)


# Define the endpoint to retrieve data
@app.route("/get_panels", methods=["GET"])
def get_data():
    # Create a cursor object to interact with the database
    cur = conn.cursor()

    # Execute a query to retrieve data from a table
    cur.execute("SELECT * FROM solar_panels")

    # Fetch all rows from the result set
    rows = cur.fetchall()

    # Convert the rows to a dictionary of dictionaries
    data = {}
    for row in rows:
        cur.execute(
            "SELECT power_kw FROM solar_panels_data WHERE panel_id = %s ORDER BY data_id DESC LIMIT 1",
            (row[0],),
        )

        # Fetch the latest power_kw from the result set
        power_kw = cur.fetchone()

        data[row[0]] = {  # row[0] is the panel_id
            "name": row[1],
            "latitude": row[2],
            "longitude": row[3],
            "powerKw": power_kw[0] if power_kw else None,
        }

    # Close the cursor
    cur.close()

    # Return the data as JSON
    return jsonify(data)


@app.route("/get_all_panels_data", methods=["POST"])
def get_all_panels_data():
    # Get the list of panel IDs from the request
    panel_ids = request.json

    print(panel_ids)

    # Create a cursor object to interact with the database
    cur = conn.cursor()

    # Dictionary to store panel_id: power_kw pairs
    panel_data = {}

    # Retrieve the latest power_kw for each panel_id
    for panel_id in panel_ids:
        # Execute the query to retrieve the latest power_kw
        cur.execute(
            "SELECT power_kw FROM solar_panels_data WHERE panel_id = %s ORDER BY data_id DESC LIMIT 1",
            (panel_id,),
        )

        # Fetch the latest power_kw from the result set
        row = cur.fetchone()

        # Add the panel_id: power_kw pair to the dictionary
        panel_data[panel_id] = row[0] if row else None

    # Close the cursor
    cur.close()

    # Return the panel data as JSON
    return jsonify(panel_data)


@app.route("/add_panel", methods=["POST"])
def add_panel():
    # Get the panel data from the request
    panel_data = request.json

    # Create a cursor object to interact with the database
    cur = conn.cursor()

    try:
        # Insert the panel data into the solar_panels table
        cur.execute(
            "INSERT INTO solar_panels (panel_id, name, latitude, longitude) VALUES (%s, %s, %s, %s)",
            (
                panel_data["panelId"],
                panel_data["name"],
                panel_data["latitude"],
                panel_data["longitude"],
            ),
        )

        # Commit the transaction
        conn.commit()
        return jsonify({"panelId": panel_data["panelId"]})

    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"{e}"}), 400
    finally:
        # Close the cursor
        cur.close()


@app.route("/add_panel_data", methods=["POST"])
def add_panel_data():
    # Get the panel data from the request
    panel_data = request.json

    # Create a cursor object to interact with the database
    cur = conn.cursor()

    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    try:
        # Insert the panel data into the solar_panels_data table
        cur.execute(
            "INSERT INTO solar_panels_data (panel_id, recorded_at, power_kw) VALUES (%s, %s, %s)",
            (panel_data["panelId"], current_timestamp, panel_data["powerKw"]),
        )

        # Commit the transaction
        conn.commit()

        r.lpush("solarPanelData", panel_data["panelId"])

        # Return a success message
        return jsonify({"message": "Panel data added successfully"})
    except Exception as e:
        conn.rollback()
        # Handle the error when the panel_id does not exist in the solar_panels table
        return jsonify({"error": f"{e}"}), 400
    finally:
        # Close the cursor
        cur.close()


if __name__ == "__main__":
    # Run the Flask application on port 3002
    app.run(port=os.getenv("SERVER_PORT") or 3002)
