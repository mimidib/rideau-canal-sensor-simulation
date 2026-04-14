# ---- Imports ----
import os

from dotenv import load_dotenv

# ---- Config ----
load_dotenv()
CONNECTION_STRING = os.getenv("IOTHUB_CONNECTION_STRING")
INTERVAL_SECONDS = 10


def send_sensor_metrics():
    # ENV Var error Handling
    if not CONNECTION_STRING:
        print("IOTHUB_CONNECTION_STRING is not set. Please set it in the .env file.")
        return

    # 1. Create Client ONCE & connect (do this once to reduce latency and resource consumption and avoid IoT Hub Throttling

    # 2. Send Data to IoT Hub with Simulate sensor data (Timestamp, Ice thickness, temprerature, snow accumulation & external temperature)

    # 3. loop every 10 seconds to send simulated sensor data to IoT Hub
    return


if __name__ == "__main__":
    send_sensor_metrics()
