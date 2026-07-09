from pathlib import Path

import pytest

from textile_edge_sorting.image import extract_vision_features, parse_ppm_pixels


def test_parse_ppm_pixels_reads_ascii_image() -> None:
    ppm = Path("examples/blue_cotton.ppm").read_text(encoding="utf-8")

    pixels = parse_ppm_pixels(ppm)

    assert len(pixels) == 9
    assert pixels[0] == (35, 72, 160)


def test_extract_vision_features_detects_blue_dominance() -> None:
    ppm = Path("examples/blue_cotton.ppm").read_text(encoding="utf-8")

    features = extract_vision_features(ppm)

    assert features.mean_blue > features.mean_red
    assert features.blue_ratio > 0.45
    assert features.brightness > 0.25


def test_parse_ppm_pixels_rejects_wrong_size() -> None:
    with pytest.raises(ValueError, match="expected"):
        parse_ppm_pixels("P3\n2 2\n255\n0 0 0")
