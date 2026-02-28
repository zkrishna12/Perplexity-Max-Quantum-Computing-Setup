/* app.js — Quantum Lab Dashboard */

// ============ DATA ============
const EXPERIMENTS = [
  { id: 1, name: 'Quantum Coin Flip', qubits: '1', gates: ['H'], level: 'Beginner', desc: 'Superposition — qubit is 0 AND 1 at the same time', detail: 'Uses the Hadamard gate to place a single qubit into equal superposition. Measuring the qubit yields 0 or 1 with 50/50 probability — a truly random outcome governed by quantum mechanics, not pseudo-randomness.' },
  { id: 2, name: 'Quantum Entanglement', qubits: '2', gates: ['H','CNOT'], level: 'Beginner', desc: 'Two qubits instantly linked', detail: 'Creates a Bell state where two qubits become perfectly correlated regardless of distance. Measuring one instantly determines the other — the foundation of quantum teleportation and quantum networks.' },
  { id: 3, name: 'Quantum RNG', qubits: '5', gates: ['H'], level: 'Beginner', desc: 'True random numbers from physics', detail: 'Generates genuinely random numbers using quantum measurement. Unlike pseudo-random number generators, quantum randomness is fundamentally unpredictable — guaranteed by the laws of physics, not algorithmic complexity.' },
  { id: 4, name: "Grover's Search", qubits: '4', gates: ['H','X','Z','CNOT','TOFFOLI'], level: 'Intermediate', desc: 'Find 1 item in √N time', detail: "Implements Grover's algorithm to search an unsorted database quadratically faster than any classical algorithm. With 4 qubits, searches 16 items but finds the target in ~π√16/4 ≈ 3 iterations instead of 8 average classical steps." },
  { id: 5, name: 'Quantum Teleportation', qubits: '3', gates: ['H','X','Z','CNOT'], level: 'Intermediate', desc: 'Transfer quantum state without moving it', detail: 'Teleports the quantum state of one qubit to another using entanglement and classical communication. The original qubit is destroyed in the process (no-cloning theorem), but the state is perfectly reconstructed at the destination.' },
  { id: 6, name: 'DJ / QFT / VQE / Noise', qubits: '3–4', gates: ['H','X','Z','CNOT','RY'], level: 'Advanced', desc: 'Multiple quantum algorithms', detail: 'A comprehensive experiment covering four algorithms: Deutsch-Jozsa (determines if a function is constant or balanced in one query), Quantum Fourier Transform (exponential speedup for frequency analysis), Variational Quantum Eigensolver (finds molecular ground states), and Noise Simulation (models real quantum hardware errors).' },
  { id: 7, name: 'Quantum Coin Game', qubits: '1', gates: ['H','X','Z'], level: 'Beginner', desc: 'Quantum always wins the coin game', detail: 'Demonstrates quantum advantage through a simple game. The quantum player uses superposition to guarantee a win against any classical strategy — a direct proof that quantum strategies can be strictly superior.' },
  { id: 8, name: 'Password Cracker', qubits: '4', gates: ['H','X','Z','CNOT','TOFFOLI'], level: 'Intermediate', desc: "Grover's oracle for password search", detail: "Applies Grover's search algorithm to crack a 4-bit password. The quantum oracle marks the correct password, and amplitude amplification boosts its probability — finding it in √N iterations instead of N/2 average classical guesses." },
  { id: 9, name: 'Error Correction', qubits: '5', gates: ['X','CNOT','TOFFOLI'], level: 'Advanced', desc: 'Protect qubits from errors', detail: 'Implements a quantum error correction code that encodes one logical qubit across multiple physical qubits. Detects and corrects single-qubit errors (bit flips, phase flips) — essential for building reliable quantum computers.' },
  { id: 10, name: 'Random Walk', qubits: '6', gates: ['H','CNOT','X'], level: 'Intermediate', desc: 'Quantum spreads faster than classical', detail: 'Compares quantum and classical random walks. The quantum walker spreads quadratically faster due to superposition — after N steps, it covers √N more positions than its classical counterpart. Foundation for quantum search and graph algorithms.' },
  { id: 11, name: 'BB84 Key Distribution', qubits: '1', gates: ['H','X'], level: 'Intermediate', desc: 'Unbreakable quantum encryption', detail: 'Implements the BB84 quantum key distribution protocol. Two parties exchange a secret key using quantum states. Any eavesdropper disturbs the quantum states and is detected — provably secure encryption based on physics, not computational hardness.' },
  { id: 12, name: 'Superdense Coding', qubits: '2', gates: ['H','X','Z','CNOT'], level: 'Intermediate', desc: 'Send 2 classical bits using 1 qubit', detail: 'Transmits two bits of classical information by sending just one qubit, using pre-shared entanglement. This doubles the classical channel capacity — a foundational quantum communication protocol.' },
  { id: 13, name: 'Quantum Fruit Classifier', qubits: '4', gates: ['H','RY','RZ','CNOT'], level: 'AI+Quantum', desc: 'SVM + quantum feature map', detail: 'Uses a quantum feature map to embed classical data (fruit measurements) into quantum Hilbert space, then applies a support vector machine. Classical accuracy: 100%. Quantum accuracy: 78%. The quantum approach maps features to a higher-dimensional space inaccessible to classical kernels.', classical: 100, quantum: 78 },
  { id: 14, name: 'Hybrid Quantum Neural Network', qubits: '4', gates: ['H','RY','RZ','CNOT'], level: 'AI+Quantum', desc: 'PyTorch + QPanda3', detail: 'Integrates a parameterized quantum circuit as a layer inside a PyTorch neural network. Classical accuracy: 96.7%. Quantum accuracy: 70%. The quantum layer introduces entanglement-based feature interactions that classical layers cannot replicate.', classical: 96.7, quantum: 70 },
  { id: 15, name: 'Quantum Random Forest', qubits: '8–16', gates: ['H'], level: 'AI+Quantum', desc: 'QRNG seeds for Random Forest', detail: 'Uses quantum random number generation to seed a Random Forest classifier. Classical accuracy: 99.4%. Quantum accuracy: 97.6%. True quantum randomness improves the diversity of decision trees, potentially reducing overfitting in specific scenarios.', classical: 99.4, quantum: 97.6 },
  { id: 16, name: 'Quantum vs Classical Showdown', qubits: '4', gates: ['H','RY','RZ','CNOT'], level: 'AI+Quantum', desc: '5 algorithms compared', detail: 'A comprehensive benchmark comparing 5 ML algorithms with quantum-enhanced versions: Logistic Regression, SVM, Random Forest, KNN, and Quantum Circuit Classifier. Random Forest won at 90% accuracy. Demonstrates where quantum helps and where classical still dominates.', classical: 90, quantum: null, note: 'Best: Random Forest at 90%' },
  { id: 17, name: 'Quantum Stock Predictor', qubits: '4', gates: ['H','RY','RZ','CNOT'], level: 'AI+Quantum', desc: 'Stock prediction comparison', detail: 'Applies quantum-enhanced ML to stock price prediction. Classical: 76.2%. Quantum: 49.7%. Hybrid: 74.1%. Financial data is noisy and high-dimensional — the hybrid approach narrows the gap by combining classical feature engineering with quantum circuit expressibility.', classical: 76.2, quantum: 49.7, hybrid: 74.1 },
  { id: 18, name: "Bell's Inequality Test", qubits: '2', gates: ['H','CNOT','RY'], level: 'Fun', desc: 'Tests if God plays dice', detail: "Measures Bell's inequality parameter S. Result: S = 2.847, violating the classical limit of 2.0. This proves quantum mechanics is non-local — entangled particles share correlations that cannot be explained by any local hidden variable theory. Einstein called it \"spooky action at a distance.\"" },
  { id: 19, name: 'Chicken or Egg', qubits: '4', gates: ['H','CNOT','X','Z'], level: 'Fun', desc: 'Quantum causal order — both came first', detail: 'Implements a quantum switch that places two operations in an indefinite causal order. Result: both the chicken and the egg came first simultaneously. Demonstrates that quantum mechanics allows superposition of causal orders — a concept with no classical analog.' },
  { id: 20, name: 'Multi-Algorithm Suite', qubits: '3–4', gates: ['H','X','Z','CNOT','RY'], level: 'Fun', desc: 'DJ Algorithm, QFT, VQE, Noise Sim sub-experiments', detail: 'A bonus collection of four quantum algorithm sub-experiments packaged as a mini-suite: Deutsch-Jozsa for function classification, QFT for frequency domain analysis, VQE for chemistry simulation, and a noise model simulating real quantum hardware imperfections.' }
];

