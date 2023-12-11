import random
import threading
import time

import psycopg2
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

# Database connection parameters - update these with your database details
DB_HOST = "localhost"
DB_NAME = "solardata"
DB_USER = "postgres"
DB_PASS = "12345678"
DB_PORT = "5433"


def get_random_kwh_value():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )
    cursor = conn.cursor()
    cursor.execute("SELECT power_kw FROM solar_panels_data ORDER BY RANDOM() LIMIT 1")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None


def get_random_solarPanel_data(panel_id="EC1"):
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )
    cursor = conn.cursor()
    cursor.execute(
        "SELECT power_kw FROM solar_panels_data WHERE panel_id = %s ORDER BY RANDOM() LIMIT 1",
        (panel_id,),
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None


def send_random_solarPanel_data(panel_id="EC1"):
    while True:
        time.sleep(5)
        random_kw = get_random_solarPanel_data(panel_id)
        if random_kw is not None:
            socketio.emit("new_number", {"number": str(random_kw)})


def send_random_number():
    while True:
        time.sleep(5)
        random_kwh = get_random_kwh_value()
        if random_kwh is not None:
            socketio.emit("new_number", {"number": random_kwh})


@app.route("/")
def index():
    return "Random Number Generator"


if __name__ == "__main__":
    threading.Thread(target=send_random_solarPanel_data).start()
    socketio.run(app, port=5001)
