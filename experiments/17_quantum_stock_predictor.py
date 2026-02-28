#!/usr/bin/env python3
"""
AI + Quantum Experiment 5: Quantum Stock Pattern Predictor
===========================================================
A hybrid quantum-classical system for predicting stock price movements.

Architecture:
  Stock Data -> Technical Indicators (classical) 
             -> Quantum Feature Extraction (quantum circuit)
             -> Combined Hybrid Features
             -> PyTorch Neural Network -> UP/DOWN Prediction

Three models compete:
  1. Classical AI (technical indicators only)
  2. Quantum AI (quantum features only)
  3. Hybrid AI (classical + quantum features combined)

What You'll Learn:
  - How quantum circuits extract financial patterns
  - Why hybrid (classical+quantum) is the industry approach
  - Time-series aware train/test splitting
  - Real-world application banks are investing in

Note: Uses simulated stock data for demonstration.

Requirements: pyqpanda3, torch, scikit-learn, matplotlib, numpy
Run: python 17_quantum_stock_predictor.py
"""
from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, RY, RZ, CNOT, measure
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math

print("=" * 65)
print("  AI + QUANTUM EXP 5: Quantum Stock Pattern Predictor")
print("  (Quantum Feature Extraction + PyTorch Prediction)")
print("=" * 65)
print()

# ============================================================
# STEP 1: Generate Stock-Like Data
# ============================================================
np.random.seed(42)
n_days = 500
price = [100.0]
for i in range(1, n_days):
    trend = 0.02 * math.sin(2 * math.pi * i / 100)
    momentum = 0.3 * (price[-1] - price[-2]) / price[-2] if i > 1 else 0
    mean_rev = -0.01 * (price[-1] - 100) / 100
    noise = np.random.normal(0, 0.015)
    seasonal = 0.005 * math.sin(2 * math.pi * i / 20)
    price.append(price[-1] * (1 + trend + momentum * 0.1 + mean_rev + noise + seasonal))
price = np.array(price)

# Create features (look-back window of 10 days)
window = 10
features, labels = [], []
for i in range(window, len(price) - 1):
    wp = price[i-window:i]
    returns = np.diff(wp) / wp[:-1]
    features.append([
        returns.mean(), returns.std(), returns[-1],
        (wp[-1] - wp[0]) / wp[0],
        (wp[-1] - wp.mean()) / wp.std(),
        sum(1 for r in returns if r > 0) / len(returns),
    ])
    labels.append(1 if price[i+1] > price[i] else 0)

X = np.array(features); y = np.array(labels)
scaler = StandardScaler(); X_scaled = scaler.fit_transform(X)

print(f"Stock simulation: {n_days} days, ${price[0]:.0f} -> ${price[-1]:.2f}")
print(f"  {len(X)} samples | Up: {sum(y)} | Down: {len(y)-sum(y)}")
print()

# ============================================================
# STEP 2: Quantum Feature Extraction
# ============================================================
def quantum_stock_features(features, shots=500):
    n_qubits = 4
    circuit = QCircuit()
    for i in range(n_qubits):
        val = float(features[i % len(features)])
        circuit << H(i) << RY(i, val * math.pi) << RZ(i, val * math.pi * 0.5)
    circuit << CNOT(0, 1) << CNOT(1, 2) << CNOT(2, 3) << CNOT(3, 0)
    for i in range(n_qubits):
        j = (i + 2) % n_qubits
        circuit << RY(i, float(features[i % len(features)] * features[j % len(features)]) * math.pi)
    circuit << CNOT(0, 2) << CNOT(1, 3)
    
    prog = QProg() << circuit
    for i in range(n_qubits):
        prog << measure(i, i)
    qvm = CPUQVM(); qvm.run(prog, shots)
    counts = qvm.result().get_counts()
    return np.array([counts.get(format(b, f'0{n_qubits}b'), 0) / shots for b in range(2**n_qubits)])

print("Extracting quantum features...")
X_quantum = []
for i, x in enumerate(X_scaled):
    X_quantum.append(quantum_stock_features(x))
    if (i + 1) % 100 == 0:
        print(f"  {i+1}/{len(X_scaled)} days processed...")
X_quantum = np.array(X_quantum)
X_hybrid = np.hstack([X_scaled, X_quantum])
print(f"  Classical: {X_scaled.shape} | Quantum: {X_quantum.shape} | Hybrid: {X_hybrid.shape}")
print()

# ============================================================
# STEP 3: Time-Series Split (no future peeking!)
# ============================================================
split = int(len(X) * 0.7)
X_train_c, X_test_c = X_scaled[:split], X_scaled[split:]
X_train_q, X_test_q = X_quantum[:split], X_quantum[split:]
X_train_h, X_test_h = X_hybrid[:split], X_hybrid[split:]
y_train, y_test = y[:split], y[split:]

