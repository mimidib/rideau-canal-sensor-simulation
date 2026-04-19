# Rideau Canal Sensor Simulator

Simulates three IoT sensor devices on the Rideau Canal Skateway, sending real-time environmental readings to Azure IoT Hub every 10 seconds.

## Repository Structure

```
rideau-canal-sensor-simulation/
├── README.md               # This file
├── sensor_simulator.py     # Main simulation script
├── requirements.txt        # Python dependencies
├── .env.dows-lake          # Example env file for Dow's Lake device
├── .env.fifth-avenue       # Example env file for Fifth Avenue device
├── .env.nac                # Example env file for NAC device
└── .gitignore
```

---

## Overview

The simulator generates realistic sensor readings for three locations:
- **Dow's Lake**
- **Fifth Avenue**
- **NAC (National Arts Centre)**

Each device sends a JSON payload every 10 seconds containing:
- Ice thickness (cm)
- Surface temperature (°C)
- Snow accumulation (cm)
- External temperature (°C)

Data ranges are modelled on real Ottawa winter conditions. Ice thickness and snow accumulation are derived from external temperature to produce physically plausible readings.

**Technologies used:** Python 3, `azure-iot-device`, `python-dotenv`

---

## Prerequisites

- Python 3.8+
- Three devices registered in Azure IoT Hub (one per location)
- Device connection strings for each device

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/mimidib/rideau-canal-sensor-simulation
cd rideau-canal-sensor-simulation

# 2. Create and activate a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Configuration

Copy the example `.env` file for the location you want to run and fill in your real connection string:

```bash
cp .env.dows-lake .env.dows-lake.local
```

Each `.env` file requires two variables:

```
IOTHUB_DEVICE_CONNECTION_STRING=HostName=your-hub.azure-devices.net;DeviceId=your-device;SharedAccessKey=...
LOCATION="dows-lake"
```

Get the connection string from: **Azure Portal → IoT Hub → Devices → [device name] → Primary Connection String**

---

## Usage

Run one terminal per location, passing the corresponding `.env` file as an argument:

```bash
# Terminal 1
python sensor_simulator.py .env.dows-lake

# Terminal 2
python sensor_simulator.py .env.fifth-avenue

# Terminal 3
python sensor_simulator.py .env.nac
```

Press `Ctrl+C` to stop a simulator. It will disconnect cleanly from IoT Hub.

---

## Code Structure

### `generate_sensor_data(location)`
Generates one reading as a JSON string. Produces realistic Ottawa winter values:
- `external_temperature`: random between -40°C and +10°C
- `surface_temperature`: derived from external temp ± small offset
- `ice_thickness`: linearly mapped from temperature (colder = thicker), with random variation
- `snow_accumulation`: 0 if above freezing, otherwise random 0–30cm

### `send_to_iot_hub(client, data)`
Sends one JSON message to IoT Hub via the device client. Logs success or failure without crashing the loop.

### `main()`
Creates the IoT Hub client once, then loops every 10 seconds: generate data → send → sleep. Handles `KeyboardInterrupt` for clean shutdown.

---

## Sensor Data Format

### JSON Schema

```json
{
  "location": "string",
  "timestamp": "ISO 8601 UTC string",
  "external_temperature": "float (°C)",
  "surface_temperature": "float (°C)",
  "ice_thickness": "float (cm)",
  "snow_accumulation": "float (cm)"
}
```

### Example Output

```json
{
  "location": "Dow's Lake",
  "timestamp": "2026-04-17T18:32:01.123456+00:00",
  "external_temperature": -12.4,
  "surface_temperature": -13.8,
  "ice_thickness": 34.2,
  "snow_accumulation": 8.7
}
```

---

## Troubleshooting

**`IOTHUB_DEVICE_CONNECTION_STRING is not set`**
You did not pass an `.env` file argument, or the file is missing the variable. Run as:
```bash
python sensor_simulator.py .env.dows-lake
```

**`Error sending message to IoT Hub`**
- Check your connection string is correct and not expired
- Confirm the device is registered in IoT Hub
- Check your internet connection

**`ModuleNotFoundError: No module named 'azure'`**
Your virtual environment is not activated, or dependencies are not installed:
```bash
.venv\Scripts\activate
pip install -r requirements.txt
```
