import json
from pathlib import Path

from fastapi.testclient import TestClient

from textile_edge_sorting.api import app
from textile_edge_sorting.cli import main


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_classify_endpoint_returns_integration_payloads() -> None:
    frame = "station=line-1;nir=0.74;visible=0.62;moisture=0.08;weight_g=312;timestamp=2026-07-09T12:00:00Z"
    ppm = Path("examples/blue_cotton.ppm").read_text(encoding="utf-8")

    response = client.post("/classify", json={"serial_frame": frame, "image_ppm": ppm})

    assert response.status_code == 200
    body = response.json()
    assert body["station_id"] == "line-1"
    assert body["mqtt_topic"] == "dotank/textile/line-1/classification"
    assert "influx_line" in body
    assert body["opcua_tags"]


def test_classify_endpoint_rejects_invalid_request() -> None:
    response = client.post("/classify", json={"serial_frame": "bad", "image_ppm": "bad"})

    assert response.status_code == 422


def test_cli_prints_json(capsys) -> None:
    exit_code = main(["--frame-file", "examples/sensor_frames.txt", "--image", "examples/blue_cotton.ppm"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert exit_code == 0
    assert payload["station_id"] == "line-1"
    assert payload["actuator"]["diverter_gate"]
