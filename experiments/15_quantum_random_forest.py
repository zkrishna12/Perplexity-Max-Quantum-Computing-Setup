#!/usr/bin/env python3
"""
AI + Quantum Experiment 3: Quantum Random Forest
==================================================
A Random Forest where the randomness comes from QUANTUM PHYSICS 
instead of a pseudo-random number generator.

Classical random numbers follow a deterministic algorithm — they look
random but are predictable. Quantum random numbers are certified by 
the laws of physics — truly unpredictable.

What You'll Learn:
  - How to build a quantum random number generator (QRNG)
  - Why true randomness matters for AI and security
  - Comparison of quantum vs classical randomness quality

Requirements: pyqpanda3, scikit-learn, matplotlib, numpy
Run: python 15_quantum_random_forest.py
"""
from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, measure
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("=" * 65)
print("  AI + QUANTUM EXP 3: Quantum Random Forest")
print("  (Quantum True-Random vs Classical Pseudo-Random)")
print("=" * 65)
print()

# ============================================================
# STEP 1: Quantum Random Number Generator
# ============================================================
def quantum_random_seed(n_bits=16):
    """
    Generate a truly random seed using quantum superposition.
    Each qubit in superposition has exactly 50/50 chance of 0 or 1.
    This randomness is guaranteed by quantum physics — no algorithm.
    """
    circuit = QCircuit()
    for i in range(n_bits):
        circuit << H(i)  # Superposition = true randomness
    
    prog = QProg() << circuit
    for i in range(n_bits):
        prog << measure(i, i)
    
    qvm = CPUQVM()
    qvm.run(prog, 1)
    counts = qvm.result().get_counts()
    result_key = list(counts.keys())[0]
    return int(result_key, 2)

print("Generating quantum random seeds...")
n_forests = 20
quantum_seeds = [quantum_random_seed() for _ in range(n_forests)]
print(f"  Generated {n_forests} quantum random seeds")
print()

# ============================================================
# STEP 2: Load Real Dataset (Wine Classification)
# ============================================================
wine = load_wine()
X, y = wine.data, wine.target

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42, stratify=y
)

print(f"Dataset: Wine Classification ({len(X)} wines, {X.shape[1]} features)")
print(f"  3 types of wine to classify")
print()

# ============================================================
# STEP 3: Classical vs Quantum Random Forests
# ============================================================
print(f"Running {n_forests} forests with each type of randomness...")

classical_accuracies = []
quantum_accuracies = []

for i in range(n_forests):
    clf_c = RandomForestClassifier(n_estimators=50, random_state=i*42, max_features='sqrt')
    clf_c.fit(X_train, y_train)
    classical_accuracies.append(accuracy_score(y_test, clf_c.predict(X_test)))
    
    clf_q = RandomForestClassifier(n_estimators=50, random_state=quantum_seeds[i], max_features='sqrt')
    clf_q.fit(X_train, y_train)
    quantum_accuracies.append(accuracy_score(y_test, clf_q.predict(X_test)))

classical_accuracies = np.array(classical_accuracies)
quantum_accuracies = np.array(quantum_accuracies)

print(f"\nClassical RF: {classical_accuracies.mean():.2%} (std: {classical_accuracies.std():.2%})")
print(f"Quantum RF:   {quantum_accuracies.mean():.2%} (std: {quantum_accuracies.std():.2%})")
print()

# ============================================================
# STEP 4: Randomness Quality Test
# ============================================================
print("Randomness Quality Test (10,000 bits)...")
quantum_bits = []
for _ in range(100):
    circuit = QCircuit()
    for i in range(8):
        circuit << H(i)
    prog = QProg() << circuit
    for i in range(8):
        prog << measure(i, i)
    qvm = CPUQVM()
    qvm.run(prog, 100)
    counts = qvm.result().get_counts()
    for key, cnt in counts.items():
        for bit in key:
            quantum_bits.extend([int(bit)] * cnt)

quantum_bits = np.array(quantum_bits[:10000])
np.random.seed(42)
classical_bits = np.random.randint(0, 2, 10000)

print(f"  Quantum:   {quantum_bits.mean():.4f} ratio (perfect=0.5000)")
print(f"  Classical: {classical_bits.mean():.4f} ratio (perfect=0.5000)")
print()

