from __future__ import annotations

from dataclasses import dataclass
import re


_SEGMENT_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")


@dataclass(frozen=True)
class UnsAddress:
    """Asset address for an enterprise/site/area/line/cell/asset UNS hierarchy."""

    enterprise: str
    site: str
    area: str
    line: str
    cell: str
    asset: str

    def __post_init__(self) -> None:
        for field_name, value in self._segments():
            _validate_segment(field_name, value)

    def topic(self, *information_path: str) -> str:
        if not information_path:
            raise ValueError("UNS topic requires an information path")
        for index, segment in enumerate(information_path):
            _validate_segment(f"information_path[{index}]", segment)

        asset_path = [value for _, value in self._segments()]
        return "/".join([*asset_path, *information_path])

    def _segments(self) -> tuple[tuple[str, str], ...]:
        return (
            ("enterprise", self.enterprise),
            ("site", self.site),
            ("area", self.area),
            ("line", self.line),
            ("cell", self.cell),
            ("asset", self.asset),
        )


def lab_uns_address(station_id: str) -> UnsAddress:
    """Map a simulated station to the lab's deterministic UNS asset path."""

    return UnsAddress(
        enterprise="portfolio",
        site="lab",
        area="textile-sorting",
        line=station_id,
        cell="edge-cell",
        asset="sorter-01",
    )


def _validate_segment(name: str, value: str) -> None:
    if not _SEGMENT_PATTERN.fullmatch(value):
        raise ValueError(
            f"{name} must use lowercase letters, numbers, or hyphens and cannot contain MQTT wildcards"
        )
