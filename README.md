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
│   ├── baseline_building.idf        
│   └── eco_loop_optimized.idf       
├── src/
│   ├── simulation/
│   │   ├── energyplus_wrapper.py     
│   │   └── pmv_calculator.py        
│   ├── mcp/
│   │   ├── mcp_server.py            
│   │   └── tools.py                  
│   ├── cognitive/
│   │   ├── llm_agent.py             
│   │   ├── prompts.py                
│   │   └── self_correction.py       
│   └── closed_loop.py               
├── dashboard/
│   ├── index.html                   
│   ├── css/style.css                 
│   └── js/dashboard.js               
├── data/
│   ├── simulation_logs.json          
│   └── benchmark_results.json        
├── ARCHITECTURE.md                    
├── PRESENTATION.md                    
├── run_demo.py                       
├── requirements.txt                   
└── README.md                         
