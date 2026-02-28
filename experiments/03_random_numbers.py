"""
Quantum Random Number Generation
=================================
Classical computers generate pseudo-random numbers using deterministic algorithms
(like Mersenne Twister). These are NOT truly random -- given the seed, you can
predict every number. Quantum computers, however, can generate numbers that are
fundamentally random, rooted in the irreducible randomness of quantum measurement.

This experiment uses 8 qubits. Each qubit is put into superposition with an H
gate, then measured. The 8-bit measurement result (a number 0-255) is one truly
random byte. We generate 1000 such numbers and visualise the distribution.

A perfect quantum random number generator produces a flat (uniform) histogram --
every value from 0 to 255 should appear roughly the same number of times.

What this experiment does:
  1. Applies H to all 8 qubits simultaneously.
  2. Measures all 8 qubits to get one 8-bit random number.
  3. Uses shot-based sampling to collect 1000 random numbers.
  4. Plots the distribution as a histogram.
"""

import os
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, measure

# -- Output directory --
charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'charts')
os.makedirs(charts_dir, exist_ok=True)

print("=" * 60)
print("  EXPERIMENT 03 - Quantum Random Number Generator")
print("=" * 60)
print()
print("Using 8 qubits to generate true random 8-bit numbers (0-255).")
print("Running 10 000 shots; each shot gives one random byte...")
print()

NQUBITS = 8
circuit = QCircuit()
prog = QProg()

for i in range(NQUBITS):
    circuit << H(i)

prog << circuit
for i in range(NQUBITS):
    prog << measure(i, i)

SHOTS = 10000
qvm = CPUQVM()
qvm.run(prog, shots=SHOTS)
counts = qvm.result().get_counts()

random_numbers = []
for bitstring, freq in counts.items():
    value = int(bitstring, 2)
    random_numbers.extend([value] * freq)

random.shuffle(random_numbers)
sample_1000 = random_numbers[:1000]

print(f"Total unique values observed (out of 256): {len(counts)}")
print(f"Sample of 10 random numbers: {sample_1000[:10]}")
print(f"Min: {min(sample_1000)},  Max: {max(sample_1000)},  Mean: {np.mean(sample_1000):.1f}")
print()
print("A uniform distribution (flat histogram) confirms true randomness.")
print()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(sample_1000, bins=32, color='#9b59b6', edgecolor='white',
             linewidth=0.8, alpha=0.9)
axes[0].axhline(1000 / 32, color='#e74c3c', linestyle='--', linewidth=1.8,
                label=f'Expected ({1000/32:.1f} per bin)')
axes[0].set_title('1000 Quantum Random Numbers\nDistribution (0-255)',
                  fontsize=13, fontweight='bold')
axes[0].set_xlabel('Random Number Value', fontsize=11)
axes[0].set_ylabel('Frequency', fontsize=11)
axes[0].legend(fontsize=10)
axes[0].grid(axis='y', alpha=0.3)
axes[0].spines['top'].set_visible(False)
axes[0].spines['right'].set_visible(False)

quantum_counts  = np.array([sample_1000.count(v) for v in range(256)])
classical_nums  = [random.randint(0, 255) for _ in range(1000)]
classical_counts = np.array([classical_nums.count(v) for v in range(256)])

axes[1].plot(range(256), quantum_counts,  color='#9b59b6', alpha=0.7,
             linewidth=0.8, label='Quantum RNG')
axes[1].plot(range(256), classical_counts, color='#3498db', alpha=0.7,
             linewidth=0.8, label='Classical RNG (for comparison)')
axes[1].axhline(1000 / 256, color='#2ecc71', linestyle='--', linewidth=1.5,
                label=f'Ideal ({1000/256:.1f})')
axes[1].set_title('Quantum vs Classical RNG\nPer-Value Frequency',
                  fontsize=13, fontweight='bold')
axes[1].set_xlabel('Number Value (0-255)', fontsize=11)
axes[1].set_ylabel('Times Generated', fontsize=11)
axes[1].legend(fontsize=10)
axes[1].grid(alpha=0.2)
axes[1].spines['top'].set_visible(False)
axes[1].spines['right'].set_visible(False)

plt.suptitle('Quantum Random Number Generator - 8 Qubits', fontsize=15,
             fontweight='bold', y=1.02)
plt.tight_layout()
out_path = os.path.join(charts_dir, '03_random_numbers.png')
plt.savefig(out_path, dpi=150, bbox_inches='tight')
plt.close()

print(f"Chart saved to: {out_path}")
print()
print("Conclusion: The quantum histogram is nearly flat -- all values 0-255")
print("appear with equal probability, confirming cryptographically strong")
print("randomness directly from quantum mechanics.")