const CONCEPTS = [
  { name: 'Superposition', explain: 'A qubit exists in multiple states simultaneously until measured. Like a coin spinning in the air — it is both heads and tails.', experiments: [1, 3, 7], application: 'Parallel computation, quantum speedup' },
  { name: 'Entanglement', explain: 'Two qubits become correlated so that measuring one instantly determines the other, regardless of distance.', experiments: [2, 5, 12, 18], application: 'Quantum internet, secure communication' },
  { name: 'Quantum Gates', explain: 'Operations that manipulate qubits — H creates superposition, CNOT entangles, X/Z flip states. The building blocks of quantum circuits.', experiments: [1, 2, 4, 5, 7, 8], application: 'All quantum algorithms' },
  { name: "Grover's Search", explain: 'A quantum algorithm that finds a specific item in an unsorted database using only √N steps instead of N.', experiments: [4, 8], application: 'Database search, optimization, cryptanalysis' },
  { name: 'Teleportation', explain: 'Transfers a quantum state from one qubit to another using entanglement and classical bits — without physically moving the qubit.', experiments: [5], application: 'Quantum networking, distributed quantum computing' },
  { name: 'QFT', explain: 'Quantum Fourier Transform decomposes quantum states into frequency components exponentially faster than the classical FFT.', experiments: [6, 20], application: "Shor's algorithm, phase estimation, signal processing" },
  { name: 'VQE', explain: 'Variational Quantum Eigensolver finds the lowest energy state of molecules using a hybrid quantum-classical optimization loop.', experiments: [6, 20], application: 'Drug discovery, materials science, chemistry' },
  { name: 'Error Correction', explain: 'Encodes logical qubits across multiple physical qubits to detect and fix errors caused by noise and decoherence.', experiments: [9], application: 'Fault-tolerant quantum computing' },
  { name: 'BB84 / QKD', explain: 'Quantum Key Distribution uses quantum states to share encryption keys. Any eavesdropper is detected by the laws of physics.', experiments: [11], application: 'Unbreakable encryption, military/banking security' },
  { name: 'Quantum Feature Maps', explain: 'Embed classical data into quantum Hilbert space to access exponentially larger feature spaces for ML.', experiments: [13, 14, 16], application: 'Quantum machine learning, classification' },
  { name: 'Hybrid QNN', explain: 'Neural networks with quantum circuit layers integrated into classical frameworks like PyTorch for quantum-enhanced learning.', experiments: [14], application: 'Image recognition, NLP, drug discovery' },
  { name: 'Quantum RNG', explain: 'True random number generation based on quantum measurement — fundamentally unpredictable, unlike classical pseudo-RNG.', experiments: [3, 15], application: 'Cryptography, Monte Carlo simulation, gaming' },
  { name: 'Benchmarking', explain: 'Systematic comparison of quantum vs classical algorithm performance to identify where quantum provides genuine advantage.', experiments: [16, 17], application: 'Algorithm selection, quantum readiness assessment' },
  { name: 'Quantum Finance', explain: 'Applying quantum computing to financial prediction, portfolio optimization, and risk analysis.', experiments: [17], application: 'Stock prediction, option pricing, risk management' }
];

