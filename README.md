# 🌿 Eco-Loop Building Agents: Autonomous Physical AI Closed-Loop HVAC Control Pipeline

> **Honeywell Campus Hackathon Entry**  
> **Author**: Rishima Sharma  
> **Topic**: Autonomous Smart Building Operations with Open-Source LLMs, Model Context Protocol (MCP), and EnergyPlus Physics Engine  

---

## 📌 Problem Background & Solution Concept

Buildings consume approximately **40% of global energy** and remain a primary driver of carbon emissions. Traditional Building Management Systems (BMS) rely on rigid, rule-based HVAC schedules that fail to adapt to weather, occupancy, grid carbon intensity, or electricity tariffs.

**Eco-Loop Building Agents** pairs physics-based building energy simulation engines (**EnergyPlus**) with an **Open-Source LLM cognitive brain** using the **Model Context Protocol (MCP)** standard. The system ingests continuous sensor metrics, evaluates Fanger PMV thermal comfort indices (ISO 7730 standard), and dynamically injects forward setpoint overrides back into EnergyPlus to achieve **quantifiable energy, cost, and carbon savings**.

---

## 🚀 Quantifiable Savings Realized

Across an extended simulation horizon (24 hours / 96 x 15-minute timesteps):

- **⚡ Net Energy Savings**: **32.5% Reduction** in total kWh consumed.
- **💰 Electricity Cost Reduction**: **30.6% Cost Savings** under Time-of-Use tariffs.
- **🌱 Carbon Emissions Cut**: **30.2% Reduction** in total $kg CO_2$ emissions.
- **🧘 Occupant Thermal Comfort**: **100% Compliance** with ISO 7730 Class B bounds ($-0.5 \le PMV \le +0.5$).

---

## 🛠️ Project Structure & Deliverables

```
Eco-Loop-Building-Agents/
├── models/
│   ├── baseline_building.idf         # Baseline standard schedule EnergyPlus model
│   └── eco_loop_optimized.idf       # AI Agent dynamic setpoint EnergyPlus model
├── src/
│   ├── simulation/
│   │   ├── energyplus_wrapper.py     # Physics simulation engine bridge & weather profile
│   │   └── pmv_calculator.py         # ISO 7730 Fanger PMV & PPD thermal comfort index
│   ├── mcp/
│   │   ├── mcp_server.py             # Model Context Protocol JSON-RPC server
│   │   └── tools.py                  # BMS tools (telemetry, PMV, setpoint override, logs)
│   ├── cognitive/
│   │   ├── llm_agent.py              # Cognitive Open-Source LLM Agent Orchestrator
│   │   ├── prompts.py                # System prompts, zero/few-shot ECM strategies
│   │   └── self_correction.py        # Thermal comfort safety guardrail & self-correction loop
│   └── closed_loop.py               # Unified closed-loop execution controller
├── dashboard/
│   ├── index.html                    # Real-time quantitative web dashboard
│   ├── css/style.css                 # Sleek dark-mode BMS glassmorphism styling
│   └── js/dashboard.js               # Dynamic Chart.js visualizations
├── data/
│   ├── simulation_logs.json          # Live telemetry stream log file
│   └── benchmark_results.json        # Comparative benchmark report
├── ARCHITECTURE.md                    # Deliverable #4: System Architecture Document
├── PRESENTATION.md                    # Deliverable #6: Presentation Slide Template Deck
├── run_demo.py                        # Executable CLI PoC runner script
├── requirements.txt                   # Project dependencies
└── README.md                          # Repository Documentation
```

---

## 💻 Quick Start & Running the Demo

### 1. Run the Closed-Loop Proof-of-Concept (PoC) Simulation
Run the unified Python pipeline from your terminal:

```bash
python run_demo.py
```

### 2. View the Quantitative Web Dashboard
Open `dashboard/index.html` in your web browser or start a local server:

```bash
python -m http.server 8000
```
Then navigate to `http://localhost:8000/dashboard/`.
