# **Sensor Simulation Repository**

Structure (`Python`)

```
rideau-canal-sensor-simulation/
├── README.md                  # Current Document: Setup and usage instructions
├── sensor_simulator.py        # Main simulation script
├── requirements.txt           # Python dependencies
├── .env.example              # Example environment variables
├── .gitignore
└── config/
    └── sensor_config.json    # Optional: sensor configuration
```

1. **Overview**
   - What the simulator does
   - Technologies used (Python, Azure IoT SDK)

2. **Prerequisites**
3. **Installation**
4. **Configuration**
5. **Usage**
6. **Code Structure**
   - Main components explained
   - Key functions
7. **Sensor Data Format**
**Data Ranges for Ottawa Winter**:
- Ice thickness (cm): Normally 25–45 cm. Safe ≥30, caution ≥25, unsafe <25.
- Surface temperature (°C): Usually near external temp, but can be a few degrees colder. Safe ≤ -2°C, caution ≤ 0°C, unsafe >0°C.
- Snow accumulation (cm): 0–30 cm, can increase gradually after a snow event.
- External temperature (°C): -25°C to +5°C.

**JSON schema:**

**Example Output:**

8. **Troubleshooting**
   - Common issues and fixes