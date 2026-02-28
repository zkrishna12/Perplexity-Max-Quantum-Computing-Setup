"""
Quantum Entanglement - Bell State
==================================
Quantum entanglement is one of the most striking features of quantum mechanics.
When two qubits are entangled, measuring one instantly determines the state of
the other -- no matter how far apart they are. Einstein called this "spooky
action at a distance."

This experiment creates the simplest entangled pair: the Bell state |Phi+>.
  Step 1 - H gate on qubit 0: puts it in superposition (50% chance of 0 or 1).
  Step 2 - CNOT(0->1): flips qubit 1 whenever qubit 0 is 1.

Result: qubits are perfectly correlated. You only ever see '00' or '11',
never '01' or '10'. The two qubits always agree, even though individually
each is in a random state.

What this experiment does:
  1. Builds the Bell state circuit (H + CNOT).
  2. Measures both qubits 10 000 times.
  3. Shows that only '00' and '11' appear with ~50% probability each.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, CNOT, measure

# -- Output directory --
charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'charts')
os.makedirs(charts_dir, exist_ok=True)

# -- Build the Bell state circuit --
print("=" * 60)
print("  EXPERIMENT 02 - Quantum Entanglement (Bell State)")
print("=" * 60)
print()
print("Circuit: H(0) -> CNOT(0,1)")
print("This creates the maximally entangled Bell state |Phi+>.")
print("Running 10 000 shots...")
print()

circuit = QCircuit()
circuit << H(0) << CNOT(0, 1)          # Bell pair

prog = QProg()
prog << circuit << measure(0, 0) << measure(1, 1)

qvm = CPUQVM()
qvm.run(prog, shots=10000)
counts = qvm.result().get_counts()

all_outcomes = {'00': 0, '01': 0, '10': 0, '11': 0}
all_outcomes.update(counts)
total = sum(all_outcomes.values())

print("Measurement results (10 000 shots):")
print(f"  '00'  (both |0>) : {all_outcomes['00']:5d}  ({100*all_outcomes['00']/total:.1f}%)")
print(f"  '01'  (mixed)    : {all_outcomes['01']:5d}  ({100*all_outcomes['01']/total:.1f}%)")
print(f"  '10'  (mixed)    : {all_outcomes['10']:5d}  ({100*all_outcomes['10']/total:.1f}%)")
print(f"  '11'  (both |1>) : {all_outcomes['11']:5d}  ({100*all_outcomes['11']/total:.1f}%)")
print()
print("Entanglement proof: '01' and '10' are essentially absent.")
print("The qubits always agree -- measuring one tells you the other instantly.")
print()

# -- Plot --
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

outcomes = list(all_outcomes.keys())
values   = list(all_outcomes.values())
colors   = ['#3498db', '#e74c3c', '#e74c3c', '#2ecc71']

bars = axes[0].bar(outcomes, values, color=colors, edgecolor='white',
                   linewidth=1.5, width=0.6)
for bar, val in zip(bars, values):
    if val > 0:
        axes[0].text(bar.get_x() + bar.get_width() / 2,
                     bar.get_height() + 60,
                     f'{val}\n({100*val/total:.1f}%)',
                     ha='center', va='bottom', fontsize=10, fontweight='bold')

axes[0].set_title('Bell State Measurement Counts\n(10 000 shots)',
                  fontsize=13, fontweight='bold')
axes[0].set_ylabel('Count', fontsize=11)
axes[0].set_xlabel('Measurement Outcome (q1 q0)', fontsize=11)
axes[0].set_ylim(0, max(values) * 1.3)
axes[0].axhline(5000, color='#f39c12', linestyle='--', linewidth=1.5,
                label='Expected 50%')
axes[0].legend(fontsize=10)
axes[0].grid(axis='y', alpha=0.3)
axes[0].spines['top'].set_visible(False)
axes[0].spines['right'].set_visible(False)

entangled = all_outcomes['00'] + all_outcomes['11']
unentangled = all_outcomes['01'] + all_outcomes['10']
pie_colors = ['#2ecc71', '#e74c3c']
wedges, texts, autotexts = axes[1].pie(
    [entangled, unentangled],
    labels=['Correlated\n(|00> + |11>)', 'Uncorrelated\n(|01> + |10>)'],
    colors=pie_colors,
    autopct='%1.1f%%',
    startangle=90,
    textprops={'fontsize': 11},
    wedgeprops={'edgecolor': 'white', 'linewidth': 2}
)
for at in autotexts:
    at.set_fontweight('bold')
    at.set_fontsize(12)
axes[1].set_title('Entanglement Quality\n(Correlated vs Uncorrelated outcomes)',
                  fontsize=13, fontweight='bold')

plt.suptitle('Quantum Entanglement - Bell State |Phi+>', fontsize=15,
             fontweight='bold', y=1.02)
plt.tight_layout()
out_path = os.path.join(charts_dir, '02_entanglement.png')
plt.savefig(out_path, dpi=150, bbox_inches='tight')
plt.close()

print(f"Chart saved to: {out_path}")
print()
print("Conclusion: ~100% of measurements show correlated outcomes ('00' or '11'),")
print("confirming perfect quantum entanglement. The two qubits behave as one.")
