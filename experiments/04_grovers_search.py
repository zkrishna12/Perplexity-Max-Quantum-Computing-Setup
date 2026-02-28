"""
Grover's Search Algorithm (2 Qubits)
======================================
Searching an unsorted list classically requires checking items one by one --
on average N/2 checks for N items. Grover's quantum search algorithm can find
the answer in roughly sqrt(N) steps, which for N=4 items means just 1 step!

This experiment searches a 2-qubit space (4 possible states: 00, 01, 10, 11)
for the target state '11'. Grover's algorithm amplifies the probability of the
target state so it becomes overwhelmingly likely after just one iteration.

How it works:
  1. Initialise: H gates on both qubits -> equal superposition over all 4 states.
  2. Oracle: Marks the target '11' with a phase flip using CZ(0,1).
     (CZ flips the phase of |11> only, since both qubits must be 1.)
  3. Diffusion (Amplitude Amplification): H, X on both -> CZ -> X, H on both.
     This "reflects" all amplitudes about the average, boosting the target.
  4. Measure: The target '11' should appear ~100% of the time.

What this experiment does:
  1. Runs Grover's algorithm for target '11'.
  2. Plots a bar chart confirming ~100% probability for '11'.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, X, CZ, measure

# -- Output directory --
charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'charts')
os.makedirs(charts_dir, exist_ok=True)

print("=" * 60)
print("  EXPERIMENT 04 - Grover's Search Algorithm (2 Qubits)")
print("=" * 60)
print()
print("Searching 4-item database for target: '11'")
print("Classical search: up to 4 checks. Quantum: just 1 iteration!")
print()

circuit = QCircuit()

# Step 1: Initialisation - equal superposition
circuit << H(0) << H(1)

# Step 2: Oracle for target |11> - CZ flips phase only when both qubits are 1
circuit << CZ(0, 1)

# Step 3: Diffusion operator (Grover's amplitude amplification)
circuit << H(0) << H(1)
circuit << X(0) << X(1)
circuit << CZ(0, 1)
circuit << X(0) << X(1)
circuit << H(0) << H(1)

prog = QProg()
prog << circuit << measure(0, 0) << measure(1, 1)

SHOTS = 10000
qvm = CPUQVM()
qvm.run(prog, shots=SHOTS)
counts = qvm.result().get_counts()

all_outcomes = {'00': 0, '01': 0, '10': 0, '11': 0}
all_outcomes.update(counts)
total = sum(all_outcomes.values())

print("Measurement results (10 000 shots):")
for outcome in ['00', '01', '10', '11']:
    marker = " <- TARGET" if outcome == '11' else ""
    print(f"  '{outcome}' : {all_outcomes[outcome]:5d}  "
          f"({100*all_outcomes[outcome]/total:.1f}%){marker}")
print()
target_prob = 100 * all_outcomes['11'] / total
print(f"Target '11' found with {target_prob:.1f}% probability.")
print()
print("Grover's algorithm concentrates nearly all probability onto the target,")
print("solving the search problem in O(sqrt(N)) quantum steps instead of O(N).")
print()

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

outcomes = list(all_outcomes.keys())
values   = list(all_outcomes.values())
colors   = ['#3498db', '#3498db', '#3498db', '#2ecc71']

bars = axes[0].bar(outcomes, values, color=colors, edgecolor='white',
                   linewidth=1.5, width=0.6)
for bar, val in zip(bars, values):
    if val > 50:
        axes[0].text(bar.get_x() + bar.get_width() / 2,
                     bar.get_height() + 80,
                     f'{val}\n({100*val/total:.1f}%)',
                     ha='center', va='bottom', fontsize=10, fontweight='bold')

axes[0].set_title("Grover's Search - Measurement Counts\nTarget: '11' (2-qubit, 10 000 shots)",
                  fontsize=12, fontweight='bold')
axes[0].set_xlabel('Measurement Outcome (q1 q0)', fontsize=11)
axes[0].set_ylabel('Count', fontsize=11)
axes[0].set_ylim(0, SHOTS * 1.2)
axes[0].grid(axis='y', alpha=0.3)
axes[0].spines['top'].set_visible(False)
axes[0].spines['right'].set_visible(False)

checks = [1, 2, 3, 4]
classical_prob_per_check = [25, 50, 75, 100]
axes[1].plot(checks, classical_prob_per_check, 'o-', color='#e74c3c',
             linewidth=2, markersize=8, label='Classical (sequential)')
axes[1].axhline(target_prob, color='#2ecc71', linestyle='--', linewidth=2.5,
                label=f"Grover's (1 step) approx {target_prob:.0f}%")
axes[1].scatter([1], [target_prob], color='#2ecc71', s=120, zorder=5)
axes[1].set_title('Quantum Speedup\nClassical vs Grover Search',
                  fontsize=12, fontweight='bold')
axes[1].set_xlabel('Number of Oracle Queries', fontsize=11)
axes[1].set_ylabel('Probability of Finding Target (%)', fontsize=11)
axes[1].set_xticks(checks)
axes[1].set_xlim(0.5, 4.5)
axes[1].set_ylim(0, 110)
axes[1].legend(fontsize=10)
axes[1].grid(alpha=0.3)
axes[1].spines['top'].set_visible(False)
axes[1].spines['right'].set_visible(False)

plt.suptitle("Grover's Quantum Search Algorithm - 2 Qubits, Target '11'",
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
out_path = os.path.join(charts_dir, '04_grovers_search.png')
plt.savefig(out_path, dpi=150, bbox_inches='tight')
plt.close()

print(f"Chart saved to: {out_path}")
print()
print("Conclusion: One Grover iteration achieves what classically needs up to 4")
print("checks -- demonstrating a genuine quantum algorithmic speedup.")
