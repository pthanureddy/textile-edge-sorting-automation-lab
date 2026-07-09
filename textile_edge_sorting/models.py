from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class TextileRoute(str, Enum):
    REUSE = "reuse"
    COTTON_RECYCLING = "cotton_recycling"
    SYNTHETIC_RECYCLING = "synthetic_recycling"
    MANUAL_INSPECTION = "manual_inspection"


@dataclass(frozen=True)
class SensorReading:
    station_id: str
    nir: float
    visible: float
    moisture: float
    weight_g: float
    timestamp: datetime


@dataclass(frozen=True)
class VisionFeatures:
    mean_red: float
    mean_green: float
    mean_blue: float
    brightness: float
    texture_variance: float
    blue_ratio: float


@dataclass(frozen=True)
class ClassificationResult:
    station_id: str
    route: TextileRoute
    confidence: float
    reason: str
    sensor: SensorReading
    vision: VisionFeatures


@dataclass(frozen=True)
class ActuatorCommand:
    diverter_gate: str
    conveyor_speed_mps: float
    reject_enabled: bool
    settle_time_ms: int


class ClassificationRequest(BaseModel):
    serial_frame: str = Field(min_length=20)
    image_ppm: str = Field(min_length=20)


class ActuatorResponse(BaseModel):
    diverter_gate: str
    conveyor_speed_mps: float
    reject_enabled: bool
    settle_time_ms: int


class ClassificationResponse(BaseModel):
    station_id: str
    route: str
    confidence: float
    reason: str
    actuator: ActuatorResponse
    mqtt_topic: str
    mqtt_payload: dict[str, object]
    opcua_tags: dict[str, object]
    influx_line: str


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
