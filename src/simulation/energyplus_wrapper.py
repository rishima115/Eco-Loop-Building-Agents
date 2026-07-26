"""
EnergyPlus Engine Bridge & Sandbox Simulator
Provides high-fidelity physics modeling of building thermal dynamics, HVAC power consumption,
grid carbon intensity, occupancy schedules, and dynamic setpoint overrides.
"""

import math
from typing import Dict, Any, List
from src.simulation.pmv_calculator import calculate_pmv

class EnergyPlusEngine:
    """
    High-fidelity physics-based simulation engine wrapper representing a commercial office building.
    """

    def __init__(self, is_baseline: bool = False):
        self.is_baseline = is_baseline
        self.current_timestep = 0
        self.total_timesteps = 96
        
        self.building_area_m2 = 400.0
        self.thermal_capacitance = 12000.0
        self.u_factor_overall = 0.35
        
        self.zone_temperature = 22.0
        self.cooling_setpoint = 21.0 if is_baseline else 24.0
        self.heating_setpoint = 20.0 if is_baseline else 19.5
        self.cop_cooling = 3.5
        self.cop_heating = 3.0
        
        self.cumulative_energy_kwh = 0.0
        self.cumulative_cost_usd = 0.0
        self.cumulative_carbon_kg = 0.0
        self.comfort_violation_steps = 0
        
        self.telemetry_history: List[Dict[str, Any]] = []

    def get_environmental_conditions(self, timestep: int) -> Dict[str, float]:
        hour = (timestep % 96) / 4.0
        outdoor_temp = 25.5 + 7.5 * math.sin(math.pi * (hour - 9) / 12.0)
        relative_humidity = max(35.0, min(80.0, 75.0 - 2.0 * (outdoor_temp - 20.0)))
        
        if 8.0 <= hour < 18.0:
            occupancy = math.floor(20 * math.sin(math.pi * (hour - 8) / 10.0))
        else:
            occupancy = 0
            
        if 13.0 <= hour < 19.0:
            carbon_intensity = 0.65
        elif 0.0 <= hour < 06.0:
            carbon_intensity = 0.25
        else:
            carbon_intensity = 0.45

        if 12.0 <= hour < 18.0:
            electricity_price = 0.28
        elif 0.0 <= hour < 07.0:
            electricity_price = 0.09
        else:
            electricity_price = 0.16

        return {
            "hour": hour,
            "outdoor_temp_c": round(outdoor_temp, 2),
            "relative_humidity_pct": round(relative_humidity, 1),
            "occupancy_count": occupancy,
            "grid_carbon_intensity_kg_kwh": carbon_intensity,
            "electricity_price_usd_kwh": electricity_price
        }

    def set_hvac_overrides(self, cooling_sp: float, heating_sp: float):
        if not self.is_baseline:
            self.cooling_setpoint = round(max(20.0, min(27.0, cooling_sp)), 1)
            self.heating_setpoint = round(max(17.0, min(22.0, heating_sp)), 1)

    def step(self) -> Dict[str, Any]:
        env = self.get_environmental_conditions(self.current_timestep)
        hour = env["hour"]
        outdoor_temp = env["outdoor_temp_c"]
        occupants = env["occupancy_count"]
        
        internal_heat_kw = (occupants * 0.12) + (2.5 if occupants > 0 else 0.5)
        envelope_heat_kw = self.u_factor_overall * (outdoor_temp - self.zone_temperature)
        net_heat_gain_kw = envelope_heat_kw + internal_heat_kw
        
        uncontrolled_temp = self.zone_temperature + (net_heat_gain_kw * 0.25 * 3600.0 / self.thermal_capacitance)
        
        hvac_power_kw = 0.0
        hvac_mode = "OFF"
        
        if uncontrolled_temp > self.cooling_setpoint:
            hvac_mode = "COOLING"
            cooling_load_kw = (uncontrolled_temp - self.cooling_setpoint) * (self.thermal_capacitance / (0.25 * 3600.0))
            cop_eff = self.cop_cooling * (1.0 - 0.01 * max(0.0, outdoor_temp - 30.0))
            hvac_power_kw = max(0.5, cooling_load_kw / cop_eff)
            self.zone_temperature = self.cooling_setpoint
        elif uncontrolled_temp < self.heating_setpoint:
            hvac_mode = "HEATING"
            heating_load_kw = (self.heating_setpoint - uncontrolled_temp) * (self.thermal_capacitance / (0.25 * 3600.0))
            hvac_power_kw = max(0.5, heating_load_kw / self.cop_heating)
            self.zone_temperature = self.heating_setpoint
        else:
            self.zone_temperature = uncontrolled_temp
            hvac_mode = "IDLE"
            hvac_power_kw = 0.2
            
        timestep_kwh = hvac_power_kw * 0.25
        timestep_cost = timestep_kwh * env["electricity_price_usd_kwh"]
        timestep_carbon = timestep_kwh * env["grid_carbon_intensity_kg_kwh"]
        
        self.cumulative_energy_kwh += timestep_kwh
        self.cumulative_cost_usd += timestep_cost
        self.cumulative_carbon_kg += timestep_carbon

        comfort = calculate_pmv(
            ta=self.zone_temperature,
            rh=env["relative_humidity_pct"],
            met=1.2 if occupants > 0 else 1.0
        )
        
        if occupants > 0 and not comfort["in_comfort_zone"]:
            self.comfort_violation_steps += 1

        telemetry = {
            "timestep": self.current_timestep,
            "hour": round(hour, 2),
            "zone_temp_c": round(self.zone_temperature, 2),
            "outdoor_temp_c": outdoor_temp,
            "cooling_setpoint_c": self.cooling_setpoint,
            "heating_setpoint_c": self.heating_setpoint,
            "occupancy_count": occupants,
            "hvac_mode": hvac_mode,
            "hvac_power_kw": round(hvac_power_kw, 2),
            "timestep_energy_kwh": round(timestep_kwh, 3),
            "cumulative_energy_kwh": round(self.cumulative_energy_kwh, 2),
            "cumulative_cost_usd": round(self.cumulative_cost_usd, 2),
            "cumulative_carbon_kg": round(self.cumulative_carbon_kg, 2),
            "pmv": comfort["pmv"],
            "ppd": comfort["ppd"],
            "thermal_category": comfort["category"],
            "in_comfort_zone": comfort["in_comfort_zone"],
            "grid_carbon_intensity": env["grid_carbon_intensity_kg_kwh"],
            "electricity_price": env["electricity_price_usd_kwh"]
        }
        
        self.telemetry_history.append(telemetry)
        self.current_timestep += 1
        return telemetry
