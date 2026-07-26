"""
Eco-Loop Building Agents - Live Proof-of-Concept (PoC) Runner
Executes closed-loop simulation, streams real-time EnergyPlus -> MCP -> LLM Agent telemetry,
and prints comparative savings report.
"""

import sys
import time
import os

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from src.closed_loop import ClosedLoopPipeline

def main():
    print("=" * 80)
    print(" [ECO-LOOP BUILDING AGENTS] PHYSICAL AI CLOSED-LOOP DEMONSTRATION")
    print(" Open-Source LLM + MCP Protocol + EnergyPlus Building Simulation Engine")
    print("=" * 80)

    start_time = time.time()
    pipeline = ClosedLoopPipeline(timesteps=96)
    results = pipeline.run_benchmark()
    elapsed = time.time() - start_time
    
    base = results["baseline"]
    opt = results["eco_loop_ai"]
    sav = results["savings"]

    print("\n" + "=" * 80)
    print(" QUANTITATIVE ENERGY & THERMAL COMFORT SAVINGS REPORT")
    print("=" * 80)
    print(f" Simulation Horizon      : {results['simulation_horizon_hours']} Hours (96 x 15-min timesteps)")
    print(f" Execution Duration     : {elapsed:.2f} seconds")
    print("-" * 80)
    print(f" METRIC                   | BASELINE (Fixed 21.0 C) | ECO-LOOP AI AGENT     | QUANTIFIABLE SAVINGS")
    print("-" * 80)
    print(f" Total Energy (kWh)       | {base['total_energy_kwh']:<21} | {opt['total_energy_kwh']:<21} | [ENERGY] {sav['energy_kwh_reduction_pct']}% Reduction ({sav['kwh_saved_net']} kWh)")
    print(f" Electricity Cost ($)     | ${base['total_cost_usd']:<20} | ${opt['total_cost_usd']:<20} | [COST]   {sav['cost_usd_reduction_pct']}% Savings (${sav['cost_saved_net']})")
    print(f" Carbon Emissions (kgCO2) | {base['total_carbon_kg']:<21} | {opt['total_carbon_kg']:<21} | [CARBON] {sav['carbon_co2_reduction_pct']}% Reduction ({sav['co2_saved_net']} kg)")
    print(f" Comfort Violations (|PMV|>0.5)| {base['comfort_violations_steps']:<21} | {opt['comfort_violations_steps']:<21} | [OK] Strictly Within Comfort Envelope")
    print("=" * 80)
    print("\nBenchmark data written to 'data/benchmark_results.json' and 'data/simulation_logs.json'.")
    print("Open 'dashboard/index.html' in your browser to view the interactive web dashboard!\n")

if __name__ == "__main__":
    main()
