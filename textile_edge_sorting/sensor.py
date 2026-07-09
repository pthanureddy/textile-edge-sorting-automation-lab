from __future__ import annotations

from datetime import datetime, timezone

from textile_edge_sorting.models import SensorReading


REQUIRED_FIELDS = {"station", "nir", "visible", "moisture", "weight_g", "timestamp"}


def parse_sensor_frame(frame: str) -> SensorReading:
    values = _parse_key_values(frame)
    missing = REQUIRED_FIELDS.difference(values)
    if missing:
        raise ValueError(f"missing sensor fields: {', '.join(sorted(missing))}")

    reading = SensorReading(
        station_id=values["station"],
        nir=_bounded_float(values["nir"], "nir", 0.0, 1.0),
        visible=_bounded_float(values["visible"], "visible", 0.0, 1.0),
        moisture=_bounded_float(values["moisture"], "moisture", 0.0, 1.0),
        weight_g=_bounded_float(values["weight_g"], "weight_g", 0.0, 5000.0),
        timestamp=_parse_timestamp(values["timestamp"]),
    )
    if not reading.station_id:
        raise ValueError("station must not be empty")
    return reading


def _parse_key_values(frame: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for chunk in frame.strip().split(";"):
        if not chunk:
            continue
        if "=" not in chunk:
            raise ValueError(f"invalid frame field: {chunk}")
        key, value = chunk.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def _bounded_float(raw: str, name: str, minimum: float, maximum: float) -> float:
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be numeric") from exc
    if value < minimum or value > maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}")
    return value


def _parse_timestamp(raw: str) -> datetime:
    normalized = raw.replace("Z", "+00:00")
    try:
        value = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError("timestamp must be ISO 8601") from exc
    if value.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return value.astimezone(timezone.utc)
