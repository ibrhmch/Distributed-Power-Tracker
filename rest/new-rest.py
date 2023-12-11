import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="solardata",
    user="postgres",
    password="12345678",
    port="5433",
)


# Define the endpoint to retrieve data
@app.route("/get_panels", methods=["GET"])
def get_data():
    # Create a cursor object to interact with the database
    cur = conn.cursor()

    # Execute a query to retrieve data from a table
    cur.execute("SELECT * FROM solar_panels")

    # Fetch all rows from the result set
    rows = cur.fetchall()

    # Close the cursor and the database connection
    cur.close()
    conn.close()

    # Convert the rows to a list of dictionaries
    data = []
    for row in rows:
        data.append(
            {
                "panel_id": row[0],
                "name": row[1],
                "latitude": row[2],
                "longitude": row[3],
            }
        )

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
            "SELECT power_kw FROM solar_panels_data WHERE panel_id = %s ORDER BY recorded_at DESC LIMIT 1",
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


if __name__ == "__main__":
    # Run the Flask application on port 3002
    app.run(port=3002)
