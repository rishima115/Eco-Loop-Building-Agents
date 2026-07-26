"""
Cognitive LLM Agent Orchestrator
"""

from typing import Dict, Any, List
from src.cognitive.prompts import SYSTEM_PROMPT_ECO_LOOP
from src.cognitive.self_correction import SelfCorrectionEngine

class CognitiveEcoLoopAgent:
    def __init__(self, mcp_server):
        self.mcp_server = mcp_server
        self.self_corrector = SelfCorrectionEngine()
        self.agent_log_history: List[Dict[str, Any]] = []

    def evaluate_and_control(self) -> Dict[str, Any]:
        telemetry_resp = self.mcp_server.direct_tool_call("get_building_telemetry")
        telemetry = telemetry_resp.get("telemetry", {})

        hour = telemetry.get("hour", 12.0)
        outdoor_temp = telemetry.get("outdoor_temp_c", 25.0)
        occupancy = telemetry.get("occupancy_count", 0)
        electricity_price = telemetry.get("electricity_price", 0.16)
        carbon_intensity = telemetry.get("grid_carbon_intensity", 0.45)

        strategy_name = "DYNAMIC_THERMAL_RESET"
        proposed_cooling_sp = 24.0
        proposed_heating_sp = 19.5
        thought_process = ""

        if occupancy == 0:
            strategy_name = "NIGHT_PURGE_UNOCCUPIED"
            proposed_cooling_sp = 26.5
            proposed_heating_sp = 18.0
            thought_process = f"Hour {hour:.1f}: Unoccupied setback mode ({proposed_cooling_sp}°C cooling / {proposed_heating_sp}°C heating)."
        elif electricity_price >= 0.25 or carbon_intensity >= 0.60:
            strategy_name = "PEAK_DEMAND_CARBON_SHED"
            proposed_cooling_sp = 24.5
            proposed_heating_sp = 19.0
            thought_process = f"Hour {hour:.1f}: Peak electricity rate (${electricity_price}/kWh). Floating cooling setpoint to {proposed_cooling_sp}°C."
        elif 6.0 <= hour < 8.0 and outdoor_temp < 24.0:
            strategy_name = "MORNING_PRE_COOLING"
            proposed_cooling_sp = 21.5
            proposed_heating_sp = 20.0
            thought_process = f"Hour {hour:.1f}: Pre-cooling thermal mass to {proposed_cooling_sp}°C during off-peak morning hours."
        else:
            strategy_name = "DYNAMIC_THERMAL_RESET"
            proposed_cooling_sp = round(max(22.5, min(24.5, 21.5 + 0.1 * (outdoor_temp - 22.0))), 1)
            proposed_heating_sp = 19.5
            thought_process = f"Hour {hour:.1f}: Dynamic cooling setpoint {proposed_cooling_sp}°C for optimal comfort."

        correction_result = self.self_corrector.evaluate_and_correct(
            telemetry=telemetry,
            proposed_cooling_sp=proposed_cooling_sp,
            proposed_heating_sp=proposed_heating_sp
        )

        final_cooling_sp = correction_result["final_cooling_setpoint_c"]
        final_heating_sp = correction_result["final_heating_setpoint_c"]

        mcp_action_resp = self.mcp_server.direct_tool_call(
            "apply_energy_conservation_measure",
            cooling_setpoint_c=final_cooling_sp,
            heating_setpoint_c=final_heating_sp,
            strategy_name=strategy_name
        )

        decision_log = {
            "timestep": telemetry.get("timestep", 0),
            "hour": hour,
            "outdoor_temp": outdoor_temp,
            "occupancy": occupancy,
            "strategy": strategy_name,
            "thought_process": thought_process,
            "initial_proposed_cooling_sp": proposed_cooling_sp,
            "final_applied_cooling_sp": final_cooling_sp,
            "final_applied_heating_sp": final_heating_sp,
            "self_correction_applied": correction_result["correction_applied"],
            "mcp_status": mcp_action_resp.get("status")
        }

        self.agent_log_history.append(decision_log)
        if len(self.agent_log_history) > 50:
            self.agent_log_history = self.agent_log_history[-50:]

        return decision_log
