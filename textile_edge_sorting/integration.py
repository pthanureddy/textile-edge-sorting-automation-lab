from __future__ import annotations

import json

from textile_edge_sorting.models import ActuatorCommand, ClassificationResult


def build_mqtt_message(result: ClassificationResult, command: ActuatorCommand) -> tuple[str, dict[str, object]]:
    topic = f"dotank/textile/{result.station_id}/classification"
    payload = {
        "station_id": result.station_id,
        "route": result.route.value,
        "confidence": result.confidence,
        "reason": result.reason,
        "actuator": {
            "diverter_gate": command.diverter_gate,
            "conveyor_speed_mps": command.conveyor_speed_mps,
            "reject_enabled": command.reject_enabled,
            "settle_time_ms": command.settle_time_ms,
        },
        "timestamp": result.sensor.timestamp.isoformat().replace("+00:00", "Z"),
    }
    return topic, payload


def mqtt_payload_json(result: ClassificationResult, command: ActuatorCommand) -> str:
    _, payload = build_mqtt_message(result, command)
    return json.dumps(payload, sort_keys=True)


def build_opcua_tags(result: ClassificationResult, command: ActuatorCommand) -> dict[str, object]:
    prefix = f"ns=2;s=DoTank.Sorting.{result.station_id}"
    return {
        f"{prefix}.Route": result.route.value,
        f"{prefix}.Confidence": result.confidence,
        f"{prefix}.DiverterGate": command.diverter_gate,
        f"{prefix}.ConveyorSpeedMps": command.conveyor_speed_mps,
        f"{prefix}.RejectEnabled": command.reject_enabled,
    }


def build_influx_line(result: ClassificationResult, command: ActuatorCommand) -> str:
    tags = f"station={_escape_tag(result.station_id)},route={_escape_tag(result.route.value)}"
    fields = (
        f"confidence={result.confidence},"
        f"nir={result.sensor.nir},"
        f"visible={result.sensor.visible},"
        f"moisture={result.sensor.moisture},"
        f"weight_g={result.sensor.weight_g},"
        f"conveyor_speed_mps={command.conveyor_speed_mps}"
    )
    timestamp_ns = int(result.sensor.timestamp.timestamp() * 1_000_000_000)
    return f"textile_sorting,{tags} {fields} {timestamp_ns}"


def _escape_tag(value: str) -> str:
    return value.replace(" ", "\\ ").replace(",", "\\,").replace("=", "\\=")
