# Textile Edge Sorting Automation Lab

Python edge automation lab for textile sorting and circular-flow prototyping. It combines synthetic sensor frames, simple computer-vision features, routing logic, REST APIs, MQTT-style payloads, OPC UA tag mapping, and InfluxDB line protocol output.

This is a portfolio project for digitalization, AI, and automation work in textile applications. It is not connected to real machines, PLCs, Arduino, ESP32, Raspberry Pi, or production sorting equipment. The hardware boundary is represented through simulated serial frames and integration payloads so the software behavior can be reviewed and tested without lab hardware.

## What It Demonstrates

- Parsing serial-style textile sensor frames from an edge station.
- Extracting simple computer-vision features from PPM textile image patches.
- Classifying textile items into reuse, cotton recycling, synthetic recycling, or manual inspection.
- Producing actuator commands for conveyor speed, diverter gate, and reject state.
- Exposing REST endpoints for edge classification and health checks.
- Emitting MQTT-style JSON messages, OPC UA tag maps, and InfluxDB line protocol telemetry.
- Running automated tests and GitHub Actions CI.

## Repository Structure

```text
textile_edge_sorting/
  api.py          FastAPI endpoints
  classifier.py   feature scoring and routing logic
  cli.py          command-line processing flow
  control.py      actuator command generation
  image.py        PPM parsing and vision feature extraction
  integration.py  MQTT payloads, OPC UA tags, InfluxDB line protocol
  models.py       typed domain models
  sensor.py       serial frame parser
examples/
  sensor_frames.txt
  blue_cotton.ppm
  dark_reject.ppm
docs/
  architecture.md
  lab-boundary.md
```

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -e ".[dev]"
python -m pytest
```

On macOS or Linux, activate with `source .venv/bin/activate`.

## Run The CLI

```powershell
textile-edge-sort --frame-file examples/sensor_frames.txt --image examples/blue_cotton.ppm
```

Example output:

```json
{
  "station_id": "line-1",
  "route": "cotton_recycling",
  "confidence": 0.82,
  "actuator": {
    "diverter_gate": "A",
    "conveyor_speed_mps": 0.42
  }
}
```

## Run The API

```powershell
uvicorn textile_edge_sorting.api:app --reload
```

Submit a sample edge classification:

```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{
    "serial_frame": "station=line-1;nir=0.74;visible=0.62;moisture=0.08;weight_g=312;timestamp=2026-07-09T12:00:00Z",
    "image_ppm": "P3\n2 2\n255\n35 72 160 40 76 168 42 78 171 38 74 164"
  }'
```

## Test Coverage

The pytest suite covers:

- serial frame parsing and validation,
- PPM image parsing,
- computer-vision feature extraction,
- textile routing decisions,
- actuator command generation,
- MQTT, OPC UA, and InfluxDB integration payloads,
- REST API success and validation behavior,
- CLI execution.

## Limitations

- Computer vision uses lightweight color and texture features, not a trained deep-learning model.
- MQTT, OPC UA, and InfluxDB integrations emit payloads but do not connect to live brokers, PLCs, or databases.
- PLC programming, EtherCAT, and real-time machine control are documented as production boundaries and not claimed as implemented.
- Physical prototyping with 3D printing, electronics, Arduino, ESP32, Raspberry Pi, and sensors would require lab hardware outside this workflow.
