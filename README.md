# Quantum Computing Hands-On Lab

**Learn Quantum Computing by Running Real Experiments - No PhD Required**

> Built with [Perplexity Pro](https://perplexity.ai) in under 20 minutes. Every experiment runs locally on your computer using Origin Quantum's QPanda3 simulator.

---

## What Is This?

This is a **beginner-friendly, hands-on quantum computing lab** that you can run on your own computer. Instead of reading theory for months, you'll run 14 real quantum experiments and *see* quantum mechanics in action through charts and results.

No cloud account needed. No quantum hardware required. Just Python and curiosity.

---

## What Will You Learn?

| # | Experiment | What It Teaches You | Real-World Connection |
|---|-----------|--------------------|-----------------------|
| 1 | Quantum Coin Flip | Superposition - a qubit can be 0 AND 1 | Random number generation for security |
| 2 | Quantum Entanglement | Two qubits linked across any distance | Foundation of quantum internet |
| 3 | Quantum Random Number Generator | True randomness (not pseudo-random) | Cryptography, lottery systems |
| 4 | Grover's Search | Searching a database quadratically faster | Database search, optimization |
| 5 | Quantum Teleportation | Transfer quantum states instantly | Quantum networking |
| 6 | Deutsch-Jozsa Algorithm | Determine function type in 1 shot | Algorithm speedup proof |
| 7 | Quantum Fourier Transform | Frequency analysis on qubits | Shor's algorithm (breaks RSA) |
| 8 | VQE (Variational Quantum Eigensolver) | Find minimum energy of molecules | Drug discovery, materials science |
| 9 | Noise Simulation | How real quantum computers make errors | Understanding hardware limitations |
| 10 | Quantum Coin Game | Quantum strategy always beats classical | Game theory, decision making |
| 11 | Quantum Password Cracker | Grover's algorithm finds passwords faster | Cybersecurity implications |
| 12 | Quantum Error Correction | Protecting fragile qubits from errors | Building reliable quantum computers |
| 13 | Quantum Random Walk | Quantum particles spread faster than classical | Why quantum search is faster |
| 14 | BB84 Key Distribution | Create unbreakable encryption keys | Bank security, government comms |
| 15 | Superdense Coding | Send 2 bits using 1 qubit | Doubling communication capacity |

---

## Quick Start (5 Minutes)

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Step 1: Clone This Repository
```bash
git clone https://github.com/zkrishna12/Perplexity-Max-Quantum-Computing-Setup.git
cd Perplexity-Max-Quantum-Computing-Setup
```

### Step 2: Create a Virtual Environment
```bash
python -m venv quantum-env

# Windows:
quantum-env\Scripts\activate

# Mac/Linux:
source quantum-env/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install pyqpanda3 matplotlib numpy
```

### Step 4: Run Your First Experiment
```bash
python experiments/01_coin_flip.py
```

That's it! You'll see a chart showing a quantum coin that lands 50/50 - your first quantum experiment.

---

## How to Use with Perplexity Pro

This entire lab was built and run using **Perplexity Pro** as an AI coding assistant. Here's how you can do the same:

1. **Open Perplexity Pro** (perplexity.ai)
2. **Paste this prompt:**
   > "I have Python installed on my computer. Help me set up Origin Quantum's QPanda3 and run quantum computing experiments. Start with a simple quantum coin flip and explain the results in plain English."
3. **Perplexity will:**
   - Create the virtual environment for you
   - Install all dependencies
   - Write and run the experiment code
   - Generate charts showing results
   - Explain everything in simple language
4. **To run more experiments, just say:**
   > "Run experiment #11 (Password Cracker) and explain what it means"

**Total setup time: ~5 minutes.** Perplexity handles all the coding - you just learn.

---

## Project Structure

```
quantum-computing-lab/
+-- README.md
+-- requirements.txt
+-- guide/
+-- experiments/
|   +-- 01_coin_flip.py
|   +-- 02_entanglement.py
|   +-- 03_random_numbers.py
|   +-- 04_grovers_search.py
|   +-- 05_teleportation.py
|   +-- 06_advanced_algorithms.py
|   +-- 07_coin_game.py
|   +-- 08_password_cracker.py
|   +-- 09_error_correction.py
|   +-- 10_random_walk.py
|   +-- 11_bb84_key_distribution.py
|   +-- 12_superdense_coding.py
+-- charts/
```

---

## License

MIT License - Use freely for learning, teaching, and sharing.

**Built with curiosity and [Perplexity Pro](https://perplexity.ai) | Powered by [Origin Quantum QPanda3](https://originqc.com/developer-tools/qpanda)**
