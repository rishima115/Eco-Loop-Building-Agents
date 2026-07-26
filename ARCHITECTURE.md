# 🏗️ Eco-Loop Building Agents: System Architecture Document

> **Honeywell Campus Hackathon Deliverable #4**  
> **Author**: Rishima Sharma  
> **Topic**: Physical AI Closed-Loop Autonomous HVAC Optimization Engine  
> **Core Architecture**: Physics Engine Bridge (EnergyPlus) + Model Context Protocol (MCP) + Open-Source Cognitive LLM Core  

---

## 1. Executive System Overview

**Eco-Loop Building Agents** is an autonomous smart building optimization framework that replaces rigid, static Building Management System (BMS) thermostat schedules with an intelligent, self-correcting closed-loop AI agent. 

The system pairs a physics-grounded **EnergyPlus building simulation engine** with an **Open-Source LLM cognitive brain** using the **Model Context Protocol (MCP)** standard.

---

## 2. Tool-Calling & MCP Protocol Architecture

The **Model Context Protocol (MCP)** acts as the standard communication bridge between the LLM cognitive engine and the building hardware/simulator.

### Registered BMS MCP Tools:
1. `get_building_telemetry()`: Exposes zone air temperature (°C), outdoor ambient weather (°C), relative humidity (%), active occupant count, electricity price ($/kWh), and grid carbon intensity ($kg CO_2 / kWh$).
2. `calculate_thermal_comfort(air_temp_c, rh_pct)`: Evaluates Fanger's 7-point **Predicted Mean Vote (PMV)** and **Predicted Percentage Dissatisfied (PPD)** according to ISO 7730 / ASHRAE Standard 55.
3. `apply_energy_conservation_measure(cooling_setpoint_c, heating_setpoint_c, strategy_name)`: Injects dynamic supervisory HVAC setpoint overrides back into the active EnergyPlus instance.
4. `parse_simulation_logs(max_history_steps)`: Scans runtime logs to detect thermal comfort violations or HVAC energy spikes.

---

## 3. Prompt Engineering & Latency Management Strategies

### Zero-Shot & Few-Shot Reasoning Strategies
The LLM agent utilizes domain-specific HVAC optimization directives:
- **Morning Pre-Cooling**: Pre-cools building thermal mass during off-peak morning hours (06:00 - 08:00) when grid carbon intensity and electricity prices are low.
- **Peak Demand & Carbon Shedding**: Floats setpoints to 24.5°C during high tariff ($0.28/kWh) and peak carbon grid periods (13:00 - 18:00).
- **Dynamic Thermal Reset**: Dynamically modulates cooling setpoints in response to ambient outdoor temperature to maintain PMV near neutral ($0.0 \le PMV \le +0.2$).
- **Night Purge / Unoccupied Setback**: Relaxes cooling setpoint to 26.5°C when occupancy drops to 0, eliminating nighttime HVAC energy draw.

---

## 4. Closed-Loop Self-Correction & Comfort Boundaries

To ensure the AI agent saves energy **without compromising human occupant comfort**, the pipeline includes an autonomous **Self-Correction Safety Loop**:

- **Thermal Comfort Constraint**: ASHRAE Class B standard requires $-0.5 \le PMV \le +0.5$ during occupied hours.
- **Automated Interception**: If an LLM setpoint directive threatens comfort ($PMV > +0.5$ or $PMV < -0.5$), the `SelfCorrectionEngine` automatically intercepts and clamps the setpoint back to a compliant temperature.

---

## 5. Quantitative Benchmark Results

Across a standard 24-hour / 96-timestep simulation horizon:

| Performance Metric | Fixed Baseline Schedule (21.0°C) | Eco-Loop AI Agent | Realized Savings |
| :--- | :--- | :--- | :--- |
| **Total Energy Draw (kWh)** | 27.64 kWh | 18.65 kWh | **⚡ 32.51% Reduction** |
| **Electricity Cost ($)** | $5.96 | $4.14 | **💰 30.57% Cost Savings** |
| **Carbon Emissions ($kg CO_2$)**| 14.57 kg | 10.17 kg | **🌱 30.22% Emissions Cut** |
| **PMV Comfort Compliance** | ISO Class B | ISO Class B | **✅ 100% Thermal Compliance** |
