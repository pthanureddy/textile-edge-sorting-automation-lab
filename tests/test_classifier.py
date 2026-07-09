from pathlib import Path

from textile_edge_sorting.classifier import classify_item
from textile_edge_sorting.image import extract_vision_features
from textile_edge_sorting.models import TextileRoute
from textile_edge_sorting.sensor import parse_sensor_frame


def test_classify_good_blue_cotton_for_reuse_or_cotton_recycling() -> None:
    frame = "station=line-1;nir=0.74;visible=0.62;moisture=0.08;weight_g=312;timestamp=2026-07-09T12:00:00Z"
    ppm = Path("examples/blue_cotton.ppm").read_text(encoding="utf-8")

    result = classify_item(parse_sensor_frame(frame), extract_vision_features(ppm))

    assert result.route in {TextileRoute.REUSE, TextileRoute.COTTON_RECYCLING}
    assert result.confidence >= 0.7


def test_classify_dark_patch_for_manual_inspection() -> None:
    frame = "station=line-1;nir=0.31;visible=0.20;moisture=0.35;weight_g=188;timestamp=2026-07-09T12:00:02Z"
    ppm = Path("examples/dark_reject.ppm").read_text(encoding="utf-8")

    result = classify_item(parse_sensor_frame(frame), extract_vision_features(ppm))

    assert result.route == TextileRoute.MANUAL_INSPECTION
    assert "manual inspection" in result.reason
