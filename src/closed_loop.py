"""
Unified Closed-Loop Simulation Controller & Benchmark Evaluator
"""

import json
import os
import sys
from typing import Dict, Any

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from src.simulation.energyplus_wrapper import EnergyPlusEngine
from src.mcp.mcp_server import MCPServer
from src.cognitive.llm_agent import CognitiveEcoLoopAgent

class ClosedLoopPipeline:
    def __init__(self, timesteps: int = 96):
        self.timesteps = timesteps

    def run_benchmark(self) -> Dict[str, Any]:
        print("[1/2] Initializing Baseline Simulation (Fixed Setpoints: 21.0 C)...")
        baseline_engine = EnergyPlusEngine(is_baseline=True)
        for _ in range(self.timesteps):
            baseline_engine.step()

        print("[2/2] Initializing Eco-Loop Autonomous AI Agent Pipeline...")
        optimized_engine = EnergyPlusEngine(is_baseline=False)
        mcp_server = MCPServer(optimized_engine)
        agent = CognitiveEcoLoopAgent(mcp_server)

        ai_logs = []
        for _ in range(self.timesteps):
            optimized_engine.step()
            decision = agent.evaluate_and_control()
            ai_logs.append(decision)

        base_kwh = baseline_engine.cumulative_energy_kwh
        opt_kwh = optimized_engine.cumulative_energy_kwh
        kwh_savings_pct = round(((base_kwh - opt_kwh) / base_kwh) * 100.0, 2)

        base_cost = baseline_engine.cumulative_cost_usd
        opt_cost = optimized_engine.cumulative_cost_usd
        cost_savings_pct = round(((base_cost - opt_cost) / base_cost) * 100.0, 2)

        base_co2 = baseline_engine.cumulative_carbon_kg
        opt_co2 = optimized_engine.cumulative_carbon_kg
        co2_savings_pct = round(((base_co2 - opt_co2) / base_co2) * 100.0, 2)

        results = {
            "simulation_horizon_hours": round(self.timesteps / 4.0, 1),
            "baseline": {
                "total_energy_kwh": round(base_kwh, 2),
                "total_cost_usd": round(base_cost, 2),
                "total_carbon_kg": round(base_co2, 2),
                "comfort_violations_steps": baseline_engine.comfort_violation_steps
            },
            "eco_loop_ai": {
                "total_energy_kwh": round(opt_kwh, 2),
                "total_cost_usd": round(opt_cost, 2),
                "total_carbon_kg": round(opt_co2, 2),
                "comfort_violations_steps": optimized_engine.comfort_violation_steps
            },
            "savings": {
                "energy_kwh_reduction_pct": kwh_savings_pct,
                "cost_usd_reduction_pct": cost_savings_pct,
                "carbon_co2_reduction_pct": co2_savings_pct,
                "kwh_saved_net": round(base_kwh - opt_kwh, 2),
                "cost_saved_net": round(base_cost - opt_cost, 2),
                "co2_saved_net": round(base_co2 - opt_co2, 2)
            },
            "baseline_telemetry": baseline_engine.telemetry_history,
            "eco_loop_telemetry": optimized_engine.telemetry_history,
            "agent_decisions": ai_logs
        }

        os.makedirs("data", exist_ok=True)
        with open("data/benchmark_results.json", "w") as f:
            json.dump(results, f, indent=2)
            
        with open("data/simulation_logs.json", "w") as f:
            json.dump(ai_logs, f, indent=2)

        return results

if __name__ == "__main__":
    pipeline = ClosedLoopPipeline(timesteps=96)
    res = pipeline.run_benchmark()
    print(f"\n[OK] Simulation Complete! Net Energy Savings: {res['savings']['energy_kwh_reduction_pct']}%")
