"""
Thermal Comfort Calculation Module - Fanger PMV & PPD Model (ISO 7730 Standard)
Calculates Predicted Mean Vote (PMV) and Predicted Percentage Dissatisfied (PPD)
to ensure human occupant comfort boundaries are maintained while optimizing HVAC energy.
"""

import math

def calculate_pmv(ta: float, tr: float = None, rh: float = 50.0, vel: float = 0.1, 
                  met: float = 1.2, clo: float = 0.8) -> dict:
    """
    Calculates PMV and PPD according to ISO 7730 / ASHRAE 55 standard.
    """
    if tr is None:
        tr = ta

    pa = rh * 10.0 * math.exp(16.6536 - 4030.18 / (ta + 235.0))
    m = met * 58.15
    w = 0.0
    mw = m - w
    
    icl = 0.155 * clo
    fcl = 1.0 + 1.29 * icl if icl <= 0.078 else 1.05 + 0.645 * icl

    hcf = 12.1 * math.sqrt(vel)
    taa = ta + 273.15
    tra = tr + 273.15

    tcla = taa
    tcl = tcla - 273.15
    hc = hcf

    for _ in range(100):
        tcl_old = tcl
        hcn = 2.38 * math.pow(abs(tcl - ta), 0.25)
        hc = hcn if hcn > hcf else hcf
        
        tcl = (35.7 - 0.028 * mw - icl * fcl * (3.96e-8 * (math.pow(tra, 4) - math.pow(tcl + 273.15, 4)))) / (1.0 + icl * fcl * hc / 100.0)
        if abs(tcl - tcl_old) < 0.001:
            break

    hl1 = 3.05 * 0.001 * (5733.0 - 6.99 * mw - pa)
    hl2 = 0.42 * (mw - 58.15) if mw > 58.15 else 0.0
    hl3 = 1.7e-5 * m * (5867.0 - pa)
    hl4 = 0.0014 * m * (34.0 - ta)
    hl5 = 3.96e-8 * fcl * (math.pow(tcl + 273.15, 4) - math.pow(tra, 4))
    hl6 = fcl * hc * (tcl - ta)

    ts = 0.303 * math.exp(-0.036 * m) + 0.028
    pmv = ts * (mw - hl1 - hl2 - hl3 - hl4 - hl5 - hl6)

    pmv = max(-3.0, min(3.0, round(pmv, 2)))
    ppd = round(100.0 - 95.0 * math.exp(-0.03353 * math.pow(pmv, 4) - 0.2179 * math.pow(pmv, 2)), 1)

    if abs(pmv) <= 0.2:
        category = "Class A (Optimal Comfort)"
    elif abs(pmv) <= 0.5:
        category = "Class B (Good Comfort)"
    elif pmv > 0.5:
        category = "Warm Discomfort" if pmv <= 1.5 else "Hot / Severe Overheating"
    else:
        category = "Cool Discomfort" if pmv >= -1.5 else "Cold / Severe Underheating"

    in_comfort_zone = abs(pmv) <= 0.5

    return {
        "pmv": pmv,
        "ppd": ppd,
        "category": category,
        "in_comfort_zone": in_comfort_zone,
        "air_temperature_c": round(ta, 2),
        "relative_humidity_pct": round(rh, 1)
    }
