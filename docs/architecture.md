# Architecture

## Flow

```text
Serial sensor frame + textile image patch
  -> parser and validation
  -> vision feature extraction
  -> textile route classifier
  -> actuator command
  -> MQTT payload, OPC UA tags, InfluxDB line protocol
```

## Module Responsibilities

| Module | Responsibility |
| --- | --- |
| `sensor.py` | Parses serial-style key/value frames from an edge station. |
| `image.py` | Parses ASCII PPM image patches and extracts color/texture features. |
| `classifier.py` | Combines sensor and vision features into a routing decision. |
| `control.py` | Converts routing decisions into actuator commands. |
| `integration.py` | Builds MQTT-style JSON, OPC UA tags, and InfluxDB line protocol. |
| `api.py` | FastAPI endpoint for edge classification. |
| `cli.py` | Reproducible command-line processing path. |

## Design Notes

- The code is deterministic and small enough to review.
- It uses typed Pydantic models at the API boundary and dataclasses in the core.
- Integration adapters are payload builders rather than live external dependencies, so automated tests remain repeatable.
- The classifier is intentionally simple. The project demonstrates prototype integration, not production textile science.
