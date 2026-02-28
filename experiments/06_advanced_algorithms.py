"""
Advanced Quantum Algorithms Showcase
======================================
This file demonstrates four foundational quantum algorithms on a single canvas:

1. DEUTSCH-JOZSA (2 qubits) - determines if a function is constant or balanced
2. QUANTUM FOURIER TRANSFORM (3 qubits) - core subroutine in Shor's algorithm
3. VQE -- VARIATIONAL QUANTUM EIGENSOLVER - finds ground-state energy of molecules
4. NOISE SIMULATION - shows how fidelity degrades with depolarising errors
"""

import os
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from pyqpanda3.core import (QCircuit, QProg, CPUQVM, H, X, Z, CNOT, CZ,
                            RY, RZ, measure,
                            VQCircuit, Param, Hamiltonian,
                            NoiseModel, depolarizing_error)

# -- Output directory --
charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'charts')
os.makedirs(charts_dir, exist_ok=True)

print("=" * 60)
print("  EXPERIMENT 06 - Advanced Quantum Algorithms")
print("=" * 60)
print()

# 1. DEUTSCH-JOZSA
print("--- 1. Deutsch-Jozsa Algorithm ---")
print("Testing balanced oracle: f(x)=1 only when x='11'")

circuit_dj = QCircuit()
circuit_dj << X(2) << H(0) << H(1) << H(2)
circuit_dj << CNOT(0, 2) << CNOT(1, 2)
circuit_dj << H(0) << H(1)

prog_dj = QProg()
prog_dj << circuit_dj << measure(0, 0) << measure(1, 1)

qvm = CPUQVM()
qvm.run(prog_dj, shots=1000)
dj_counts = qvm.result().get_counts()

is_balanced = any(k != '00' for k in dj_counts if dj_counts[k] > 10)
print(f"  Measurement result: {dict(dj_counts)}")
print(f"  Verdict: {'BALANCED' if is_balanced else 'CONSTANT'} (expected: BALANCED)")
print()

# 2. QUANTUM FOURIER TRANSFORM (3 qubits)
print("--- 2. Quantum Fourier Transform (3 qubits) ---")

def controlled_phase(circuit, control, target, k):
    angle = 2 * math.pi / (2 ** k)
    circuit << RZ(target, angle / 2)
    circuit << CNOT(control, target)
    circuit << RZ(target, -angle / 2)
    circuit << CNOT(control, target)
    circuit << RZ(control, angle / 2)

def swap_bits(circuit, a, b):
    circuit << CNOT(a, b) << CNOT(b, a) << CNOT(a, b)

circuit_qft = QCircuit()
circuit_qft << X(0) << X(2)
circuit_qft << H(0)
controlled_phase(circuit_qft, 1, 0, 2)
controlled_phase(circuit_qft, 2, 0, 3)
circuit_qft << H(1)
controlled_phase(circuit_qft, 2, 1, 2)
circuit_qft << H(2)
swap_bits(circuit_qft, 0, 2)

prog_qft = QProg()
prog_qft << circuit_qft
for i in range(3):
    prog_qft << measure(i, i)

qvm2 = CPUQVM()
qvm2.run(prog_qft, shots=8000)
qft_counts = qvm2.result().get_counts()

all_qft = {f'{i:03b}': 0 for i in range(8)}
all_qft.update(qft_counts)

print(f"  Input: |101> -> QFT output distribution:")
for k, v in sorted(all_qft.items()):
    print(f"    |{k}> : {v:5d}  ({100*v/8000:.1f}%)")
print()

# 3. VQE
print("--- 3. VQE Demo - Minimising <Z0> ---")
print("  Sweeping RY angle theta from 0 to 2*pi...")

hamiltonian = Hamiltonian({"Z0": 1.0 + 0j})
angles = np.linspace(0, 2 * np.pi, 50)
expectations = []

for theta in angles:
    vc = VQCircuit()
    vc << RY(0, Param([0]))
    vc.set_Param([theta])
    _, exp_val = vc.get_gradients_and_expectation(hamiltonian, 1000)
    expectations.append(float(np.real(exp_val)))

min_exp = min(expectations)
min_angle = angles[expectations.index(min_exp)]
print(f"  Minimum expectation: {min_exp:.4f} at theta = {min_angle:.4f} rad")
print(f"  (Theory: minimum is -1.0 at theta = pi = {math.pi:.4f})")
print()

# 4. NOISE SIMULATION
print("--- 4. Noise Simulation - Bell State Fidelity ---")

