"""
Quantum Password Cracker - Grover's Search on 2 Qubits
========================================================
A 2-bit password has 4 possible values: '00', '01', '10', '11'.
Classical brute force needs up to 4 guesses; on average 2.5.

Grover's algorithm finds the correct password in just 1 iteration with ~100%
probability, demonstrating a quadratic quantum speedup.

For each of the 4 possible passwords, we:
  1. Build a custom quantum oracle that marks the target password with a phase flip.
     The oracle works by:
       a. Flipping qubits that should be 0 (so target becomes |11>).
       b. Applying CZ to flip the phase of |11> only.
       c. Flipping those qubits back (uncompute).
  2. Apply the diffusion operator to amplify the marked state.
  3. Measure -- the target should appear ~100% of the time.

Bit ordering: QPanda3 output "ab" -> cbit1=a, cbit0=b.
So password secret[0] corresponds to q1, secret[1] to q0.

What this experiment does:
  - Runs Grover's algorithm separately for all 4 passwords.
  - Plots a 2x2 grid showing measurement probabilities for each case.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, X, CZ, measure

# -- Output directory --
charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'charts')
os.makedirs(charts_dir, exist_ok=True)

print("=" * 60)
print("  EXPERIMENT 08 - Quantum Password Cracker")
print("=" * 60)
print()
print("2-bit password space: 00, 01, 10, 11")
print("Using Grover's oracle to crack each password in 1 quantum step.")
print()

SHOTS = 10000
ALL_PASSWORDS = ['00', '01', '10', '11']


def build_grover_circuit(secret):
    """
    Build a 2-qubit Grover circuit for a given 2-bit target password.
    Bit ordering (QPanda3): output "ab" -> cbit1=a (q1), cbit0=b (q0).
    So secret[0] is the bit for q1, secret[1] is the bit for q0.
    """
    target_q0 = int(secret[1])   # secret[1] -> qubit 0 (rightmost)
    target_q1 = int(secret[0])   # secret[0] -> qubit 1 (leftmost)

    circuit = QCircuit()

    # Step 1: Initialise in equal superposition
    circuit << H(0) << H(1)

    # Step 2: Oracle -- mark target with phase flip
    if target_q0 == 0:
        circuit << X(0)
    if target_q1 == 0:
        circuit << X(1)
    circuit << CZ(0, 1)           # Phase flip for |11> only
    if target_q0 == 0:
        circuit << X(0)
    if target_q1 == 0:
        circuit << X(1)

    # Step 3: Diffusion operator (amplitude amplification)
    circuit << H(0) << H(1)
    circuit << X(0) << X(1)
    circuit << CZ(0, 1)
    circuit << X(0) << X(1)
    circuit << H(0) << H(1)

    return circuit


# -- Run Grover for each password --
all_results = {}

print(f"{'Password':>10} {'Found?':>8} {'Probability':>13}")
print("-" * 38)

for secret in ALL_PASSWORDS:
    circuit = build_grover_circuit(secret)
    prog = QProg()
    prog << circuit << measure(0, 0) << measure(1, 1)

    qvm = CPUQVM()
    qvm.run(prog, shots=SHOTS)
    counts = qvm.result().get_counts()

    outcomes = {'00': 0, '01': 0, '10': 0, '11': 0}
    outcomes.update(counts)

    target_count = outcomes[secret]
    target_prob  = 100 * target_count / SHOTS
    success      = "YES" if target_prob > 85 else "NO"

    all_results[secret] = outcomes
    print(f"  '{secret}'     {success}    {target_prob:6.1f}%")

print()
print("Grover's search finds every password with ~100% probability in 1 step!")
print()

# -- Plot --
fig, axes = plt.subplots(2, 2, figsize=(12, 9))
axes = axes.flatten()

bar_default = '#3498db'
bar_target  = '#2ecc71'

for i, secret in enumerate(ALL_PASSWORDS):
    ax = axes[i]
    outcomes = all_results[secret]
    labels = list(outcomes.keys())
    values = list(outcomes.values())
    colors = [bar_target if lbl == secret else bar_default for lbl in labels]

    bars = ax.bar(labels, values, color=colors, edgecolor='white',
                  linewidth=1.5, width=0.6)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 50,
                f'{100*val/SHOTS:.1f}%',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    target_pct = 100 * outcomes[secret] / SHOTS
    ax.set_title(f"Password: '{secret}'\nFound with {target_pct:.1f}% confidence",
                 fontsize=12, fontweight='bold')
    ax.set_xlabel('Measurement Outcome (q1 q0)', fontsize=10)
    ax.set_ylabel('Count', fontsize=10)
    ax.set_ylim(0, SHOTS * 1.2)
    ax.grid(axis='y', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    from matplotlib.patches import Patch
    legend_elems = [Patch(color=bar_target, label=f"Target '{secret}'"),
                    Patch(color=bar_default, label='Other outcomes')]
    ax.legend(handles=legend_elems, fontsize=9)

plt.suptitle("Quantum Password Cracker - Grover's Algorithm\n"
             "One quantum query finds the correct 2-bit password ~100% of the time",
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
out_path = os.path.join(charts_dir, '08_password_cracker.png')
plt.savefig(out_path, dpi=150, bbox_inches='tight')
plt.close()

print(f"Chart saved to: {out_path}")
print()
print("Conclusion: Grover's oracle correctly identifies all 4 passwords with")
print("near-100% success rate, demonstrating genuine quantum search advantage.")