const LEVELS = ['All', 'Beginner', 'Intermediate', 'Advanced', 'AI+Quantum', 'Fun'];
const LEVEL_COLORS = { Beginner: 'badge-beginner', Intermediate: 'badge-intermediate', Advanced: 'badge-advanced', 'AI+Quantum': 'badge-ai', Fun: 'badge-fun' };

// ============ ROUTING ============
const SECTIONS = {
  overview: { title: 'Overview', el: 'sec-overview' },
  experiments: { title: 'Experiments', el: 'sec-experiments' },
  results: { title: 'AI vs Quantum', el: 'sec-results' },
  concepts: { title: 'Concepts', el: 'sec-concepts' },
  stack: { title: 'Tech Stack', el: 'sec-stack' },
  about: { title: 'About', el: 'sec-about' }
};

let currentSection = 'overview';
let chartsInitialized = {};

function navigate(section) {
  if (!SECTIONS[section]) section = 'overview';
  currentSection = section;

  // Update nav
  document.querySelectorAll('.nav-item').forEach(n => {
    n.classList.toggle('active', n.dataset.section === section);
  });

  // Update sections
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  const target = document.getElementById(SECTIONS[section].el);
  if (target) {
    target.classList.add('active');
    // Re-trigger animation
    target.style.animation = 'none';
    target.offsetHeight; // reflow
    target.style.animation = '';
  }

  // Update header
  document.getElementById('headerTitle').textContent = SECTIONS[section].title;

  // Close mobile sidebar
  closeSidebar();

  // Scroll main to top
  document.querySelector('.main').scrollTop = 0;

  // Init charts on first visit
  if (section === 'overview' && !chartsInitialized.overview) {
    requestAnimationFrame(() => { initOverviewCharts(); chartsInitialized.overview = true; });
  }
  if (section === 'results' && !chartsInitialized.results) {
    requestAnimationFrame(() => { initComparisonChart(); chartsInitialized.results = true; });
  }

  // Animate KPIs on overview
  if (section === 'overview') {
    requestAnimationFrame(animateKPIs);
  }
}

