"""
Classical vs Quantum Random Walk
==================================
A random walk is the mathematical formalisation of "taking random steps."
It models everything from stock prices and diffusion to polymer chains.

CLASSICAL RANDOM WALK:
  At each step, move left (-1) or right (+1) with equal probability.
  After N steps, the probability distribution is a Gaussian (bell curve)
  centred at 0. Standard deviation grows as sqrt(N) (diffusion-like spreading).

QUANTUM WALK:
  The quantum analogue uses a "coin qubit" to determine direction.
  But because the coin is in superposition, the walker can go both left AND
  right simultaneously. Interference effects accumulate over steps, producing
  a very different distribution -- two peaks near +/-N/sqrt(2) instead of one
  central peak. The quantum walk spreads quadratically faster (sigma ~ N vs sqrt(N)).

This experiment:
  1. Simulates 5000 classical random walks for 10, 20, and 50 steps.
  2. Analytically computes the quantum walk distribution using the quantum
     walk recurrence relation (unitary coin operator = Hadamard).
  3. Shows side-by-side comparison for each step count in 3 charts.

Note: Full QPanda3 quantum walk simulation requires N qubits for N-step
position space. We use the theoretical quantum walk distribution here to
clearly demonstrate the conceptual difference, which is the educational
goal of this experiment.
"""

import os
import random
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# -- Output directory --
charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'charts')
os.makedirs(charts_dir, exist_ok=True)

print("=" * 60)
print("  EXPERIMENT 10 - Classical vs Quantum Random Walk")
print("=" * 60)
print()


# -- Classical Random Walk --
def classical_walk_distribution(n_steps, n_walkers=5000):
    positions = np.zeros(n_walkers, dtype=int)
    for _ in range(n_steps):
        steps = np.random.choice([-1, 1], size=n_walkers)
        positions += steps
    return positions


# -- Quantum Walk (analytical) --
def quantum_walk_distribution(n_steps):
    """
    Compute the position probability distribution for a Hadamard quantum walk.
    State: |position, coin>. Position ranges from -n_steps to +n_steps (step 2).
    Returns (positions, probabilities).
    """
    state = {}
    state[(0, 0)] = 1.0 / math.sqrt(2)
    state[(0, 1)] = 1j  / math.sqrt(2)

    for _ in range(n_steps):
        new_state = {}
        for (pos, coin), amp in state.items():
            if coin == 0:
                h00 =  amp / math.sqrt(2)
                h01 =  amp / math.sqrt(2)
            else:
                h00 =  amp / math.sqrt(2)
                h01 = -amp / math.sqrt(2)

            key_r = (pos + 1, 0)
            key_l = (pos - 1, 1)
            new_state[key_r] = new_state.get(key_r, 0) + h00
            new_state[key_l] = new_state.get(key_l, 0) + h01
        state = new_state

    positions_prob = {}
    for (pos, coin), amp in state.items():
        positions_prob[pos] = positions_prob.get(pos, 0) + abs(amp) ** 2

    all_positions = sorted(positions_prob.keys())
    probs = np.array([positions_prob[p] for p in all_positions])
    return np.array(all_positions), probs


# -- Run for 3 step counts --
step_counts = [10, 20, 50]
N_WALKERS = 5000

print(f"Simulating {N_WALKERS} classical walkers for each step count...")
print()

classical_results = {}
quantum_results   = {}

for n in step_counts:
    cpos = classical_walk_distribution(n, N_WALKERS)
    classical_results[n] = cpos
    qpos, qprob = quantum_walk_distribution(n)
    quantum_results[n] = (qpos, qprob)

    c_std = np.std(cpos)
    q_std = np.sqrt(np.sum(qpos**2 * qprob) - np.sum(qpos * qprob)**2)
    print(f"  {n:2d} steps -- Classical sigma = {c_std:.2f}  (theory: {math.sqrt(n):.2f})")
    print(f"          Quantum sigma  = {q_std:.2f}  (theory: {n/math.sqrt(2):.2f})")
    print()

print("The quantum walk spreads much faster: sigma_quantum ~ N/sqrt(2) vs sigma_classical ~ sqrt(N)")
print()

# -- Plot --
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

for i, n in enumerate(step_counts):
    ax = axes[i]

    cpos = classical_results[n]
    bins = np.arange(-n - 1.5, n + 2.5, 2)
    ax.hist(cpos, bins=bins, density=True, color='#3498db', alpha=0.65,
            label='Classical walk', edgecolor='white', linewidth=0.5)

    qpos, qprob = quantum_results[n]
    bin_width = 2
    ax.plot(qpos, qprob / bin_width, color='#e74c3c', linewidth=2.2,
            label='Quantum walk (theory)', zorder=5)
    ax.fill_between(qpos, qprob / bin_width, alpha=0.25, color='#e74c3c')

    x_range = np.linspace(-n * 1.1, n * 1.1, 300)
    gaussian = (1 / (math.sqrt(n) * math.sqrt(2 * math.pi))) * \
               np.exp(-x_range**2 / (2 * n))
    ax.plot(x_range, gaussian, '--', color='#2ecc71', linewidth=1.5,
            label='Classical Gaussian fit')

    ax.set_title(f'{n}-Step Random Walk', fontsize=13, fontweight='bold')
    ax.set_xlabel('Position', fontsize=11)
    ax.set_ylabel('Probability Density', fontsize=11)
    ax.legend(fontsize=9, loc='upper left')
    ax.grid(alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    c_std = np.std(cpos)
    q_std = float(np.sqrt(np.sum(qpos**2 * qprob) - np.sum(qpos * qprob)**2))
    ax.text(0.97, 0.95,
            f'Classical sigma = {c_std:.1f}\nQuantum sigma = {q_std:.1f}',
            transform=ax.transAxes, ha='right', va='top',
            fontsize=9, bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

plt.suptitle('Classical vs Quantum Random Walk\n'
             'Quantum walk has two peaks and spreads proportional to N (vs sqrt(N) for classical)',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
out_path = os.path.join(charts_dir, '10_random_walk.png')
plt.savefig(out_path, dpi=150, bbox_inches='tight')
plt.close()

print(f"Chart saved to: {out_path}")
print()
print("Conclusion: The quantum walk shows a characteristic two-peaked distribution")
print("with much faster spreading than the classical Gaussian -- a quadratic")
print("speedup that underpins quantum search and graph algorithms.")