# ============================================================
# STEP 4: PyTorch Predictor
# ============================================================
class StockPredictor(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 32), nn.ReLU(), nn.Dropout(0.2),
            nn.Linear(32, 16), nn.ReLU(), nn.Dropout(0.2),
            nn.Linear(16, 1), nn.Sigmoid()
        )
    def forward(self, x):
        return self.net(x)

def train_model(model, X_tr, y_tr, X_te, y_te, epochs=200):
    X_tr_t = torch.tensor(X_tr, dtype=torch.float32)
    y_tr_t = torch.tensor(y_tr, dtype=torch.float32).unsqueeze(1)
    X_te_t = torch.tensor(X_te, dtype=torch.float32)
    
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.BCELoss()
    losses = []
    
    for epoch in range(epochs):
        model.train(); optimizer.zero_grad()
        loss = loss_fn(model(X_tr_t), y_tr_t); loss.backward(); optimizer.step()
        losses.append(loss.item())
    
    model.eval()
    with torch.no_grad():
        test_acc = accuracy_score(y_te, (model(X_te_t) > 0.5).float().numpy())
        test_f1 = f1_score(y_te, (model(X_te_t) > 0.5).float().numpy(), average='weighted')
    return test_acc, test_f1, losses

# ============================================================
# STEP 5: Train All Three Models
# ============================================================
print("Training models...")
acc_c, f1_c, losses_c = train_model(StockPredictor(X_train_c.shape[1]), X_train_c, y_train, X_test_c, y_test)
print(f"  Classical AI:  {acc_c:.1%} accuracy, F1={f1_c:.3f}")
acc_q, f1_q, losses_q = train_model(StockPredictor(X_train_q.shape[1]), X_train_q, y_train, X_test_q, y_test)
print(f"  Quantum AI:    {acc_q:.1%} accuracy, F1={f1_q:.3f}")
acc_h, f1_h, losses_h = train_model(StockPredictor(X_train_h.shape[1]), X_train_h, y_train, X_test_h, y_test)
print(f"  Hybrid AI:     {acc_h:.1%} accuracy, F1={f1_h:.3f}")
random_acc = max(sum(y_test)/len(y_test), 1-sum(y_test)/len(y_test))
print(f"  Random guess:  {random_acc:.1%}")
print()

# ============================================================
# STEP 6: Visualization
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle("AI + Quantum: Stock Pattern Predictor\n(Classical vs Quantum vs Hybrid)", 
             fontsize=16, fontweight='bold')

ax1 = axes[0][0]
ax1.plot(range(len(price)), price, 'gray', alpha=0.5, linewidth=1)
ax1.axvline(split + window, color='red', linestyle='--', alpha=0.7, label='Train/Test Split')
ax1.set_title("Stock Price Simulation", fontsize=12, fontweight='bold')
ax1.set_xlabel("Day"); ax1.set_ylabel("Price ($)"); ax1.legend(); ax1.grid(True, alpha=0.3)

ax2 = axes[0][1]
bars = ax2.bar(['Classical\nAI', 'Quantum\nAI', 'HYBRID\n(Both)', 'Random\nBaseline'],
               [acc_c*100, acc_q*100, acc_h*100, random_acc*100],
               color=['#3498db', '#9b59b6', '#e74c3c', '#95a5a6'], edgecolor='black', width=0.6)
for bar in bars:
    ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
             f'{bar.get_height():.1f}%', ha='center', fontweight='bold', fontsize=11)
ax2.set_title("Prediction Accuracy", fontsize=12, fontweight='bold')
ax2.set_ylabel("Accuracy (%)"); ax2.set_ylim(0, 80)
ax2.axhline(50, color='gray', linestyle=':', alpha=0.5, label='Coin Flip'); ax2.legend()

ax3 = axes[1][0]
ax3.plot(losses_c, color='#3498db', linewidth=1.5, label='Classical')
ax3.plot(losses_q, color='#9b59b6', linewidth=1.5, label='Quantum')
ax3.plot(losses_h, color='#e74c3c', linewidth=1.5, label='Hybrid')
ax3.set_title("Training Loss", fontsize=12, fontweight='bold')
ax3.set_xlabel("Epoch"); ax3.set_ylabel("Loss"); ax3.legend(); ax3.grid(True, alpha=0.3)

ax4 = axes[1][1]
q_up = X_quantum[y==1].mean(axis=0); q_down = X_quantum[y==0].mean(axis=0)
x_pos = range(16)
ax4.bar([x-0.2 for x in x_pos], q_up, 0.4, color='#2ecc71', alpha=0.7, label='UP days')
ax4.bar([x+0.2 for x in x_pos], q_down, 0.4, color='#e74c3c', alpha=0.7, label='DOWN days')
ax4.set_title("Quantum Fingerprint (UP vs DOWN)", fontsize=12, fontweight='bold')
ax4.set_xlabel("Quantum Feature Index"); ax4.set_ylabel("Probability"); ax4.legend()

plt.tight_layout()
plt.savefig('charts/17_quantum_stock_predictor.png', dpi=150, bbox_inches='tight')
print("Chart saved: charts/17_quantum_stock_predictor.png")
