from __future__ import annotations

from textile_edge_sorting.models import ClassificationResult, SensorReading, TextileRoute, VisionFeatures


def classify_item(sensor: SensorReading, vision: VisionFeatures) -> ClassificationResult:
    quality_score = _quality_score(sensor, vision)
    synthetic_score = _synthetic_score(sensor, vision)
    cotton_score = _cotton_score(sensor, vision)

    if quality_score < 0.35 or sensor.moisture > 0.3 or vision.brightness < 0.12:
        return ClassificationResult(
            station_id=sensor.station_id,
            route=TextileRoute.MANUAL_INSPECTION,
            confidence=round(1 - quality_score, 2),
            reason="low quality, high moisture, or low visibility requires manual inspection",
            sensor=sensor,
            vision=vision,
        )

    if quality_score > 0.78 and sensor.moisture < 0.12:
        return ClassificationResult(
            station_id=sensor.station_id,
            route=TextileRoute.REUSE,
            confidence=round(quality_score, 2),
            reason="high quality score with low moisture supports reuse route",
            sensor=sensor,
            vision=vision,
        )

    if cotton_score >= synthetic_score:
        return ClassificationResult(
            station_id=sensor.station_id,
            route=TextileRoute.COTTON_RECYCLING,
            confidence=round(cotton_score, 2),
            reason="NIR and visible response match cotton recycling profile",
            sensor=sensor,
            vision=vision,
        )

    return ClassificationResult(
        station_id=sensor.station_id,
        route=TextileRoute.SYNTHETIC_RECYCLING,
        confidence=round(synthetic_score, 2),
        reason="spectral response and image features match synthetic recycling profile",
        sensor=sensor,
        vision=vision,
    )


def _quality_score(sensor: SensorReading, vision: VisionFeatures) -> float:
    dry_score = max(0.0, 1.0 - sensor.moisture * 2.2)
    visibility_score = min(1.0, sensor.visible * 1.2)
    texture_score = max(0.0, 1.0 - vision.texture_variance * 10)
    return _clamp((dry_score * 0.45) + (visibility_score * 0.35) + (texture_score * 0.2))


def _cotton_score(sensor: SensorReading, vision: VisionFeatures) -> float:
    spectral = (sensor.nir * 0.65) + (sensor.visible * 0.2)
    image = (1.0 - abs(vision.blue_ratio - 0.45)) * 0.15
    return _clamp(spectral + image)


def _synthetic_score(sensor: SensorReading, vision: VisionFeatures) -> float:
    spectral = ((1.0 - sensor.nir) * 0.55) + (sensor.visible * 0.2)
    image = vision.blue_ratio * 0.25
    return _clamp(spectral + image)


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))
