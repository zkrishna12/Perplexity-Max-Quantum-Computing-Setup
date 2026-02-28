#!/usr/bin/env python3
"""
AI + Quantum Experiment 4: Quantum vs Classical AI Showdown
============================================================
5 AI algorithms compete on the same hard dataset:
  1. Logistic Regression (simple linear)
  2. Random Forest (ensemble)
  3. Neural Network (deep learning)
  4. Classical SVM (kernel trick)
  5. Quantum-Enhanced SVM (quantum feature map + SVM)

Dataset is designed with circular/angular patterns where quantum 
rotational gates should have a natural advantage.

What You'll Learn:
  - How different AI algorithms compare on the same problem
  - Where quantum feature maps help vs. hurt
  - Why quantum advantage depends on circuit design
  - Cross-validation for robust comparison

Requirements: pyqpanda3, scikit-learn, matplotlib, numpy
Run: python 16_quantum_vs_classical_showdown.py
"""
from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, RY, RZ, CNOT, measure
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import time

print("=" * 65)
print("  AI + QUANTUM EXP 4: Quantum vs Classical Showdown!")
print("  (5 Algorithms, 1 Hard Dataset, Who Wins?)")
print("=" * 65)
print()

# ============================================================
# STEP 1: Create Angular Pattern Dataset
# ============================================================
np.random.seed(42)
n_samples = 300
theta = np.random.uniform(0, 2*np.pi, n_samples)
r = np.random.uniform(0.5, 2.0, n_samples)
class_boundary = np.sin(2*theta) * np.cos(theta) + 0.3 * np.sin(3*theta)
y = (r > 1.0 + 0.4 * class_boundary).astype(int)

X = np.column_stack([
    r * np.cos(theta), r * np.sin(theta),
    np.sin(theta) * r, np.cos(2*theta) * r**0.5,
])
X += np.random.normal(0, 0.1, X.shape)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42, stratify=y
)

print(f"Dataset: {n_samples} points with circular angular patterns")
print(f"  Class 0: {sum(y==0)} | Class 1: {sum(y==1)}")
print()

# ============================================================
# STEP 2: Quantum Feature Map
# ============================================================
def quantum_feature_map(features, shots=1000):
    n_qubits = 4
    circuit = QCircuit()
    for i in range(n_qubits):
        circuit << H(i)
        circuit << RY(i, float(features[i]) * math.pi)
    for i in range(n_qubits - 1):
        circuit << CNOT(i, i + 1)
    circuit << CNOT(n_qubits - 1, 0)
    for i in range(n_qubits):
        j = (i + 1) % n_qubits
        circuit << RZ(i, float(features[i] * features[j]) * math.pi)
    for i in range(0, n_qubits - 1, 2):
        circuit << CNOT(i, i + 1)
    
    prog = QProg() << circuit
    for i in range(n_qubits):
        prog << measure(i, i)
    qvm = CPUQVM()
    qvm.run(prog, shots)
    counts = qvm.result().get_counts()
    
    return np.array([counts.get(format(b, f'0{n_qubits}b'), 0) / shots for b in range(2**n_qubits)])

print("Encoding data through quantum circuit...")
X_quantum_train = np.array([quantum_feature_map(x) for x in X_train])
X_quantum_test = np.array([quantum_feature_map(x) for x in X_test])
print(f"  Encoded: {X_train.shape} -> {X_quantum_train.shape}")
print()

# ============================================================
# STEP 3: The Showdown
# ============================================================
print("=" * 50)
print("  THE SHOWDOWN!")
print("=" * 50)
print()

results = {}

for name, model, X_tr, X_te, color in [
    ('Logistic\nRegression', LogisticRegression(max_iter=1000, random_state=42), X_train, X_test, '#3498db'),
    ('Random\nForest', RandomForestClassifier(n_estimators=100, random_state=42), X_train, X_test, '#2ecc71'),
    ('Neural\nNetwork', MLPClassifier(hidden_layer_sizes=(64,32), max_iter=500, random_state=42), X_train, X_test, '#e74c3c'),
    ('Classical\nSVM', SVC(kernel='rbf', random_state=42), X_train, X_test, '#f39c12'),
    ('QUANTUM\nSVM', SVC(kernel='rbf', random_state=42), X_quantum_train, X_quantum_test, '#9b59b6'),
]:
    start = time.time()
    model.fit(X_tr, y_train)
    acc = accuracy_score(y_test, model.predict(X_te))
    t = time.time() - start
    results[name] = {'acc': acc, 'time': t, 'color': color}
    print(f"  {name.replace(chr(10), ' ')}: {acc:.1%} ({t:.3f}s)")

