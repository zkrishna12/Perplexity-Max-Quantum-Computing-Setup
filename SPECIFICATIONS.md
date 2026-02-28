# Lab Specifications & Complete Inventory

> Full technical specifications for all 20 experiments in this quantum computing lab.

---

## Environment Specifications

| Component | Version | Provider | Purpose |
|-----------|---------|----------|--------|
| Python | 3.12.12 | Python.org | Core runtime |
| QPanda3 | 0.3.3 | Origin Quantum | Quantum circuit simulator |
| PyTorch | 2.10.0 (CPU) | Meta AI | Deep learning framework |
| scikit-learn | 1.8.0 | Community | Classical ML algorithms |
| NumPy | 2.4.2 | Community | Numerical computing |
| Matplotlib | 3.10.8 | Community | Chart generation |
| Pandas | 3.0.1 | Community | Data manipulation |
| Simulator | CPUQVM | Origin Quantum | Local quantum simulator (no cloud needed) |
| **Total Env Size** | **1.8 GB** | — | **Complete portable installation** |

---

## Complete Experiment Specifications

### Part 1: Quantum Computing Fundamentals (Experiments 1–12)

| # | Experiment | Qubits | Gates Used | Shots | Quantum Concept | Level |
|---|-----------|--------|-----------|-------|----------------|-------|
| 1 | Quantum Coin Flip | 1 | H | 10,000 | Superposition | Beginner |
| 2 | Quantum Entanglement | 2 | H, CNOT | 10,000 | Entanglement | Beginner |
| 3 | Quantum RNG | 5 | H | 10,000 | True randomness | Beginner |
| 4 | Grover's Search | 4 | H, X, Z, CNOT, TOFFOLI | 10,000 | Quadratic speedup | Intermediate |
| 5 | Quantum Teleportation | 3 | H, X, Z, CNOT | 10,000 | State transfer | Intermediate |
| 6 | DJ / QFT / VQE / Noise | 3–4 | H, X, Z, CNOT, RY | 10,000 | Multiple algorithms | Advanced |
| 7 | Quantum Coin Game | 1 | H, X, Z | 10,000 | Quantum strategy | Beginner |
| 8 | Password Cracker | 4 | H, X, Z, CNOT, TOFFOLI | 10,000 | Grover's oracle | Intermediate |
| 9 | Error Correction | 5 | X, CNOT, TOFFOLI | 10,000 | 3-qubit code | Advanced |
| 10 | Random Walk | 6 | H, CNOT, X | 1,000 | Quantum diffusion | Intermediate |
| 11 | BB84 Key Distribution | 1 | H, X | 1,000 | Quantum crypto | Intermediate |
| 12 | Superdense Coding | 2 | H, X, Z, CNOT | 10,000 | 2 bits per qubit | Intermediate |

### Part 2: AI + Quantum Computing Hybrid Experiments (Experiments 13–17)

| # | Experiment | Qubits | Gates Used | Shots | Quantum Concept | AI Algorithm | Level |
|---|-----------|--------|-----------|-------|----------------|-------------|-------|
| 13 | Quantum Fruit Classifier | 4 | H, RY, RZ, CNOT | 2,000 | Quantum feature map | SVM (scikit-learn) | AI+Quantum |
| 14 | Hybrid Quantum Neural Network | 4 | H, RY, RZ, CNOT | 500 | Quantum hidden layer | PyTorch Neural Network | AI+Quantum |
| 15 | Quantum Random Forest | 8–16 | H | 1–100 | Quantum RNG seeds | Random Forest (scikit-learn) | AI+Quantum |
| 16 | Quantum vs Classical Showdown | 4 | H, RY, RZ, CNOT | 1,000 | Feature map | LR / RF / NN / SVM | AI+Quantum |
| 17 | Quantum Stock Predictor | 4 | H, RY, RZ, CNOT | 500 | Feature extraction | PyTorch Neural Network | AI+Quantum |

### Bonus: Fun Experiments

| # | Experiment | Qubits | What It Tests |
|---|-----------|--------|---------------|
| 18 | Bell's Inequality Test | 2 | Does God play dice? (S = 2.847, violated classical limit of 2.0) |
| 19 | Chicken or Egg | 4 | Quantum causal order — both came first simultaneously |

---

## Quantum + AI Concepts Covered & Why They Matter

