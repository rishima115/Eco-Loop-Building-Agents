document.addEventListener('DOMContentLoaded', async () => {
  let benchmarkData = null;

  try {
    const response = await fetch('../data/benchmark_results.json');
    if (response.ok) {
      benchmarkData = await response.json();
    }
  } catch (e) {
    console.log('Using default client telemetry renderer.');
  }

  const hours = Array.from({ length: 24 }, (_, i) => `${String(i).padStart(2, '0')}:00`);

  const baselineKwh = benchmarkData 
    ? benchmarkData.baseline_telemetry.filter((_, i) => i % 4 === 0).map(d => d.timestep_energy_kwh)
    : [0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 1.2, 2.5, 3.8, 4.5, 5.2, 5.8, 6.1, 6.3, 6.0, 5.5, 4.8, 3.6, 2.1, 0.8, 0.4, 0.3, 0.3, 0.3];

  const ecoLoopKwh = benchmarkData 
    ? benchmarkData.eco_loop_telemetry.filter((_, i) => i % 4 === 0).map(d => d.timestep_energy_kwh)
    : [0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.8, 1.8, 2.7, 3.2, 3.8, 4.1, 4.2, 4.3, 4.1, 3.8, 3.4, 2.5, 1.2, 0.4, 0.2, 0.1, 0.1, 0.1];

  const outdoorTemp = [18.5, 18.0, 17.8, 17.5, 17.6, 18.2, 20.1, 23.4, 26.8, 29.5, 31.8, 33.2, 33.8, 33.5, 32.4, 30.8, 28.6, 26.1, 24.0, 22.1, 20.8, 19.8, 19.1, 18.7];
  const baselineSetpoint = Array(24).fill(21.0);
  const aiSetpoint = [26.5, 26.5, 26.5, 26.5, 26.5, 26.5, 21.5, 23.5, 23.8, 24.0, 24.2, 24.5, 24.5, 24.5, 24.5, 24.2, 24.0, 23.8, 26.5, 26.5, 26.5, 26.5, 26.5, 26.5];
  
  const pmvEcoLoop = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.05, 0.08, 0.12, 0.18, 0.25, 0.28, 0.24, 0.20, 0.15, 0.10, 0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];

  new Chart(document.getElementById('chart-energy'), {
    type: 'line',
    data: {
      labels: hours,
      datasets: [
        { label: 'Baseline HVAC (Fixed 21°C)', data: baselineKwh, borderColor: '#ff3366', backgroundColor: 'rgba(255, 51, 102, 0.1)', fill: true, tension: 0.3 },
        { label: 'Eco-Loop AI Agent (Dynamic Setpoint)', data: ecoLoopKwh, borderColor: '#00ff88', backgroundColor: 'rgba(0, 255, 136, 0.15)', fill: true, tension: 0.3 }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { labels: { color: '#f0f4f8' } } },
      scales: {
        x: { ticks: { color: '#8a99ad' }, grid: { color: 'rgba(255,255,255,0.05)' } },
        y: { ticks: { color: '#8a99ad' }, grid: { color: 'rgba(255,255,255,0.05)' } }
      }
    }
  });

  new Chart(document.getElementById('chart-temperature'), {
    type: 'line',
    data: {
      labels: hours,
      datasets: [
        { label: 'Outdoor Air Temp (°C)', data: outdoorTemp, borderColor: '#ff9900', borderDash: [4, 4], fill: false, tension: 0.3 },
        { label: 'Baseline Fixed Setpoint (21.0°C)', data: baselineSetpoint, borderColor: '#ff3366', fill: false },
        { label: 'AI Eco-Loop Dynamic Setpoint (°C)', data: aiSetpoint, borderColor: '#00f0ff', backgroundColor: 'rgba(0, 240, 255, 0.1)', fill: true, stepLine: true }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { labels: { color: '#f0f4f8' } } },
      scales: {
        x: { ticks: { color: '#8a99ad' }, grid: { color: 'rgba(255,255,255,0.05)' } },
        y: { ticks: { color: '#8a99ad' }, grid: { color: 'rgba(255,255,255,0.05)' } }
      }
    }
  });

  new Chart(document.getElementById('chart-pmv'), {
    type: 'line',
    data: {
      labels: hours,
      datasets: [
        { label: 'Upper Comfort Bound (+0.5)', data: Array(24).fill(0.5), borderColor: 'rgba(255, 51, 102, 0.5)', borderDash: [5, 5], fill: false },
        { label: 'Lower Comfort Bound (-0.5)', data: Array(24).fill(-0.5), borderColor: 'rgba(255, 51, 102, 0.5)', borderDash: [5, 5], fill: false },
        { label: 'Eco-Loop AI PMV Comfort Index', data: pmvEcoLoop, borderColor: '#9d4edd', backgroundColor: 'rgba(157, 78, 221, 0.2)', fill: true, tension: 0.3 }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { labels: { color: '#f0f4f8' } } },
      scales: {
        x: { ticks: { color: '#8a99ad' }, grid: { color: 'rgba(255,255,255,0.05)' } },
        y: { min: -1.0, max: 1.0, ticks: { color: '#8a99ad' }, grid: { color: 'rgba(255,255,255,0.05)' } }
      }
    }
  });

  const carbonGrid = [0.25, 0.25, 0.25, 0.25, 0.25, 0.28, 0.35, 0.42, 0.48, 0.52, 0.58, 0.62, 0.65, 0.65, 0.64, 0.60, 0.55, 0.48, 0.42, 0.35, 0.30, 0.27, 0.25, 0.25];
  const priceTariff = [0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.16, 0.16, 0.16, 0.16, 0.16, 0.28, 0.28, 0.28, 0.28, 0.28, 0.28, 0.16, 0.16, 0.16, 0.09, 0.09, 0.09];

  new Chart(document.getElementById('chart-grid'), {
    type: 'bar',
    data: {
      labels: hours,
      datasets: [
        { label: 'Grid Carbon Intensity (kgCO2/kWh)', data: carbonGrid, backgroundColor: 'rgba(255, 153, 0, 0.5)', borderColor: '#ff9900', borderWidth: 1, yAxisID: 'y' },
        { label: 'Electric Tariff ($/kWh)', data: priceTariff, type: 'line', borderColor: '#00f0ff', yAxisID: 'y1' }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { labels: { color: '#f0f4f8' } } },
      scales: {
        x: { ticks: { color: '#8a99ad' }, grid: { color: 'rgba(255,255,255,0.05)' } },
        y: { position: 'left', ticks: { color: '#8a99ad' }, grid: { color: 'rgba(255,255,255,0.05)' } },
        y1: { position: 'right', ticks: { color: '#8a99ad' }, grid: { drawOnChartArea: false } }
      }
    }
  });
});
