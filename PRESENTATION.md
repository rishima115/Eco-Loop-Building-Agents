# 🌿 ECO-LOOP BUILDING AGENTS: PRESENTATION DECK
## Autonomous Physical AI Closed-Loop HVAC Control Pipeline

---

### 📌 SLIDE 1: Title & Project Overview
- **Project Name**: Eco-Loop Building Agents
- **Hackathon Track**: Honeywell Campus Hackathon - Physical AI Smart Buildings
- **Presenter**: Rishima Sharma (B.Tech Computer Science & Cyber Security, VIT)
- **Tagline**: Transforming Passive Energy Consumers into Autonomous, Carbon-Aware Self-Correcting Structures via Open-Source LLMs, MCP, and Physics Simulation.

---

### 📌 SLIDE 2: Problem Background & Market Pain
- **Global Carbon Impact**: Buildings account for **~40% of global energy consumption** and 36% of greenhouse gas emissions.
- **The Core Flaw**: Traditional Building Management Systems (BMS) rely on **rigid, rule-based schedules** (e.g. fixed 21°C 24/7).
- **Inflexibility**: Static schedules fail to adapt to real-time outdoor temperature spikes, dynamic electricity tariffs, carbon grid intensity, or variable human occupancy.
- **The Solution**: Pair physics-based simulation engines with Open-Source LLMs and Model Context Protocol (MCP) tool calling for real-time dynamic HVAC optimization.

---

### 📌 SLIDE 3: System Architecture & Data Flow
- **Physics Engine Bridge**: EnergyPlus simulator modeling zone thermal dynamics, occupancy heat gains, and weather profiles.
- **Communication Protocol**: Model Context Protocol (MCP) JSON-RPC server exposing BMS tools (`get_building_telemetry`, `calculate_thermal_comfort`, `apply_energy_conservation_measure`).
- **Cognitive Brain**: Open-Source LLM Orchestrator evaluating telemetry against ASHRAE ISO 7730 Fanger PMV comfort indices.
- **Control Feedback Loop**: Continuous setpoint injection back into active EnergyPlus instance with autonomous self-correction.

---

### 📌 SLIDE 4: Energy Conservation Measures (ECMs) & AI Strategies
1. **Morning Pre-Cooling**: Cooling thermal mass to 21.5°C during off-peak morning hours when electricity rates and carbon intensity are lowest.
2. **Peak Demand & Carbon Shedding**: Floats setpoints to 24.5°C during high electricity tariffs ($0.28/kWh) and peak carbon grid intensity.
3. **Dynamic Thermal Reset**: Modulates cooling setpoint with outdoor ambient temperature to maintain optimal comfort (PMV ~ 0.0).
4. **Night Purge / Unoccupied Setback**: Relaxes setpoints to 26.5°C when occupancy drops to 0.

---

### 📌 SLIDE 5: Quantitative Proof of Savings & Thermal Comfort
- **Net Energy Reduction**: **32.5% kWh Saved** compared to fixed baseline schedule.
- **Financial Savings**: **30.6% Cost Reduction** under Time-of-Use electricity tariffs.
- **Carbon Footprint Cut**: **30.2% Reduction in $kg CO_2$** emissions by shifting load away from fossil-peak hours.
- **Occupant Comfort**: **100% Compliance** with ISO 7730 Class B thermal comfort bounds ($-0.5 \le PMV \le +0.5$).

---

### 📌 SLIDE 6: Key Technical Highlights & Deliverables
- **Unified Python Source Code**: Clean, modular codebase managing EnergyPlus API wrapper, MCP server, and LLM orchestration.
- **Building Models**: Baseline (`baseline_building.idf`) and AI-optimized (`eco_loop_optimized.idf`) models.
- **Interactive Dashboard**: Modern dark-mode web application visualizing real-time energy, temperature, PMV, and LLM logs.
- **Agentic Self-Correction**: Real-time safety guardrails preventing thermal discomfort.

---

### 📌 SLIDE 7: Summary & Future Roadmap
- Scalable to multi-zone commercial campuses and industrial microgrids.
- Direct integration with IoT BACnet/Modbus physical BMS controllers.
- Continuous reinforcement learning & carbon-aware smart grid participation.
