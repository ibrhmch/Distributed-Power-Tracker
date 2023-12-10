import random
import threading
import time

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
CORS(
    app
)  # Enable CORS for all domains. For specific domains, use CORS(app, origins=["http://localhost:3000"])
socketio = SocketIO(
    app, cors_allowed_origins="http://localhost:3000"
)  # Allow your React app's origin


def send_random_number():
    while True:
        time.sleep(5)
        random_number = random.randint(1, 100)
        socketio.emit("new_number", {"number": random_number})


@app.route("/")
def index():
    return "Random Number Generator"


if __name__ == "__main__":
    threading.Thread(target=send_random_number).start()
    socketio.run(app, port=5001)
