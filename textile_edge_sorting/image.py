from __future__ import annotations

from statistics import mean

from textile_edge_sorting.models import VisionFeatures


def parse_ppm_pixels(ppm: str) -> list[tuple[int, int, int]]:
    tokens = _tokenize_ppm(ppm)
    if len(tokens) < 4 or tokens[0] != "P3":
        raise ValueError("only ASCII P3 PPM images are supported")

    width = int(tokens[1])
    height = int(tokens[2])
    max_value = int(tokens[3])
    if width <= 0 or height <= 0 or max_value <= 0:
        raise ValueError("PPM dimensions and max value must be positive")

    expected_values = width * height * 3
    raw_values = tokens[4:]
    if len(raw_values) != expected_values:
        raise ValueError(f"expected {expected_values} RGB values, got {len(raw_values)}")

    pixels: list[tuple[int, int, int]] = []
    for index in range(0, len(raw_values), 3):
        rgb = tuple(int(value) for value in raw_values[index : index + 3])
        if any(channel < 0 or channel > max_value for channel in rgb):
            raise ValueError("RGB value outside PPM range")
        scaled = tuple(round(channel * 255 / max_value) for channel in rgb)
        pixels.append((scaled[0], scaled[1], scaled[2]))
    return pixels


def extract_vision_features(ppm: str) -> VisionFeatures:
    pixels = parse_ppm_pixels(ppm)
    reds = [pixel[0] for pixel in pixels]
    greens = [pixel[1] for pixel in pixels]
    blues = [pixel[2] for pixel in pixels]
    brightness_values = [(r + g + b) / (3 * 255) for r, g, b in pixels]
    avg_brightness = mean(brightness_values)
    texture_variance = mean((value - avg_brightness) ** 2 for value in brightness_values)
    blue_ratio = mean(b / max(r + g + b, 1) for r, g, b in pixels)

    return VisionFeatures(
        mean_red=mean(reds) / 255,
        mean_green=mean(greens) / 255,
        mean_blue=mean(blues) / 255,
        brightness=avg_brightness,
        texture_variance=texture_variance,
        blue_ratio=blue_ratio,
    )


def _tokenize_ppm(ppm: str) -> list[str]:
    tokens: list[str] = []
    for line in ppm.splitlines():
        clean = line.split("#", 1)[0].strip()
        if clean:
            tokens.extend(clean.split())
    return tokens