noise_levels = [0.0, 0.01, 0.02, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
fidelities = []

circuit_bell = QCircuit()
circuit_bell << H(0) << CNOT(0, 1)
prog_bell = QProg()
prog_bell << circuit_bell << measure(0, 0) << measure(1, 1)

for p in noise_levels:
    qvm_n = CPUQVM()
    if p > 0:
        noise = NoiseModel()
        noise.add(depolarizing_error(p))
        qvm_n.run(prog_bell, 5000, noise)
    else:
        qvm_n.run(prog_bell, shots=5000)
    c = qvm_n.result().get_counts()
    total = sum(c.values())
    corr = c.get('00', 0) + c.get('11', 0)
    fidelity = corr / total
    fidelities.append(fidelity)
    print(f"  Noise p={p:.2f}: fidelity = {fidelity:.4f}")

print()

# PLOT - 4 subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

ax = axes[0, 0]
dj_all = {'00': 0, '01': 0, '10': 0, '11': 0}
dj_all.update(dj_counts)
dj_colors = ['#e74c3c' if k == '00' else '#2ecc71' for k in dj_all]
bars = ax.bar(dj_all.keys(), dj_all.values(), color=dj_colors,
              edgecolor='white', linewidth=1.5, width=0.6)
for bar, (k, v) in zip(bars, dj_all.items()):
    if v > 0:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                f'{v}', ha='center', va='bottom', fontsize=11, fontweight='bold')
ax.set_title('Deutsch-Jozsa Algorithm\n(Balanced oracle, 2-qubit input)',
             fontsize=11, fontweight='bold')
ax.set_xlabel('Measurement (q1 q0)', fontsize=10)
ax.set_ylabel('Count (1000 shots)', fontsize=10)
ax.set_ylim(0, 1100)
from matplotlib.patches import Patch
legend_elements = [Patch(color='#e74c3c', label='Constant -> |00>'),
                   Patch(color='#2ecc71', label='Balanced -> not |00>')]
ax.legend(handles=legend_elements, fontsize=9)
ax.grid(axis='y', alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax = axes[0, 1]
qft_states = sorted(all_qft.keys())
qft_vals   = [all_qft[k] for k in qft_states]
ax.bar(qft_states, qft_vals, color='#9b59b6', edgecolor='white', linewidth=1.5, width=0.6)
ax.set_title('Quantum Fourier Transform (3 qubits)\nInput: |101>',
             fontsize=11, fontweight='bold')
ax.set_xlabel('Output State', fontsize=10)
ax.set_ylabel('Count (8000 shots)', fontsize=10)
ax.grid(axis='y', alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax = axes[1, 0]
ax.plot(angles, expectations, color='#3498db', linewidth=2.2, label='<Z0> expectation')
ax.axhline(-1, color='#2ecc71', linestyle='--', linewidth=1.5, label='Ground state (-1)')
ax.axvline(min_angle, color='#e74c3c', linestyle=':', linewidth=1.5,
           label=f'Min at theta = {min_angle:.2f}')
ax.scatter([min_angle], [min_exp], color='#e74c3c', s=80, zorder=5)
ax.set_title('VQE - Expectation of Z0\nvs RY rotation angle theta',
             fontsize=11, fontweight='bold')
ax.set_xlabel('theta (radians)', fontsize=10)
ax.set_ylabel('<Z0> Expectation Value', fontsize=10)
ax.set_xticks([0, math.pi/2, math.pi, 3*math.pi/2, 2*math.pi])
ax.set_xticklabels(['0', 'pi/2', 'pi', '3pi/2', '2pi'])
ax.legend(fontsize=9)
ax.grid(alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax = axes[1, 1]
ax.plot([p * 100 for p in noise_levels], [f * 100 for f in fidelities],
        'o-', color='#f39c12', linewidth=2.2, markersize=7)
ax.axhline(100, color='#2ecc71', linestyle='--', linewidth=1.5, label='Ideal (100%)')
ax.fill_between([p * 100 for p in noise_levels],
                [f * 100 for f in fidelities],
                100, alpha=0.15, color='#e74c3c', label='Fidelity loss')
ax.set_title('Noise Simulation - Bell State Fidelity\nvs Depolarising Error Rate',
             fontsize=11, fontweight='bold')
ax.set_xlabel('Depolarising Error Rate (%)', fontsize=10)
ax.set_ylabel('Bell State Fidelity (%)', fontsize=10)
ax.set_ylim(0, 110)
ax.legend(fontsize=9)
ax.grid(alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.suptitle('Advanced Quantum Algorithms - Deutsch-Jozsa | QFT | VQE | Noise',
             fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
out_path = os.path.join(charts_dir, '06_advanced_algorithms.png')
plt.savefig(out_path, dpi=150, bbox_inches='tight')
plt.close()

print(f"Chart saved to: {out_path}")
print()
print("All four advanced algorithms demonstrated successfully.")
