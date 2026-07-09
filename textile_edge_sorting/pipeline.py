from __future__ import annotations

from textile_edge_sorting.classifier import classify_item
from textile_edge_sorting.control import build_actuator_command
from textile_edge_sorting.image import extract_vision_features
from textile_edge_sorting.integration import build_influx_line, build_mqtt_message, build_opcua_tags
from textile_edge_sorting.models import ClassificationResponse
from textile_edge_sorting.sensor import parse_sensor_frame


def process_textile_item(serial_frame: str, image_ppm: str) -> ClassificationResponse:
    sensor = parse_sensor_frame(serial_frame)
    vision = extract_vision_features(image_ppm)
    result = classify_item(sensor, vision)
    command = build_actuator_command(result)
    topic, payload = build_mqtt_message(result, command)

    return ClassificationResponse(
        station_id=result.station_id,
        route=result.route.value,
        confidence=result.confidence,
        reason=result.reason,
        actuator={
            "diverter_gate": command.diverter_gate,
            "conveyor_speed_mps": command.conveyor_speed_mps,
            "reject_enabled": command.reject_enabled,
            "settle_time_ms": command.settle_time_ms,
        },
        mqtt_topic=topic,
        mqtt_payload=payload,
        opcua_tags=build_opcua_tags(result, command),
        influx_line=build_influx_line(result, command),
    )
