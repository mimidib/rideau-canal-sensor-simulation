# ---- Imports ----
import json
import logging
import os
import random
import sys
import time
from datetime import datetime, timezone

from azure.iot.device import IoTHubDeviceClient
from azure.iot.device.exceptions import IoTHubError
from dotenv import load_dotenv

# ---- Config ----
INTERVAL_SECONDS = 10

# Load the .env file provided in cli arg. Default to .env if no arg
ENV_FILE = sys.argv[1] if len(sys.argv) > 1 else ".env"
load_dotenv(ENV_FILE)

# Env variables
CONNECTION_STRING = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
LOCATION = os.getenv("LOCATION")

# Setup Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Empty env var error handling
logging.info("Checking env vars...")
if not CONNECTION_STRING:
    logging.error(
        "IOTHUB_DEVICE_CONNECTION_STRING is not set. Please set it in %s.", ENV_FILE
    )
    sys.exit(1)
elif not LOCATION:
    logging.error("LOCATION is not set. Please set it in %s.", ENV_FILE)
    sys.exit(1)


# ---- Functions ----
# Step 2. in flow
def generate_sensor_data(location):
    """Generates the simulated sensor data for the given location for Rideau Canal Skateway
    - Temperatures - These variables surface_temperature and external_temperature relate.
        If external temperature is above 0, snow accumulation should be close to 0, else anywhere in range.
        external_temperature: -40 to 10C.
        surface_temperature: -40 to 0.0C.
    - Ice_thickness - range between 0 and 60 cm.
        Depends on temperature.
        When temp is at its maximum (+10), thickness is at 0. When temp is at its minimum (-40), thickness is at 60. Everything in between scales proportionally
    - Snow_accumulation -  0-30cm
        If external temperature is above 0, snow accumulation should be close to 0, else anywhere in range."""

    timestamp = datetime.now(timezone.utc).isoformat()
    external_temperature = random.uniform(-40, 10)
    surface_temperature = external_temperature + random.uniform(-2, 1)

    # Derives a base thickness that shifts based on how cold it is.
    # Colder temp = higher base. Then add a small variation on that base.
    # visual representation of mapping thickness and temperature
    # temp:      -40 -------- -15 -------- +10
    # thickness:  60 -------- 30  --------   0
    # output = output_max * (input_max - input) / input_range
    base_thickness = (
        60 * (10 - external_temperature) / 50
    )  # maps thickness and temperature
    ice_thickness = base_thickness + random.uniform(
        -5, 5
    )  # add variation of -5 and +5 so its not predictable

    # If external temperature is above 0, snow accumulation should be close to 0, else anywhere in range.
    snow_accumulation = max(
        0,
        (0 + random.uniform(-1, 1))
        if (external_temperature > 0)
        else random.uniform(0, 30),
    )

    data = {
        "location": location,
        "timestamp": timestamp,
        "external_temperature": external_temperature,
        "surface_temperature": surface_temperature,
        "ice_thickness": ice_thickness,
        "snow_accumulation": snow_accumulation,
    }
    return json.dumps(data)  # dumps to a JSON string


# Step 3. in flow
def send_to_iot_hub(client, data):
    """Sends one event (dict) to IoT Hub, runs every 10 seconds"""
    # this is used in a loop in main
    # 2. Send Data to IoT Hub with Simulate sensor data (Timestamp, Ice thickness, temprerature, snow accumulation & external temperature)
    try:
        client.send_message(data)
        logging.info("Message successfully sent to IoT Hub: %s", data)
    except Exception as e:
        logging.error("Error sending message to IoT Hub: %s", e)


# ---- Main ----
def main():
    logging.info("Starting Sensor Simulator...")
    # 1. Create Client ONCE & connect (do this once to reduce latency and resource consumption and avoid IoT Hub Throttling
    assert (
        CONNECTION_STRING
    )  # guaranteed filled value by startup check above in Env Var checks

    logging.info("Creating IoT Hub Device Client...")
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    # connect client, not required, will stop script immediately if connection string invalid vs after 10s on first attempt
    client.connect()

    try:
        while True:
            # 2. Generate simulated Rideau Canal Metrics
            data = generate_sensor_data(LOCATION)

            # 3. Send JSON data to IoT Hub
            send_to_iot_hub(client, data)

            # 4. Sleep for 10s for interval
            time.sleep(INTERVAL_SECONDS)
    except KeyboardInterrupt:
        logging.info("Stopping simulator...")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
