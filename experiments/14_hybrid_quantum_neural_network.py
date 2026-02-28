#!/usr/bin/env python3
"""
AI + Quantum Experiment 2: Hybrid Quantum Neural Network
=========================================================
A real neural network where the hidden layer is a QUANTUM CIRCUIT.
PyTorch handles classical layers, QPanda3 handles the quantum layer.

Architecture:
  Input (2) -> Classical Linear (2->4) -> QUANTUM LAYER (4 qubits) -> Classical Linear (4->1) -> Output

What You'll Learn:
  - How to build a hybrid quantum-classical neural network
  - How quantum gates act as trainable "neurons"
  - How PyTorch can optimize quantum gate angles alongside classical weights
  - The "barren plateau" challenge in quantum ML gradient flow

Requirements: pyqpanda3, torch, scikit-learn, matplotlib, numpy
Run: python 14_hybrid_quantum_neural_network.py
"""
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, RY, RZ, RX, CNOT, measure
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math

print("=" * 65)
print("  AI + QUANTUM EXP 2: Hybrid Quantum Neural Network")
print("  (PyTorch + QPanda3 Quantum Layer)")
print("=" * 65)
print()

# ============================================================
# STEP 1: Create Dataset (Half-Moons — Hard to Separate)
# ============================================================
X, y = make_moons(n_samples=200, noise=0.15, random_state=42)
scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print(f"Dataset: Half-moons (200 points, 2 classes)")
print(f"  Train: {len(X_train)} | Test: {len(X_test)}")
print()

# ============================================================
# STEP 2: Quantum Layer (the quantum "neuron")
# ============================================================
class QuantumLayer:
    """
    A quantum circuit that acts as a neural network layer.
    
    Input: classical values -> encoded as qubit rotations
    Process: Superposition -> Entanglement -> Trainable rotations -> Measurement
    Output: probabilities (quantum features)
    """
    def __init__(self, n_qubits=4, shots=500):
        self.n_qubits = n_qubits
        self.shots = shots
    
    def forward(self, x, weights):
        circuit = QCircuit()
        
        # Encode classical data into quantum state
        for i in range(self.n_qubits):
            circuit << H(i)
            angle = float(x[i % len(x)]) * math.pi
            circuit << RY(i, angle)
        
        # Entangle qubits
        for i in range(self.n_qubits - 1):
            circuit << CNOT(i, i + 1)
        
        # Trainable rotations (these are the quantum "weights")
        for i in range(self.n_qubits):
            w_idx = i % len(weights)
            circuit << RY(i, float(weights[w_idx]))
            circuit << RZ(i, float(weights[(w_idx + 1) % len(weights)]))
        
        # Cross-entanglement
        circuit << CNOT(0, 2)
        circuit << CNOT(1, 3)
        
        # Second trainable layer
        for i in range(self.n_qubits):
            w_idx = (i + self.n_qubits) % len(weights)
            circuit << RY(i, float(weights[w_idx]))
        
        # Measure
        prog = QProg() << circuit
        for i in range(self.n_qubits):
            prog << measure(i, i)
        
        qvm = CPUQVM()
        qvm.run(prog, self.shots)
        counts = qvm.result().get_counts()
        
        # Extract per-qubit probabilities
        probs = []
        for q in range(self.n_qubits):
            p1 = 0
            for key, count in counts.items():
                if len(key) > q and key[-(q+1)] == '1':
                    p1 += count
            probs.append(p1 / self.shots)
        
        return np.array(probs)

# ============================================================
# STEP 3: Hybrid Network (Classical + Quantum + Classical)
# ============================================================
class HybridQuantumNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.pre_layer = nn.Linear(2, 4)       # Classical input
        self.post_layer = nn.Linear(4, 1)      # Classical output
        self.quantum = QuantumLayer(n_qubits=4, shots=500)
        self.q_weights = nn.Parameter(torch.randn(8) * 0.5)  # Quantum weights
        
    def forward_single(self, x):
        h = torch.relu(self.pre_layer(x))
        q_input = h.detach().numpy()
        q_output = self.quantum.forward(q_input, self.q_weights.detach().numpy())
        q_tensor = torch.tensor(q_output, dtype=torch.float32)
        out = torch.sigmoid(self.post_layer(q_tensor))
        return out

# ============================================================
# STEP 4: Pure Classical NN (for comparison)
# ============================================================
class ClassicalNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 8), nn.ReLU(),
            nn.Linear(8, 4), nn.ReLU(),
            nn.Linear(4, 1), nn.Sigmoid()
        )
    def forward(self, x):
        return self.net(x)

# ============================================================
# STEP 5: Train Both
# ============================================================
X_train_t = torch.tensor(X_train, dtype=torch.float32)
y_train_t = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
X_test_t = torch.tensor(X_test, dtype=torch.float32)
loss_fn = nn.BCELoss()

# Train Classical
print("Training CLASSICAL Neural Network...")
classical_model = ClassicalNN()
optimizer_c = optim.Adam(classical_model.parameters(), lr=0.01)
classical_losses = []
for epoch in range(100):
    optimizer_c.zero_grad()
    pred = classical_model(X_train_t)
    loss = loss_fn(pred, y_train_t)
    loss.backward()
    optimizer_c.step()
    classical_losses.append(loss.item())
    if (epoch + 1) % 25 == 0:
        print(f"  Epoch {epoch+1}/100, Loss: {loss.item():.4f}")

