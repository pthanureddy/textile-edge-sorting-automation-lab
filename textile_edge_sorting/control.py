from __future__ import annotations

from textile_edge_sorting.models import ActuatorCommand, ClassificationResult, TextileRoute


GATE_BY_ROUTE = {
    TextileRoute.REUSE: "A",
    TextileRoute.COTTON_RECYCLING: "B",
    TextileRoute.SYNTHETIC_RECYCLING: "C",
    TextileRoute.MANUAL_INSPECTION: "REJECT",
}


def build_actuator_command(result: ClassificationResult) -> ActuatorCommand:
    reject = result.route == TextileRoute.MANUAL_INSPECTION
    speed = 0.25 if reject else 0.42 if result.confidence >= 0.7 else 0.32
    return ActuatorCommand(
        diverter_gate=GATE_BY_ROUTE[result.route],
        conveyor_speed_mps=speed,
        reject_enabled=reject,
        settle_time_ms=350 if reject else 180,
    )
