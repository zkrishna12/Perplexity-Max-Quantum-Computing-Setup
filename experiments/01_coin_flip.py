"""
Quantum Coin Flip
=================
A classical coin flip uses physical randomness (gravity, spin, air currents) to
produce heads or tails with roughly 50/50 probability. A quantum coin flip does
the same thing but uses the fundamental laws of quantum mechanics -- specifically
the Hadamard (H) gate -- to put a single qubit into a perfect superposition of
|0> and |1>. When measured, it collapses randomly to 0 ("tails") or 1 ("heads")
with exactly 50% probability each. This is true randomness at the quantum level,
unlike any classical pseudo-random algorithm.

What this experiment does:
  1. Applies the H gate to qubit 0, creating an equal superposition state.
  2. Measures the qubit 1000 times (shots).
  3. Plots a bar chart showing the near-50/50 split between 0 and 1.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, measure

# -- Output directory --
charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'charts')
os.makedirs(charts_dir, exist_ok=True)

# -- Build the quantum circuit --
print("=" * 60)
print("  EXPERIMENT 01 - Quantum Coin Flip")
print("=" * 60)
print()
print("Building circuit: H gate on qubit 0 creates a superposition.")
print("Measuring 1000 times to simulate 1000 quantum coin flips...")
print()

circuit = QCircuit()
circuit << H(0)                        # Put qubit into superposition

prog = QProg()
prog << circuit << measure(0, 0)       # Measure qubit 0 -> classical bit 0

# -- Run on the CPU simulator --
qvm = CPUQVM()
qvm.run(prog, shots=1000)
counts = qvm.result().get_counts()     # e.g. {'0': 503, '1': 497}

# -- Extract results --
tails = counts.get('0', 0)            # qubit measured as 0 -> "Tails"
heads = counts.get('1', 0)            # qubit measured as 1 -> "Heads"
total = tails + heads

print(f"Results from 1000 quantum coin flips:")
print(f"  Tails (|0>) : {tails:5d}  ({100 * tails / total:.1f}%)")
print(f"  Heads (|1>) : {heads:5d}  ({100 * heads / total:.1f}%)")
print()
print("The H gate creates a perfect quantum superposition. Each flip is")
print("independent and truly random -- no pattern can ever be predicted.")
print()

# -- Plot --
fig, ax = plt.subplots(figsize=(7, 5))

labels = ['Tails (|0>)', 'Heads (|1>)']
values = [tails, heads]
colors = ['#3498db', '#e74c3c']

bars = ax.bar(labels, values, color=colors, edgecolor='white', linewidth=1.5,
              width=0.5)

# Value labels on bars
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 8,
            f'{val}\n({100 * val / total:.1f}%)',
            ha='center', va='bottom', fontsize=12, fontweight='bold')

# 50% reference line
ax.axhline(500, color='#2ecc71', linestyle='--', linewidth=1.8,
           label='Perfect 50%')

ax.set_title('Quantum Coin Flip - 1000 Shots', fontsize=15, fontweight='bold',
             pad=14)
ax.set_ylabel('Number of Outcomes', fontsize=12)
ax.set_ylim(0, max(values) * 1.25)
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
out_path = os.path.join(charts_dir, '01_coin_flip.png')
plt.savefig(out_path, dpi=150)
plt.close()

print(f"Chart saved to: {out_path}")
print()
print("Conclusion: The quantum coin flip produces results very close to the")
print("ideal 50/50 split, demonstrating quantum superposition in action.")
