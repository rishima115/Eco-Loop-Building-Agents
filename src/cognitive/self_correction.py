"""
Self-Correction Loop & Diagnostic Module
"""

from typing import Dict, Any

class SelfCorrectionEngine:
    def __init__(self, min_cooling_sp: float = 21.0, max_cooling_sp: float = 25.5):
        self.min_cooling_sp = min_cooling_sp
        self.max_cooling_sp = max_cooling_sp
        self.correction_count = 0

    def evaluate_and_correct(self, telemetry: Dict[str, Any], proposed_cooling_sp: float, proposed_heating_sp: float) -> Dict[str, Any]:
        pmv = telemetry.get("pmv", 0.0)
        occupancy = telemetry.get("occupancy_count", 0)

        corrected_cooling = proposed_cooling_sp
        corrected_heating = proposed_heating_sp
        correction_applied = False
        reason = "Setpoints within optimal operating bounds."

        if occupancy > 0:
            if pmv > 0.5 or proposed_cooling_sp > 25.0:
                corrected_cooling = min(proposed_cooling_sp, 24.0)
                correction_applied = True
                self.correction_count += 1
                reason = f"PMV ({pmv}) upper threshold intervention. Corrected cooling setpoint to {corrected_cooling}°C."
            elif pmv < -0.5 or proposed_cooling_sp < 21.0:
                corrected_cooling = max(proposed_cooling_sp, 22.0)
                correction_applied = True
                self.correction_count += 1
                reason = f"PMV ({pmv}) lower threshold intervention. Corrected cooling setpoint to {corrected_cooling}°C."

        return {
            "correction_applied": correction_applied,
            "reason": reason,
            "final_cooling_setpoint_c": round(corrected_cooling, 1),
            "final_heating_setpoint_c": round(corrected_heating, 1)
        }