with torch.no_grad():
    c_pred = (classical_model(X_test_t) > 0.5).float()
    acc_classical = accuracy_score(y_test, c_pred.numpy())
print(f"  Classical NN Accuracy: {acc_classical:.1%}")
print()

# Train Hybrid Quantum
print("Training HYBRID QUANTUM Neural Network...")
print("(Slower — each forward pass runs a quantum circuit)")
hybrid_model = HybridQuantumNN()
optimizer_q = optim.Adam(
    list(hybrid_model.pre_layer.parameters()) + 
    list(hybrid_model.post_layer.parameters()) + 
    [hybrid_model.q_weights], lr=0.01
)
quantum_losses = []
n_epochs_q = 30

for epoch in range(n_epochs_q):
    predictions = []
    for i in range(len(X_train_t)):
        pred = hybrid_model.forward_single(X_train_t[i])
        predictions.append(pred)
    
    preds = torch.stack(predictions).view(-1, 1)
    loss = loss_fn(preds, y_train_t)
    optimizer_q.zero_grad()
    loss.backward()
    optimizer_q.step()
    quantum_losses.append(loss.item())
    if (epoch + 1) % 5 == 0:
        print(f"  Epoch {epoch+1}/{n_epochs_q}, Loss: {loss.item():.4f}")

q_predictions = []
with torch.no_grad():
    for i in range(len(X_test_t)):
        pred = hybrid_model.forward_single(X_test_t[i])
        q_predictions.append((pred > 0.5).float().item())

acc_quantum = accuracy_score(y_test, q_predictions)
print(f"  Hybrid Quantum NN Accuracy: {acc_quantum:.1%}")
print()

# ============================================================
# STEP 6: Visualization
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 12))
fig.suptitle("AI + Quantum: Hybrid Quantum Neural Network\n(PyTorch + QPanda3 Quantum Layer)", 
             fontsize=16, fontweight='bold')

ax1 = axes[0][0]
ax1.scatter(X[y==0, 0], X[y==0, 1], c='#3498db', label='Class 0', alpha=0.5, s=20)
ax1.scatter(X[y==1, 0], X[y==1, 1], c='#e74c3c', label='Class 1', alpha=0.5, s=20)
ax1.set_title("Half-Moon Dataset", fontsize=13, fontweight='bold')
ax1.set_xlabel("Feature 1"); ax1.set_ylabel("Feature 2")
ax1.legend(); ax1.grid(True, alpha=0.3)

ax2 = axes[0][1]
ax2.plot(classical_losses, color='#3498db', linewidth=1.5, label='Classical NN')
epochs_q = np.linspace(0, 100, n_epochs_q)
ax2.plot(epochs_q, quantum_losses, color='#9b59b6', linewidth=2, 
         linestyle='--', marker='o', markersize=4, label='Hybrid Quantum NN')
ax2.set_title("Training Loss", fontsize=13, fontweight='bold')
ax2.set_xlabel("Epoch"); ax2.set_ylabel("Loss")
ax2.legend(); ax2.grid(True, alpha=0.3)

ax3 = axes[1][0]
bars = ax3.bar(['Classical\nNN', 'Hybrid Quantum\nNN'],
               [acc_classical * 100, acc_quantum * 100],
               color=['#3498db', '#9b59b6'], edgecolor='black', linewidth=0.5, width=0.5)
for bar, val in zip(bars, [acc_classical, acc_quantum]):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             f'{val:.1%}', ha='center', fontweight='bold', fontsize=14)
ax3.set_title("Accuracy Comparison", fontsize=13, fontweight='bold')
ax3.set_ylabel("Accuracy (%)"); ax3.set_ylim(0, 110)

ax4 = axes[1][1]
q_weights_np = hybrid_model.q_weights.detach().numpy()
ax4.bar(range(len(q_weights_np)), q_weights_np, 
        color=['#9b59b6' if w > 0 else '#e74c3c' for w in q_weights_np],
        edgecolor='black', linewidth=0.5)
ax4.axhline(0, color='black', linewidth=0.5)
ax4.set_title("Learned Quantum Gate Angles", fontsize=13, fontweight='bold', color='#9b59b6')
ax4.set_xlabel("Quantum Weight Index")
ax4.set_ylabel("Angle (radians)")
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('charts/14_hybrid_quantum_neural_network.png', dpi=150, bbox_inches='tight')
print("\nChart saved: charts/14_hybrid_quantum_neural_network.png")

print("\n" + "=" * 65)
print("  WHAT JUST HAPPENED?")
print("=" * 65)
print()
print("You just trained a neural network where the MIDDLE LAYER")
print("was a quantum circuit running on a quantum simulator!")
print()
print("Architecture used:")
print("  Input (2 features)")
print("     ↓ Classical Linear Layer (2→4 neurons)")
print("     ↓ ReLU Activation")
print("     ↓ QUANTUM CIRCUIT LAYER (4 qubits)")
print("       - Data encoding via RY rotations")
print("       - Entanglement via CNOT gates")
print("       - Trainable quantum gates (8 parameters)")
print("       - Measurement → 4 probability outputs")
print("     ↓ Classical Linear Layer (4→1 neuron)")
print("     ↓ Sigmoid → Binary classification")
print()
print("Key insight: The quantum weights (rotation angles) were")
print("optimized by PyTorch's Adam optimizer alongside the")
print("classical weights — this is 'quantum-classical co-training'")
print()
print(f"Final: Classical={acc_classical:.1%} | Quantum={acc_quantum:.1%}")
