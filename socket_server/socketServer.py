import os
import random
import threading
import time

import psycopg2
import redis
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=os.getenv("PSQL_HOST") or "localhost",
    database="solardata",
    user="postgres",
    password="12345678",
    port=os.getenv("PSQL_PORT") or "5433",
)

r = redis.Redis(host=os.getenv("REDIS_HOST") or "localhost", port=6379, db=0)


def wait_for_queue(queue_name):
    item = r.blpop(queue_name)
    if item is not None:
        # Do something with the popped item
        print("Item popped from the queue:", item)
        # Continue with further actions
        # ...
        return item[1].decode("utf-8")
    else:
        print("No item popped from the queue")
        return None


def get_latest_panel_data(panel_id="EC1"):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT power_kw FROM solar_panels_data WHERE panel_id = %s ORDER BY data_id DESC LIMIT 1",
        (panel_id,),
    )
    result = cursor.fetchone()
    cursor.close()

    return result[0] if result else None


def send_latest_panel_data():
    while True:
        panel_id = wait_for_queue("solarPanelData")
        random_kw = get_latest_panel_data(panel_id)
        print("Panel ID:", panel_id)
        print("Sending new number:", random_kw)
        if random_kw is not None:
            socketio.emit(
                "NewPanelData", {"powerKw": str(random_kw), "panelId": panel_id}
            )


@app.route("/socket/random")
def index():
    random_number = random.randint(1, 100)  # Generate a random number
    return f"Random Number Generator: {random_number}"


if __name__ == "__main__":
    threading.Thread(target=send_latest_panel_data).start()
    socketio.run(
        app,
        host="0.0.0.0",
        port=os.getenv("SERVER_PORT") or 5001,
        allow_unsafe_werkzeug=True,
    )
