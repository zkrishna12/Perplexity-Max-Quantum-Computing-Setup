#!/usr/bin/env python3
"""
AI + Quantum Experiment 1: Quantum-Enhanced Fruit Classifier
=============================================================
Uses a quantum circuit as a feature map to transform classical data
into quantum-enhanced features, then feeds them to a classical SVM.

Architecture:
  Fruit Features (4) → Quantum Circuit → Quantum Features (16) → SVM → Classification

What You'll Learn:
  - How quantum feature maps work (data encoding via rotations)
  - How entanglement creates feature correlations impossible classically
  - How to combine quantum computing with classical ML (scikit-learn)

Requirements: pyqpanda3, scikit-learn, matplotlib, numpy
Run: python 13_quantum_fruit_classifier.py
"""
from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, RY, RZ, CNOT, measure
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math

print("=" * 65)
print("  AI + QUANTUM EXP 1: Quantum-Enhanced Fruit Classifier")
print("  (Quantum Feature Map + Classical SVM)")
print("=" * 65)
print()

# ============================================================
# STEP 1: Create Fruit Dataset
# ============================================================
# Features: [weight_grams, sweetness(1-10), diameter_cm, texture(1-10)]
# Labels: 0=Apple, 1=Orange, 2=Banana

np.random.seed(42)
n_per_class = 50

apples = np.column_stack([
    np.random.normal(180, 20, n_per_class),   # weight
    np.random.normal(6, 1, n_per_class),      # sweetness
    np.random.normal(7.5, 0.5, n_per_class),  # diameter
    np.random.normal(3, 0.5, n_per_class),    # texture (smooth)
])

oranges = np.column_stack([
    np.random.normal(200, 25, n_per_class),
    np.random.normal(4, 1, n_per_class),
    np.random.normal(8, 0.5, n_per_class),
    np.random.normal(8, 0.5, n_per_class),    # texture (rough)
])

bananas = np.column_stack([
    np.random.normal(120, 15, n_per_class),
    np.random.normal(8, 1, n_per_class),
    np.random.normal(4, 0.8, n_per_class),    # "diameter" (thin)
    np.random.normal(2, 0.5, n_per_class),
])

X = np.vstack([apples, oranges, bananas])
y = np.array([0]*n_per_class + [1]*n_per_class + [2]*n_per_class)
fruit_names = ['Apple', 'Orange', 'Banana']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"Dataset: {len(X)} fruits, {X.shape[1]} features each")
print(f"Classes: {n_per_class} Apples, {n_per_class} Oranges, {n_per_class} Bananas")
print()

# ============================================================
# STEP 2: Quantum Feature Map
# ============================================================
def quantum_feature_map(features, shots=2000):
    """
    Transform classical features through a quantum circuit.
    
    Process:
    1. Put each qubit in superposition (H gate)
    2. Encode features as rotation angles (RY gate)
    3. Entangle qubits (CNOT gates) — creates quantum correlations
    4. Second encoding round for deeper feature extraction
    5. Measure — probabilities become new features
    
    Input:  4 classical features
    Output: 16 quantum features (probabilities of 4-qubit outcomes)
    """
    n_qubits = 4
    circuit = QCircuit()
    
    # Layer 1: Superposition + feature encoding
    for i in range(n_qubits):
        angle = float(features[i % len(features)]) * math.pi
        circuit << H(i)
        circuit << RY(i, angle)
    
    # Layer 2: Entanglement (quantum correlations between features)
    for i in range(n_qubits - 1):
        circuit << CNOT(i, i + 1)
    
    # Layer 3: Second encoding (deeper feature extraction)
    for i in range(n_qubits):
        angle2 = float(features[i % len(features)]) * math.pi * 0.5
        circuit << RZ(i, angle2)
        circuit << RY(i, angle2 * 0.7)
    
    # Layer 4: Cross-entanglement
    circuit << CNOT(0, 2)
    circuit << CNOT(1, 3)
    
    # Measure all qubits
    prog = QProg() << circuit
    for i in range(n_qubits):
        prog << measure(i, i)
    
    qvm = CPUQVM()
    qvm.run(prog, shots)
    counts = qvm.result().get_counts()
    
    # Convert to probability vector (16 quantum features)
    quantum_features = []
    for bits in range(2**n_qubits):
        key = format(bits, f'0{n_qubits}b')
        prob = counts.get(key, 0) / shots
        quantum_features.append(prob)
    
    return np.array(quantum_features)

print("Encoding fruits through quantum circuit...")
print("(4 classical features -> 16 quantum features per fruit)")
print()

