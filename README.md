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
+-- README.md                          # This file
+-- requirements.txt                   # Python dependencies
+-- guide/
|   +-- Quantum_Computing_Lab_Guide.pdf  # Complete PDF guide
+-- experiments/
|   +-- 01_coin_flip.py                # Quantum coin flip
|   +-- 02_entanglement.py            # Quantum entanglement
|   +-- 03_random_numbers.py          # True random number generator
|   +-- 04_grovers_search.py          # Grover's search algorithm
|   +-- 05_teleportation.py           # Quantum teleportation
|   +-- 06_advanced_algorithms.py     # DJ, QFT, VQE, noise sim
|   +-- 07_coin_game.py               # Quantum coin game
|   +-- 08_password_cracker.py        # Quantum password cracker
|   +-- 09_error_correction.py        # 3-qubit error correction
|   +-- 10_random_walk.py             # Quantum random walk
|   +-- 11_bb84_key_distribution.py   # BB84 quantum cryptography
|   +-- 12_superdense_coding.py       # Superdense coding
+-- charts/                            # Generated chart images
    +-- (auto-generated when you run experiments)
```

---

## What's In It For You?

### If You're a Student
- **Hands-on portfolio** - show employers you've run quantum experiments
- **Foundation** for quantum computing courses and certifications
- **Understanding** that goes beyond textbook theory

### If You're an IT Professional
- **Stay ahead** - quantum computing is coming to enterprise IT
- **Client conversations** - explain quantum concepts confidently
- **Career positioning** - quantum skills are increasingly in demand

### If You're Just Curious
- **Demystify** quantum computing without needing a physics degree
- **See results** immediately - every experiment produces visual output
- **Plain English** explanations - no jargon, no complex math

---

## Learn More - Free Resources

### Beginner Courses (Free)
| Resource | Platform | Level | Link |
|----------|----------|-------|------|
| Quantum Computing for Everyone | edX (UChicago) | Beginner | [Link](https://www.edx.org/learn/quantum-computing/the-university-of-chicago-quantum-computing-for-everyone) |
| Qiskit Textbook | IBM | Beginner-Advanced | [Link](https://github.com/Qiskit/textbook) |
| Quantum Computing Course | freeCodeCamp (YouTube) | Beginner | [Link](https://www.youtube.com/watch?v=tsbCSkvHhMo) |
| Quantum 101 | Microsoft Learn | Beginner | [Link](https://learn.microsoft.com/en-us/azure/quantum/) |
| Linux Foundation QC Fundamentals | Linux Foundation | Beginner | [Link](https://training.linuxfoundation.org/training/fundamentals-of-quantum-computing/) |

### YouTube Channels
- **Quantum Soar** - Simple algorithm explanations
- **Qiskit** - Official IBM quantum channel
- **Quantum Sense** - Strong on foundations
- **freeCodeCamp** - Full beginner course
- **Google Quantum AI** - Latest hardware breakthroughs

### Books (Free Online)
- **"Quantum Computing for the Quantum Curious"** - Open access, high school physics only ([Archive.org](https://archive.org/details/oapen-20.500.12657-48236))
- **"Introduction to Classical and Quantum Computing"** by Tom Wong - Only needs trigonometry
- **"Learn Quantum Computation using Qiskit"** - Free IBM textbook with code ([GitHub](https://github.com/Qiskit/textbook))

### Tools & Platforms
- **Origin Quantum QPanda3** - What this lab uses ([originqc.com](https://originqc.com/developer-tools/qpanda))
- **IBM Quantum Experience** - Free access to real quantum computers ([quantum.ibm.com](https://quantum.ibm.com))
- **Google Cirq** - Google's quantum framework ([quantumai.google/cirq](https://quantumai.google/cirq))
- **Microsoft QDK** - Q# language and Azure Quantum ([learn.microsoft.com](https://learn.microsoft.com/en-us/azure/quantum/))

---

## About Origin Quantum & QPanda3

This lab uses **QPanda3** (Quantum Programming Architecture for NISQ Device Application v3), developed by **Origin Quantum** - China's leading quantum computing company. QPanda3 is:

- **Open source** and freely available via `pip install pyqpanda3`
- **20x faster** circuit construction than Qiskit (benchmarked)
- Connected to **Origin Wukong**, a 72-qubit superconducting quantum processor
- Supports local simulation (what we use) and cloud-based real hardware execution

---

## Contributing

Found a bug? Want to add an experiment? PRs are welcome!

1. Fork this repo
2. Create a branch (`git checkout -b new-experiment`)
3. Add your experiment in the `experiments/` folder
4. Submit a Pull Request

---

## License

MIT License - Use freely for learning, teaching, and sharing.

---

**Built with curiosity and [Perplexity Pro](https://perplexity.ai) | Powered by [Origin Quantum QPanda3](https://originqc.com/developer-tools/qpanda)**
