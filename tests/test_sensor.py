from datetime import timezone

import pytest

from textile_edge_sorting.sensor import parse_sensor_frame


def test_parse_sensor_frame_reads_all_fields() -> None:
    frame = "station=line-1;nir=0.74;visible=0.62;moisture=0.08;weight_g=312;timestamp=2026-07-09T12:00:00Z"

    reading = parse_sensor_frame(frame)

    assert reading.station_id == "line-1"
    assert reading.nir == 0.74
    assert reading.visible == 0.62
    assert reading.moisture == 0.08
    assert reading.weight_g == 312
    assert reading.timestamp.tzinfo == timezone.utc


def test_parse_sensor_frame_rejects_missing_field() -> None:
    frame = "station=line-1;nir=0.74;visible=0.62;moisture=0.08;timestamp=2026-07-09T12:00:00Z"

    with pytest.raises(ValueError, match="weight_g"):
        parse_sensor_frame(frame)


def test_parse_sensor_frame_rejects_out_of_range_value() -> None:
    frame = "station=line-1;nir=1.4;visible=0.62;moisture=0.08;weight_g=312;timestamp=2026-07-09T12:00:00Z"

    with pytest.raises(ValueError, match="nir"):
        parse_sensor_frame(frame)