X_quantum = []
for i, fruit in enumerate(X_scaled):
    qf = quantum_feature_map(fruit)
    X_quantum.append(qf)
    if (i + 1) % 30 == 0:
        print(f"  Encoded {i+1}/{len(X_scaled)} fruits...")

X_quantum = np.array(X_quantum)
print(f"  Done! Shape: {X_scaled.shape} -> {X_quantum.shape}")
print()

# ============================================================
# STEP 3: Classical SVM vs Quantum-Enhanced SVM
# ============================================================
X_train_c, X_test_c, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42, stratify=y
)
X_train_q, X_test_q, _, _ = train_test_split(
    X_quantum, y, test_size=0.3, random_state=42, stratify=y
)

print("Training Classical SVM (plain features)...")
svm_classical = SVC(kernel='rbf', random_state=42)
svm_classical.fit(X_train_c, y_train)
y_pred_classical = svm_classical.predict(X_test_c)
acc_classical = accuracy_score(y_test, y_pred_classical)
print(f"  Classical SVM Accuracy: {acc_classical:.1%}")
print()

print("Training Quantum-Enhanced SVM (quantum features)...")
svm_quantum = SVC(kernel='rbf', random_state=42)
svm_quantum.fit(X_train_q, y_train)
y_pred_quantum = svm_quantum.predict(X_test_q)
acc_quantum = accuracy_score(y_test, y_pred_quantum)
print(f"  Quantum SVM Accuracy:   {acc_quantum:.1%}")
print()

# Cross-validation
print("Cross-validation comparison (5-fold):")
cv_classical = cross_val_score(SVC(kernel='rbf'), X_scaled, y, cv=5)
cv_quantum = cross_val_score(SVC(kernel='rbf'), X_quantum, y, cv=5)
print(f"  Classical: {cv_classical.mean():.1%} (+/-{cv_classical.std():.1%})")
print(f"  Quantum:   {cv_quantum.mean():.1%} (+/-{cv_quantum.std():.1%})")
print()

print("Detailed Results:")
print(classification_report(y_test, y_pred_classical, target_names=fruit_names))
print(classification_report(y_test, y_pred_quantum, target_names=fruit_names))

# ============================================================
# STEP 4: Visualization
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 12))
fig.suptitle("AI + Quantum: Fruit Classifier\n(Quantum Feature Map + Classical SVM)", 
             fontsize=16, fontweight='bold')

ax1 = axes[0][0]
for i, name in enumerate(fruit_names):
    mask = y == i
    ax1.scatter(X_scaled[mask, 0], X_scaled[mask, 3], alpha=0.6, s=50, label=name)
ax1.set_title("Classical Features (Weight vs Texture)", fontsize=13, fontweight='bold')
ax1.set_xlabel("Weight (normalized)")
ax1.set_ylabel("Texture (normalized)")
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2 = axes[0][1]
for i, name in enumerate(fruit_names):
    mask = y == i
    ax2.scatter(X_quantum[mask, 0], X_quantum[mask, 3], alpha=0.6, s=50, label=name)
ax2.set_title("Quantum Features (After Quantum Transform)", fontsize=13, fontweight='bold', color='#9b59b6')
ax2.set_xlabel("Quantum Feature 0")
ax2.set_ylabel("Quantum Feature 3")
ax2.legend()
ax2.grid(True, alpha=0.3)

ax3 = axes[1][0]
bars = ax3.bar(['Classical\nSVM', 'Quantum-Enhanced\nSVM'], 
               [acc_classical * 100, acc_quantum * 100],
               color=['#3498db', '#9b59b6'], edgecolor='black', linewidth=0.5, width=0.5)
for bar, val in zip(bars, [acc_classical, acc_quantum]):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
             f'{val:.1%}', ha='center', fontweight='bold', fontsize=14)
ax3.set_title("Accuracy Comparison", fontsize=13, fontweight='bold')
ax3.set_ylabel("Accuracy (%)")
ax3.set_ylim(0, 110)

ax4 = axes[1][1]
q_means = np.zeros((3, 16))
for i in range(3):
    q_means[i] = X_quantum[y == i].mean(axis=0)
im = ax4.imshow(q_means, aspect='auto', cmap='viridis')
ax4.set_title("Quantum Feature Fingerprint Per Fruit", fontsize=13, fontweight='bold', color='#9b59b6')
ax4.set_xlabel("Quantum Feature Index (0-15)")
ax4.set_ylabel("Fruit Type")
ax4.set_yticks([0, 1, 2])
ax4.set_yticklabels(fruit_names)
plt.colorbar(im, ax=ax4, label='Probability')

plt.tight_layout()
plt.savefig('charts/13_quantum_fruit_classifier.png', dpi=150, bbox_inches='tight')
print("\nChart saved: charts/13_quantum_fruit_classifier.png")
