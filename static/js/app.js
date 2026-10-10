/**
 * AstroCast Client Engine
 * Handles real-time tabular forecast updates, preset switches,
 * red-light night-vision mode, and the 30-second screen cutoff timer.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Elements
  const presetButtons = document.querySelectorAll('.preset-btn');
  const displayLocation = document.getElementById('display-location');
  const displayCoords = document.getElementById('display-coords');
  const displayRatingBadge = document.getElementById('display-rating-badge');
  const displayScore = document.getElementById('display-score');
  const displaySummary = document.getElementById('display-summary');
  const displaySeeing = document.getElementById('display-seeing');
  const displayTransparency = document.getElementById('display-transparency');
  const displayCloud = document.getElementById('display-cloud');
  const barSeeing = document.getElementById('bar-seeing');
  const barTransparency = document.getElementById('bar-transparency');
  const barCloud = document.getElementById('bar-cloud');

  const displayMoonIcon = document.getElementById('display-moon-icon');
  const displayMoonPhase = document.getElementById('display-moon-phase');
  const displayMoonIllum = document.getElementById('display-moon-illum');
  const displayMoonAge = document.getElementById('display-moon-age');
  const displayMoonAdvisory = document.getElementById('display-moon-advisory');

  const displayWindowTime = document.getElementById('display-window-time');
  const displayWindowDuration = document.getElementById('display-window-duration');
  const displayWindowDesc = document.getElementById('display-window-desc');

  const displayTemp = document.getElementById('display-temp');
  const displayDewGap = document.getElementById('display-dew-gap');
  const displayWind = document.getElementById('display-wind');
  const displaySource = document.getElementById('display-source');
  const targetsContainer = document.getElementById('targets-container');

  const redLightToggle = document.getElementById('red-light-toggle');
  const btnDarkTimer = document.getElementById('btn-dark-timer');
  const darkModal = document.getElementById('dark-modal');
  const countdownNum = document.getElementById('countdown-num');
  const btnCancelTimer = document.getElementById('btn-cancel-timer');
  const btnPrintPass = document.getElementById('btn-print-pass');

  let countdownInterval = null;

  // Preset Button Click Handlers
  presetButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      presetButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const lat = parseFloat(btn.dataset.lat);
      const lon = parseFloat(btn.dataset.lon);
      const name = btn.dataset.name;
      fetchForecast(lat, lon, name);
    });
  });

  // Fetch forecast from API
  async function fetchForecast(lat, lon, name) {
    try {
      const res = await fetch(`/api/forecast?lat=${lat}&lon=${lon}&location_name=${encodeURIComponent(name)}`);
      if (!res.ok) throw new Error('API network response error');
      const data = await res.json();
      renderDashboard(data);
    } catch (err) {
      console.warn('Network issue, rendering default state:', err);
    }
  }

  // Render Dashboard
  function renderDashboard(data) {
    const loc = data.location;
    const pred = data.prediction;
    const moon = data.moon;
    const w = data.weather;
    const win = data.window;
    const targets = data.targets;

    // Header & Meta
    displayLocation.textContent = loc.name;
    displayCoords.textContent = `${Math.abs(loc.lat).toFixed(2)}° ${loc.lat >= 0 ? 'N' : 'S'}, ${Math.abs(loc.lon).toFixed(2)}° ${loc.lon >= 0 ? 'E' : 'W'}`;

    // Score & Summary
    displayScore.textContent = Math.round(pred.overall_score);
    displaySummary.textContent = pred.summary;
    displayRatingBadge.textContent = pred.rating;
    displayRatingBadge.className = `rating-badge rating-${pred.badge_color}`;

    // Sub-metrics
    displaySeeing.textContent = `${Math.round(pred.seeing_score)}%`;
    barSeeing.style.width = `${Math.round(pred.seeing_score)}%`;

    displayTransparency.textContent = `${Math.round(pred.transparency_score)}%`;
    barTransparency.style.width = `${Math.round(pred.transparency_score)}%`;

    displayCloud.textContent = `${Math.round(w.cloud_cover_total)}%`;
    barCloud.style.width = `${Math.round(w.cloud_cover_total)}%`;

    // Moon
    displayMoonIcon.textContent = moon.icon;
    displayMoonPhase.textContent = moon.phase_name;
    displayMoonIllum.textContent = `${moon.illumination_percent}%`;
    displayMoonAge.textContent = `${moon.age_days} days`;
    displayMoonAdvisory.textContent = moon.advisory;

    // Window
    displayWindowTime.textContent = win.window;
    displayWindowDuration.textContent = `Window Duration: ${win.duration}`;
    displayWindowDesc.textContent = win.condition;

    // Weather Table
    displayTemp.textContent = `${w.temperature} °C`;
    displayDewGap.textContent = `${w.dew_point_depression} °C (Fog Risk: ${w.dew_point_depression < 2 ? 'High' : 'Low'})`;
    displayWind.textContent = `${w.wind_speed_10m} km/h`;
    displaySource.textContent = w.source.includes('Live') ? 'Open-Meteo Live' : 'Offline Autonomous Engine';

    // Targets
    targetsContainer.innerHTML = '';
    targets.forEach(t => {
      const card = document.createElement('div');
      card.className = 'target-card';
      card.innerHTML = `
        <span class="target-type">${t.type}</span>
        <h4 class="target-name">${t.name}</h4>
        <div class="target-constellation">Constellation: ${t.constellation} • Mag ${t.magnitude}</div>
        <p class="target-guide">${t.how_to_find}</p>
      `;
      targetsContainer.appendChild(card);
    });
  }

  // Red Light Mode Toggle (Field Night-Vision Preservation)
  redLightToggle.addEventListener('click', () => {
    document.body.classList.toggle('red-light-active');
    const isActive = document.body.classList.contains('red-light-active');
    redLightToggle.style.background = isActive ? 'rgba(239, 68, 68, 0.4)' : '';
  });

  // 30-Second Dark Adaptation Timer
  btnDarkTimer.addEventListener('click', () => {
    let timeLeft = 30;
    countdownNum.textContent = timeLeft;
    darkModal.classList.remove('hidden');

    clearInterval(countdownInterval);
    countdownInterval = setInterval(() => {
      timeLeft--;
      countdownNum.textContent = timeLeft;
      if (timeLeft <= 0) {
        clearInterval(countdownInterval);
        countdownNum.textContent = '🌑';
        countdownNum.style.fontSize = '3.5rem';
        const cardP = darkModal.querySelector('.dark-modal-card p');
        cardP.textContent = 'Device locked. Step outside into the night and let your eyes adjust to the stars.';
      }
    }, 1000);
  });

  btnCancelTimer.addEventListener('click', () => {
    clearInterval(countdownInterval);
    darkModal.classList.add('hidden');
    countdownNum.style.fontSize = '2.2rem';
  });

  // Save Offline Pocket Pass (Print / Export)
  btnPrintPass.addEventListener('click', () => {
    window.print();
  });

  // Initial load
  const initialBtn = document.querySelector('.preset-btn.active');
  if (initialBtn) {
    fetchForecast(
      parseFloat(initialBtn.dataset.lat),
      parseFloat(initialBtn.dataset.lon),
      initialBtn.dataset.name
    );
  }
});