winner = max(results, key=lambda k: results[k]['acc'])
print(f"\n  Winner: {winner.replace(chr(10), ' ')} ({results[winner]['acc']:.1%})")
print()

# Cross-validation
print("Cross-validation (5-fold):")
X_quantum_all = np.array([quantum_feature_map(x) for x in X_scaled])
for name, model, data in [
    ('Logistic Regression', LogisticRegression(max_iter=1000, random_state=42), X_scaled),
    ('Random Forest', RandomForestClassifier(n_estimators=100, random_state=42), X_scaled),
    ('Neural Network', MLPClassifier(hidden_layer_sizes=(64,32), max_iter=500, random_state=42), X_scaled),
    ('Classical SVM', SVC(kernel='rbf', random_state=42), X_scaled),
    ('Quantum SVM', SVC(kernel='rbf', random_state=42), X_quantum_all),
]:
    cv = cross_val_score(model, data, y, cv=5)
    print(f"  {name}: {cv.mean():.1%} (+/-{cv.std():.1%})")

# ============================================================
# STEP 4: Visualization
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle("AI + Quantum: The Ultimate Showdown\n5 Algorithms Battle on a Hard Dataset", 
             fontsize=16, fontweight='bold')

ax1 = axes[0][0]
names = list(results.keys())
bars = ax1.bar(names, [results[n]['acc']*100 for n in names], 
               color=[results[n]['color'] for n in names], edgecolor='black', linewidth=0.5, width=0.6)
for bar, n in zip(bars, names):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f'{results[n]["acc"]:.1%}', ha='center', fontweight='bold', fontsize=11)
ax1.set_title("Accuracy Showdown", fontsize=13, fontweight='bold')
ax1.set_ylabel("Accuracy (%)"); ax1.set_ylim(0, 110)

ax2 = axes[0][1]
ax2.scatter(X[y==0, 0], X[y==0, 1], c='#3498db', label='Class 0', alpha=0.5, s=20)
ax2.scatter(X[y==1, 0], X[y==1, 1], c='#e74c3c', label='Class 1', alpha=0.5, s=20)
ax2.set_title("The Dataset (Circular Patterns)", fontsize=13, fontweight='bold')
ax2.legend(); ax2.grid(True, alpha=0.3)

ax3 = axes[1][0]
pca_c = PCA(n_components=2).fit_transform(X_scaled)
pca_q = PCA(n_components=2).fit_transform(X_quantum_all)
ax3.scatter(pca_c[y==0, 0], pca_c[y==0, 1], c='#3498db', alpha=0.3, s=15, marker='o', label='Classical')
ax3.scatter(pca_c[y==1, 0], pca_c[y==1, 1], c='#e74c3c', alpha=0.3, s=15, marker='o')
offset = 5
ax3.scatter(pca_q[y==0, 0]+offset, pca_q[y==0, 1], c='#3498db', alpha=0.3, s=15, marker='^', label='Quantum')
ax3.scatter(pca_q[y==1, 0]+offset, pca_q[y==1, 1], c='#e74c3c', alpha=0.3, s=15, marker='^')
ax3.axvline(offset/2, color='gray', linestyle='--', alpha=0.5)
ax3.set_title("Classical vs Quantum Feature Space (PCA)", fontsize=13, fontweight='bold')
ax3.legend(); ax3.grid(True, alpha=0.3)

ax4 = axes[1][1]
times = [results[n]['time'] for n in names]
ax4.barh(names, times, color=[results[n]['color'] for n in names], edgecolor='black', linewidth=0.5)
ax4.set_title("Speed Comparison", fontsize=13, fontweight='bold')
ax4.set_xlabel("Time (seconds)")

plt.tight_layout()
plt.savefig('charts/16_quantum_vs_classical_showdown.png', dpi=150, bbox_inches='tight')
print("\nChart saved: charts/16_quantum_vs_classical_showdown.png")
