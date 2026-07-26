"""
Model Context Protocol (MCP) Building Management System (BMS) Tools
Defines standardized tool interfaces exposed to the Cognitive LLM Agent.
"""

from typing import Dict, Any, List
from src.simulation.pmv_calculator import calculate_pmv

MCP_TOOL_MANIFEST = [
    {
        "name": "get_building_telemetry",
        "description": "Reads real-time building sensor data from EnergyPlus simulation.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "calculate_thermal_comfort",
        "description": "Evaluates Fanger PMV & PPD thermal comfort indices.",
        "parameters": {
            "type": "object",
            "properties": {
                "air_temperature_c": {"type": "number"},
                "relative_humidity_pct": {"type": "number"}
            },
            "required": ["air_temperature_c"]
        }
    },
    {
        "name": "apply_energy_conservation_measure",
        "description": "Injects forward HVAC setpoint overrides back into active EnergyPlus engine instance.",
        "parameters": {
            "type": "object",
            "properties": {
                "cooling_setpoint_c": {"type": "number"},
                "heating_setpoint_c": {"type": "number"},
                "strategy_name": {"type": "string"}
            },
            "required": ["cooling_setpoint_c", "heating_setpoint_c", "strategy_name"]
        }
    },
    {
        "name": "parse_simulation_logs",
        "description": "Scans runtime simulation logs to detect thermal comfort violations.",
        "parameters": {"type": "object", "properties": {"max_history_steps": {"type": "integer"}}, "required": []}
    }
]

class BMSToolHandler:
    def __init__(self, simulation_engine):
        self.engine = simulation_engine

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name == "get_building_telemetry":
            return self._get_telemetry()
        elif tool_name == "calculate_thermal_comfort":
            return self._calculate_comfort(arguments)
        elif tool_name == "apply_energy_conservation_measure":
            return self._apply_ecm(arguments)
        elif tool_name == "parse_simulation_logs":
            return self._parse_logs(arguments)
        else:
            return {"status": "error", "message": f"Unknown MCP tool: {tool_name}"}

    def _get_telemetry(self) -> Dict[str, Any]:
        latest = self.engine.telemetry_history[-1] if self.engine.telemetry_history else self.engine.step()
        return {"status": "success", "telemetry": latest}

    def _calculate_comfort(self, args: Dict[str, Any]) -> Dict[str, Any]:
        ta = args.get("air_temperature_c", 23.0)
        rh = args.get("relative_humidity_pct", 50.0)
        return {"status": "success", "pmv_analysis": calculate_pmv(ta=ta, rh=rh)}

    def _apply_ecm(self, args: Dict[str, Any]) -> Dict[str, Any]:
        cooling_sp = args.get("cooling_setpoint_c", 24.0)
        heating_sp = args.get("heating_setpoint_c", 19.5)
        strategy = args.get("strategy_name", "DYNAMIC_RESET")
        self.engine.set_hvac_overrides(cooling_sp, heating_sp)
        return {
            "status": "success",
            "action_applied": {
                "strategy": strategy,
                "applied_cooling_setpoint": self.engine.cooling_setpoint,
                "applied_heating_setpoint": self.engine.heating_setpoint
            }
        }

    def _parse_logs(self, args: Dict[str, Any]) -> Dict[str, Any]:
        steps = args.get("max_history_steps", 10)
        history = self.engine.telemetry_history[-steps:]
        violations = [step for step in history if not step["in_comfort_zone"]]
        return {
            "status": "success",
            "analyzed_steps": len(history),
            "comfort_violations_found": len(violations),
            "recent_average_pmv": round(sum(s["pmv"] for s in history) / max(1, len(history)), 2)
        }