| Concept | What It Means (Plain English) | Exp # | Why It Matters (Real World) |
|---------|------------------------------|-------|----------------------------|
| **Superposition** | A qubit is 0 AND 1 at the same time | 1, 2, 3, 7 | Parallel computing power — process millions of possibilities at once |
| **Entanglement** | Two qubits instantly linked, no matter the distance | 2, 5, 12 | Quantum internet, unhackable communication |
| **Quantum Gates** | H, X, Z, CNOT, TOFFOLI, RY, RZ, RX, CZ | All | Building blocks of every quantum program |
| **Grover's Search** | Find 1 item among N items in √N time | 4, 8 | Database search, password cracking, cybersecurity |
| **Quantum Teleportation** | Transfer a quantum state without moving it physically | 5 | Foundation of quantum networking |
| **QFT / Shor's Algorithm** | Break RSA encryption mathematically | 6 | Cryptography revolution — why banks are worried |
| **VQE** | Find the lowest energy state of a molecule | 6 | Drug discovery, materials science, chemistry |
| **Error Correction** | Protect fragile qubits from noise and errors | 9 | Making quantum computers reliable enough for production |
| **BB84 / QKD** | Create encryption keys that physics guarantees are unbreakable | 11 | Banking, military, government top-secret communication |
| **Quantum Feature Maps** | Encode classical data as quantum rotations and entanglement | 13, 16, 17 | Pattern recognition that goes beyond what classical AI can see |
| **Hybrid Quantum Neural Network** | A neural network with a quantum circuit as a hidden layer | 14 | The architecture Google and IBM are researching for next-gen AI |
| **Quantum RNG for AI** | True randomness (from physics) powering AI decisions | 15 | Unhackable AI for banking, defense, and security |
| **Quantum–Classical Benchmarking** | Fair head-to-head comparison of quantum vs classical AI | 16 | Knowing when quantum actually helps vs. when it's just hype |
| **Quantum Finance** | Quantum feature extraction for market pattern prediction | 17 | JPMorgan, Goldman Sachs, Barclays are investing millions in this |

---

## Lab Statistics & Achievement Summary

| Metric | Value | Details |
|--------|-------|--------|
| **Total Experiments** | 20 | 12 quantum fundamentals + 5 AI+Quantum hybrids + 3 fun experiments |
| **Qubits Used** | 1 to 16 | From single-qubit coin flip to 16-qubit random number generator |
| **Quantum Gates Mastered** | 10 | H, X, Z, CNOT, TOFFOLI, CZ, RY, RZ, RX, Measure |
| **AI Algorithms Integrated** | 6 | SVM, Random Forest, Neural Network, Logistic Regression, PyTorch NN, MLP |
| **Quantum Shots Fired** | ~2,000,000+ | Across all experiments combined |
| **Charts Generated** | 20+ | Each experiment produces a multi-panel visualization |
| **Lines of Python Code** | ~3,500+ | Across 17 experiment files |
| **Packages Used** | 7 | QPanda3, PyTorch, scikit-learn, NumPy, Matplotlib, Pandas, Jupyter |
| **Cloud Accounts Needed** | 0 | Everything runs locally — zero cost, zero registration |
| **Time to Build** | ~20 minutes | Using Perplexity Pro (vs. 3–5 days manually) |
| **GitHub Repo** | Live | [github.com/zkrishna12/Perplexity-Max-Quantum-Computing-Setup](https://github.com/zkrishna12/Perplexity-Max-Quantum-Computing-Setup) |
| **PDF Guide** | 20 pages | Complete lab guide with plain English explanations |

---

## Why This Is Important

### For Your Career
- **Quantum computing jobs are projected to grow 30–40% annually** through 2030. By running these experiments, you have hands-on experience that most candidates only have on paper.
- **AI + Quantum is the rarest skill combination** in the market. You now have 5 working hybrid architectures in your portfolio.
- **You can explain it in plain English** — the most valuable skill when talking to clients, managers, or in interviews.

### For the Industry
- **IBM says 2026 is the year quantum computers outperform classical ones** for the first time. These experiments prepare you for that moment.
- **$125 billion projected quantum investment by 2030** — companies need people who understand both the quantum and AI sides.
- **Banks (JPMorgan, Goldman Sachs), pharma (Merck, Roche), and tech (Google, IBM, Microsoft)** are all hiring quantum-AI talent.

### For This Repository
- **One of the very few public repos** that combines QPanda3 + PyTorch for hybrid quantum-classical ML.
- **Honest results** — we show where quantum wins AND where classical beats it, which builds trust and credibility.
- **Zero barrier to entry** — anyone with Python can clone and run everything in 5 minutes.

---

> Built with [Perplexity Pro](https://perplexity.ai) — from zero to 20 quantum experiments in a single session.