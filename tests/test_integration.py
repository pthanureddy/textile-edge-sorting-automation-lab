from pathlib import Path

from textile_edge_sorting.classifier import classify_item
from textile_edge_sorting.control import build_actuator_command
from textile_edge_sorting.image import extract_vision_features
from textile_edge_sorting.integration import build_influx_line, build_mqtt_message, build_opcua_tags, mqtt_payload_json
from textile_edge_sorting.sensor import parse_sensor_frame


def _result_and_command():
    frame = "station=line-1;nir=0.74;visible=0.62;moisture=0.08;weight_g=312;timestamp=2026-07-09T12:00:00Z"
    ppm = Path("examples/blue_cotton.ppm").read_text(encoding="utf-8")
    result = classify_item(parse_sensor_frame(frame), extract_vision_features(ppm))
    command = build_actuator_command(result)
    return result, command


def test_build_mqtt_message_contains_route_and_actuator() -> None:
    result, command = _result_and_command()

    topic, payload = build_mqtt_message(result, command)

    assert topic == "portfolio/lab/textile-sorting/line-1/edge-cell/sorter-01/state/classification"
    assert payload["route"] == result.route.value
    assert payload["actuator"]["diverter_gate"] == command.diverter_gate
    assert "line-1" in mqtt_payload_json(result, command)


def test_build_opcua_tags_uses_station_prefix() -> None:
    result, command = _result_and_command()

    tags = build_opcua_tags(result, command)

    assert "ns=2;s=DoTank.Sorting.line-1.Route" in tags
    assert tags["ns=2;s=DoTank.Sorting.line-1.DiverterGate"] == command.diverter_gate


def test_build_influx_line_contains_measurement_and_timestamp() -> None:
    result, command = _result_and_command()

    line = build_influx_line(result, command)

    assert line.startswith("textile_sorting,station=line-1,route=")
    assert "confidence=" in line
    assert line.endswith("000000000")