// Hash routing
function handleHash() {
  const hash = location.hash.replace('#', '') || 'overview';
  navigate(hash);
}

window.addEventListener('hashchange', handleHash);

// Nav clicks
document.querySelectorAll('.nav-item').forEach(item => {
  item.addEventListener('click', (e) => {
    e.preventDefault();
    const section = item.dataset.section;
    history.pushState(null, '', '#' + section);
    navigate(section);
  });
});

// ============ MOBILE SIDEBAR ============
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('sidebarOverlay');
const hamburger = document.getElementById('hamburgerBtn');

function openSidebar() {
  sidebar.classList.add('open');
  overlay.classList.add('open');
}

function closeSidebar() {
  sidebar.classList.remove('open');
  overlay.classList.remove('open');
}

hamburger.addEventListener('click', () => {
  sidebar.classList.contains('open') ? closeSidebar() : openSidebar();
});
overlay.addEventListener('click', closeSidebar);

// ============ THEME TOGGLE ============
(function() {
  const toggle = document.querySelector('[data-theme-toggle]');
  const root = document.documentElement;
  let theme = 'dark';
  root.setAttribute('data-theme', theme);

  if (toggle) {
    toggle.addEventListener('click', () => {
      theme = theme === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', theme);
      toggle.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`);
      toggle.innerHTML = theme === 'dark'
        ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>'
        : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';

      // Rebuild charts with new colors
      destroyCharts();
      chartsInitialized = {};
      if (currentSection === 'overview') {
        requestAnimationFrame(() => { initOverviewCharts(); chartsInitialized.overview = true; });
      }
      if (currentSection === 'results') {
        requestAnimationFrame(() => { initComparisonChart(); chartsInitialized.results = true; });
      }
    });
  }
})();

// ============ KPI ANIMATION ============
function animateKPIs() {
  document.querySelectorAll('.kpi-value[data-count]').forEach(el => {
    const target = parseInt(el.dataset.count);
    const suffix = el.dataset.suffix || '';
    animateNumber(el, 0, target, 800, suffix);
  });

  document.querySelectorAll('.kpi-value[data-count-text]').forEach(el => {
    const text = el.dataset.countText;
    setTimeout(() => { el.textContent = text; }, 400);
  });
}

function animateNumber(el, start, end, duration, suffix) {
  const startTime = performance.now();
  const format = (n) => {
    if (n >= 1000000) return (n / 1000000).toFixed(1).replace(/\.0$/, '') + 'M';
    if (n >= 1000) return n.toLocaleString();
    return n.toString();
  };

  function tick(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    // Ease out cubic
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.round(start + (end - start) * eased);
    el.textContent = format(current) + suffix;
    if (progress < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

// ============ CHARTS ============
let chartInstances = {};

function getChartColors() {
  const style = getComputedStyle(document.documentElement);
  return {
    primary: style.getPropertyValue('--color-primary').trim(),
    gold: style.getPropertyValue('--color-gold').trim(),
    success: style.getPropertyValue('--color-success').trim(),
    blue: style.getPropertyValue('--color-blue').trim(),
    purple: style.getPropertyValue('--color-purple').trim(),
    orange: style.getPropertyValue('--color-orange').trim(),
    error: style.getPropertyValue('--color-error').trim(),
    text: style.getPropertyValue('--color-text').trim(),
    textMuted: style.getPropertyValue('--color-text-muted').trim(),
    textFaint: style.getPropertyValue('--color-text-faint').trim(),
    border: style.getPropertyValue('--color-border').trim(),
    surface: style.getPropertyValue('--color-surface').trim()
  };
}

function destroyCharts() {
  Object.values(chartInstances).forEach(c => c.destroy());
  chartInstances = {};
}

function initOverviewCharts() {
  const c = getChartColors();

  // Levels bar chart
  const ctxLevels = document.getElementById('chartLevels');
  if (ctxLevels) {
    chartInstances.levels = new Chart(ctxLevels, {
      type: 'bar',
      data: {
        labels: ['Beginner', 'Intermediate', 'Advanced', 'AI+Quantum', 'Fun/Bonus'],
        datasets: [{
          data: [4, 6, 2, 5, 3],
          backgroundColor: [c.success, c.blue, c.purple, c.orange, c.gold],
          borderRadius: 6,
          borderSkipped: false,
          maxBarThickness: 48
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 800, easing: 'easeOutCubic' },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: c.surface,
            titleColor: c.text,
            bodyColor: c.textMuted,
            borderColor: c.border,
            borderWidth: 1,
            padding: 12,
            cornerRadius: 8,
            titleFont: { family: "'Sora', sans-serif", weight: 600 },
            bodyFont: { family: "'Inter', sans-serif" }
          }
        },
        scales: {
          x: {
            grid: { color: c.border + '33', lineWidth: 0.5 },
            ticks: { color: c.textMuted, font: { family: "'Inter', sans-serif", size: 11 } },
            border: { display: false }
          },
          y: {
            grid: { display: false },
            ticks: { color: c.textMuted, font: { family: "'Inter', sans-serif", size: 12 } },
            border: { display: false }
          }
        }
      }
    });
  }

  // Distribution donut
  const ctxDist = document.getElementById('chartDistribution');
  if (ctxDist) {
    chartInstances.distribution = new Chart(ctxDist, {
      type: 'doughnut',
      data: {
        labels: ['Pure Quantum', 'Classical Baseline', 'Hybrid AI+Quantum'],
        datasets: [{
          data: [12, 3, 5],
          backgroundColor: [c.primary, c.textFaint, c.gold],
          borderColor: 'transparent',
          borderWidth: 2,
          hoverOffset: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '60%',
        animation: { animateRotate: true, duration: 800 },
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              color: c.textMuted,
              font: { family: "'Inter', sans-serif", size: 12 },
              padding: 16,
              usePointStyle: true,
              pointStyleWidth: 10
            }
          },
          tooltip: {
            backgroundColor: c.surface,
            titleColor: c.text,
            bodyColor: c.textMuted,
            borderColor: c.border,
            borderWidth: 1,
            padding: 12,
            cornerRadius: 8
          }
        }
      }
    });
  }
}

function initComparisonChart() {
  const c = getChartColors();
  const ctx = document.getElementById('chartComparison');
  if (!ctx) return;

  chartInstances.comparison = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Fruit Classifier', 'Hybrid QNN', 'Random Forest', 'Showdown', 'Stock Predictor'],
      datasets: [
        {
          label: 'Classical',
          data: [100, 96.7, 99.4, 90, 76.2],
          backgroundColor: c.textMuted + 'AA',
          borderRadius: 4,
          maxBarThickness: 36
        },
        {
          label: 'Quantum',
          data: [78, 70, 97.6, null, 49.7],
          backgroundColor: c.primary + 'CC',
          borderRadius: 4,
          maxBarThickness: 36
        },
        {
          label: 'Hybrid',
          data: [null, null, null, null, 74.1],
          backgroundColor: c.gold + 'CC',
          borderRadius: 4,
          maxBarThickness: 36
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 800, easing: 'easeOutCubic' },
      plugins: {
        legend: {
          position: 'top',
          align: 'end',
          labels: {
            color: c.textMuted,
            font: { family: "'Inter', sans-serif", size: 12 },
            padding: 16,
            usePointStyle: true,
            pointStyleWidth: 10
          }
        },
        tooltip: {
          backgroundColor: c.surface,
          titleColor: c.text,
          bodyColor: c.textMuted,
          borderColor: c.border,
          borderWidth: 1,
          padding: 12,
          cornerRadius: 8,
          callbacks: {
            label: function(ctx) {
              return ctx.dataset.label + ': ' + (ctx.raw !== null ? ctx.raw + '%' : 'N/A');
            }
          }
        }
      },
      scales: {
        y: {
          min: 0,
          max: 105,
          grid: { color: c.border + '33', lineWidth: 0.5 },
          ticks: {
            color: c.textMuted,
            font: { family: "'Inter', sans-serif", size: 11 },
            callback: v => v + '%'
          },
          border: { display: false }
        },
        x: {
          grid: { display: false },
          ticks: { color: c.textMuted, font: { family: "'Inter', sans-serif", size: 11 } },
          border: { display: false }
        }
      }
    }
  });
}

// ============ EXPERIMENTS GRID ============
function renderExperiments(filter) {
  const grid = document.getElementById('expGrid');
  const filtered = filter === 'All' ? EXPERIMENTS : EXPERIMENTS.filter(e => e.level === filter);

  grid.innerHTML = filtered.map((exp, i) => `
    <div class="exp-card" data-exp="${exp.id}" style="animation-delay:${i * 40}ms" tabindex="0" role="button" aria-label="View ${exp.name}">
      <div class="exp-card-header">
        <span class="exp-number">#${String(exp.id).padStart(2, '0')}</span>
        <span class="badge ${LEVEL_COLORS[exp.level]}">${exp.level}</span>
      </div>
      <div class="exp-name">${exp.name}</div>
      <div class="exp-desc">${exp.desc}</div>
      <div class="exp-meta">
        <span class="qubit-badge">${exp.qubits}q</span>
        ${exp.gates.slice(0, 4).map(g => `<span class="gate-pill">${g}</span>`).join('')}
        ${exp.gates.length > 4 ? `<span class="gate-pill">+${exp.gates.length - 4}</span>` : ''}
      </div>
    </div>
  `).join('');

  // Card click handlers
  grid.querySelectorAll('.exp-card').forEach(card => {
    const handler = () => openModal(parseInt(card.dataset.exp));
    card.addEventListener('click', handler);
    card.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); handler(); } });
  });
}

function renderFilters() {
  const bar = document.getElementById('filterBar');
  bar.innerHTML = LEVELS.map(level => `
    <button class="filter-btn ${level === 'All' ? 'active' : ''}" data-filter="${level}">${level}</button>
  `).join('');

  bar.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      bar.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderExperiments(btn.dataset.filter);
    });
  });
}

// ============ MODAL ============
function openModal(id) {
  const exp = EXPERIMENTS.find(e => e.id === id);
  if (!exp) return;

  const content = document.getElementById('modalContent');
  let html = `
    <div class="modal-exp-number">Experiment #${String(exp.id).padStart(2, '0')}</div>
    <div class="modal-exp-name">${exp.name}</div>
    <div class="modal-desc">${exp.detail}</div>
    <div class="modal-detail-row">
      <span class="modal-detail-label">Level</span>
      <span class="modal-detail-value"><span class="badge ${LEVEL_COLORS[exp.level]}">${exp.level}</span></span>
    </div>
    <div class="modal-detail-row">
      <span class="modal-detail-label">Qubits</span>
      <span class="modal-detail-value">${exp.qubits}</span>
    </div>
    <div class="modal-detail-row">
      <span class="modal-detail-label">Gates</span>
      <span class="modal-detail-value">${exp.gates.map(g => `<span class="gate-pill">${g}</span>`).join('')}</span>
    </div>
  `;

  if (exp.classical !== undefined) {
    html += `
      <div style="margin-top:var(--space-4);padding-top:var(--space-4);border-top:1px solid var(--color-divider);">
        <div class="modal-detail-row">
          <span class="modal-detail-label">Classical</span>
          <span class="modal-detail-value" style="font-variant-numeric:tabular-nums;font-weight:600;">${exp.classical}%</span>
        </div>
        ${exp.quantum !== null ? `<div class="modal-detail-row">
          <span class="modal-detail-label">Quantum</span>
          <span class="modal-detail-value" style="color:var(--color-primary);font-variant-numeric:tabular-nums;font-weight:600;">${exp.quantum}%</span>
        </div>` : ''}
        ${exp.hybrid ? `<div class="modal-detail-row">
          <span class="modal-detail-label">Hybrid</span>
          <span class="modal-detail-value" style="color:var(--color-gold);font-variant-numeric:tabular-nums;font-weight:600;">${exp.hybrid}%</span>
        </div>` : ''}
        ${exp.note ? `<div style="font-size:var(--text-xs);color:var(--color-text-faint);margin-top:var(--space-2);">${exp.note}</div>` : ''}
      </div>
    `;
  }

  content.innerHTML = html;
  document.getElementById('modalOverlay').classList.add('open');
  document.getElementById('modalClose').focus();
}

function closeModal() {
  document.getElementById('modalOverlay').classList.remove('open');
}

document.getElementById('modalClose').addEventListener('click', closeModal);
document.getElementById('modalOverlay').addEventListener('click', (e) => {
  if (e.target === e.currentTarget) closeModal();
});
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeModal();
});

// ============ CONCEPTS GRID ============
function renderConcepts() {
  const grid = document.getElementById('conceptsGrid');
  grid.innerHTML = CONCEPTS.map(c => `
    <div class="concept-card">
      <div class="concept-name">${c.name}</div>
      <div class="concept-explain">${c.explain}</div>
      <div class="concept-meta">
        <strong>Experiments:</strong> ${c.experiments.map(id => '#' + id).join(', ')}<br>
        <strong>Application:</strong> ${c.application}
      </div>
    </div>
  `).join('');
}

// ============ INIT ============
function init() {
  renderFilters();
  renderExperiments('All');
  renderConcepts();
  handleHash();

  // Init overview charts and KPIs on first load
  if (currentSection === 'overview') {
    // Wait for Chart.js to load
    const waitForChart = () => {
      if (typeof Chart !== 'undefined') {
        initOverviewCharts();
        chartsInitialized.overview = true;
        animateKPIs();
      } else {
        setTimeout(waitForChart, 50);
      }
    };
    waitForChart();
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