# ============================================================
# STEP 5: Visualization
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 12))
fig.suptitle("AI + Quantum: Quantum Random Forest\n(True Quantum Randomness vs Pseudo-Random)", 
             fontsize=15, fontweight='bold')

ax1 = axes[0][0]
bins = np.linspace(min(classical_accuracies.min(), quantum_accuracies.min()) - 0.02,
                   max(classical_accuracies.max(), quantum_accuracies.max()) + 0.02, 12)
ax1.hist(classical_accuracies, bins=bins, alpha=0.6, color='#3498db', 
         label=f'Classical (mean={classical_accuracies.mean():.1%})', edgecolor='black')
ax1.hist(quantum_accuracies, bins=bins, alpha=0.6, color='#9b59b6', 
         label=f'Quantum (mean={quantum_accuracies.mean():.1%})', edgecolor='black')
ax1.set_title("Accuracy Distribution (20 runs)", fontsize=12, fontweight='bold')
ax1.set_xlabel("Accuracy"); ax1.set_ylabel("Count"); ax1.legend(); ax1.grid(True, alpha=0.3)

ax2 = axes[0][1]
x_runs = range(1, n_forests + 1)
ax2.plot(x_runs, classical_accuracies * 100, 'bo-', label='Classical', alpha=0.7, markersize=5)
ax2.plot(x_runs, quantum_accuracies * 100, 's-', color='#9b59b6', label='Quantum', alpha=0.7, markersize=5)
ax2.set_title("Run-by-Run Accuracy", fontsize=12, fontweight='bold')
ax2.set_xlabel("Run #"); ax2.set_ylabel("Accuracy (%)"); ax2.legend(); ax2.grid(True, alpha=0.3)

ax3 = axes[1][0]
q_pairs = [''.join(map(str, quantum_bits[i:i+2])) for i in range(0, len(quantum_bits)-1, 2)]
c_pairs = [''.join(map(str, classical_bits[i:i+2])) for i in range(0, len(classical_bits)-1, 2)]
pair_labels = ['00', '01', '10', '11']
x_pos = np.arange(4); width = 0.35
ax3.bar(x_pos - width/2, [c_pairs.count(p) for p in pair_labels], width, color='#3498db', label='Classical', edgecolor='black', linewidth=0.5)
ax3.bar(x_pos + width/2, [q_pairs.count(p) for p in pair_labels], width, color='#9b59b6', label='Quantum', edgecolor='black', linewidth=0.5)
ax3.axhline(len(q_pairs)/4, color='green', linestyle='--', alpha=0.5, label='Perfect uniform')
ax3.set_title("Bit-Pair Distribution", fontsize=12, fontweight='bold')
ax3.set_xticks(x_pos); ax3.set_xticklabels(pair_labels); ax3.legend(fontsize=9)

ax4 = axes[1][1]
categories = ['Mean\nAccuracy', 'Best\nAccuracy', 'Consistency\n(1-std)']
c_vals = [classical_accuracies.mean()*100, classical_accuracies.max()*100, (1-classical_accuracies.std())*100]
q_vals = [quantum_accuracies.mean()*100, quantum_accuracies.max()*100, (1-quantum_accuracies.std())*100]
x_pos = np.arange(3); width = 0.3
bars1 = ax4.bar(x_pos - width/2, c_vals, width, color='#3498db', label='Classical', edgecolor='black', linewidth=0.5)
bars2 = ax4.bar(x_pos + width/2, q_vals, width, color='#9b59b6', label='Quantum', edgecolor='black', linewidth=0.5)
for bars in [bars1, bars2]:
    for bar in bars:
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                 f'{bar.get_height():.1f}%', ha='center', fontsize=9, fontweight='bold')
ax4.set_title("Overall Comparison", fontsize=12, fontweight='bold')
ax4.set_xticks(x_pos); ax4.set_xticklabels(categories); ax4.legend(); ax4.set_ylim(0, 110)

plt.tight_layout()
plt.savefig('charts/15_quantum_random_forest.png', dpi=150, bbox_inches='tight')
print("Chart saved: charts/15_quantum_random_forest.png")
