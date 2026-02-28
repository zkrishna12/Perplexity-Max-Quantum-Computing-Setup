"""
BB84 Quantum Key Distribution Protocol
========================================
BB84 (Bennett & Brassard, 1984) is the first and most famous quantum
cryptography protocol. It allows two parties (Alice and Bob) to establish
a shared secret key with unconditional security -- any eavesdropping is
physically detectable.

HOW IT WORKS:
  Alice sends qubits encoded with random bits (0 or 1) in random bases:
    Z-basis (computational): |0> or |1>
    X-basis (diagonal):      |+> or |->  (apply H gate)

  Bob measures each qubit in a randomly chosen basis.

  After transmission, Alice and Bob compare their BASES (not bits!) over
  a public channel. Measurements where they used the same basis are kept;
  the rest are discarded. This gives a shared secret key.

EAVESDROPPING DETECTION:
  If Eve intercepts qubits, she must measure in some basis. But she doesn't
  know the correct basis, so she disturbs ~50% of qubits. When Bob measures
  a disturbed qubit, there's a 25% error rate overall (50% wrong basis x
  50% wrong result). Alice and Bob can detect Eve by comparing a small
  subset of their key -- if error rate > ~11%, Eve is present.

This experiment runs:
  Scenario 1: No eavesdropper -- Alice and Bob establish a clean key (0% error).
  Scenario 2: Eve intercepts -- ~25% error rate detected in the sifted key.

100 qubits are transmitted in each scenario.
"""

import os
import random
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, X, measure

# -- Output directory --
charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'charts')
os.makedirs(charts_dir, exist_ok=True)

print("=" * 60)
print("  EXPERIMENT 11 - BB84 Quantum Key Distribution")
print("=" * 60)
print()

N_QUBITS = 100
SHOTS    = 1000   # shots per qubit measurement


def simulate_bb84(n_qubits, eavesdrop=False):
    """
    Simulate the BB84 protocol for n_qubits.
    Returns: alice_bits, alice_bases, bob_bases, bob_results, sifted_errors
    """
    alice_bits  = [random.randint(0, 1) for _ in range(n_qubits)]
    alice_bases = [random.choice(['Z', 'X']) for _ in range(n_qubits)]
    bob_bases   = [random.choice(['Z', 'X']) for _ in range(n_qubits)]
    bob_results = []

    for i in range(n_qubits):
        bit   = alice_bits[i]
        a_bas = alice_bases[i]
        b_bas = bob_bases[i]

        circuit = QCircuit()

        # Alice's preparation
        if bit == 1:
            circuit << X(0)
        if a_bas == 'X':
            circuit << H(0)

        # Eve's interception (if present): measure in random basis, re-prepare
        if eavesdrop:
            eve_basis = random.choice(['Z', 'X'])
            eve_circuit = QCircuit()
            if eve_basis == 'X':
                eve_circuit << H(0)
            eve_prog = QProg()
            eve_prog << circuit << eve_circuit << measure(0, 0)
            qvm_eve = CPUQVM()
            qvm_eve.run(eve_prog, shots=1)
            eve_result = list(qvm_eve.result().get_counts().keys())[0]
            eve_bit = int(eve_result)

            circuit = QCircuit()
            if eve_bit == 1:
                circuit << X(0)
            if eve_basis == 'X':
                circuit << H(0)

        # Bob's measurement (apply H if X-basis before measuring)
        bob_meas_circuit = QCircuit()
        if b_bas == 'X':
            bob_meas_circuit << H(0)

        prog = QProg()
        prog << circuit << bob_meas_circuit << measure(0, 0)

        qvm = CPUQVM()
        qvm.run(prog, shots=SHOTS)
        counts = qvm.result().get_counts()
        bob_bit = int(max(counts, key=counts.get))
        bob_results.append(bob_bit)

    # Sifting: keep only bits where Alice and Bob used the same basis
    sifted_alice = []
    sifted_bob   = []
    for i in range(n_qubits):
        if alice_bases[i] == bob_bases[i]:
            sifted_alice.append(alice_bits[i])
            sifted_bob.append(bob_results[i])

    errors = sum(a != b for a, b in zip(sifted_alice, sifted_bob))
    error_rate = errors / len(sifted_alice) if sifted_alice else 0

    return {
        'alice_bits':   alice_bits,
        'alice_bases':  alice_bases,
        'bob_bases':    bob_bases,
        'bob_results':  bob_results,
        'sifted_alice': sifted_alice,
        'sifted_bob':   sifted_bob,
        'sifted_len':   len(sifted_alice),
        'errors':       errors,
        'error_rate':   error_rate,
    }


# -- Scenario 1: No eavesdropper --
print("Scenario 1: No Eavesdropper")
print("-" * 38)
res1 = simulate_bb84(N_QUBITS, eavesdrop=False)
print(f"  Qubits transmitted:  {N_QUBITS}")
print(f"  Sifted key length:   {res1['sifted_len']} bits")
print(f"  Errors detected:     {res1['errors']}")
print(f"  Error rate:          {res1['error_rate']*100:.1f}%")
print(f"  Verdict: {'SECURE -- No eavesdropper detected' if res1['error_rate'] < 0.11 else 'INSECURE'}")
print()

# -- Scenario 2: Eve intercepts --
print("Scenario 2: Eve is Eavesdropping")
print("-" * 38)
res2 = simulate_bb84(N_QUBITS, eavesdrop=True)
print(f"  Qubits transmitted:  {N_QUBITS}")
print(f"  Sifted key length:   {res2['sifted_len']} bits")
print(f"  Errors detected:     {res2['errors']}")
print(f"  Error rate:          {res2['error_rate']*100:.1f}%")
print(f"  Verdict: {'INSECURE -- Eavesdropper detected! Abort.' if res2['error_rate'] > 0.10 else 'SECURE (unusual low error with Eve)'}")
print()
print("Theory: Eve introduces ~25% error rate by measuring in the wrong basis ~50%")
print("of the time, disturbing the qubit and causing ~50% wrong results those times.")
print()

# -- Plot --
fig, axes = plt.subplots(2, 2, figsize=(13, 9))

ax = axes[0, 0]
same_basis_1 = [1 if a == b else 0
                for a, b in zip(res1['alice_bases'], res1['bob_bases'])]
same_basis_2 = [1 if a == b else 0
                for a, b in zip(res2['alice_bases'], res2['bob_bases'])]

categories = ['Same basis\n(kept)', 'Different basis\n(discarded)']
vals1 = [sum(same_basis_1), N_QUBITS - sum(same_basis_1)]
vals2 = [sum(same_basis_2), N_QUBITS - sum(same_basis_2)]

x = np.arange(2)
w = 0.35
ax.bar(x - w/2, vals1, w, color='#2ecc71', label='No Eve',  edgecolor='white')
ax.bar(x + w/2, vals2, w, color='#3498db', label='With Eve', edgecolor='white')
for xi, v in zip(x - w/2, vals1):
    ax.text(xi, v + 0.5, str(v), ha='center', va='bottom', fontsize=10, fontweight='bold')
for xi, v in zip(x + w/2, vals2):
    ax.text(xi, v + 0.5, str(v), ha='center', va='bottom', fontsize=10, fontweight='bold')
ax.set_title('Basis Agreement\n(100 qubits each scenario)', fontsize=11, fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(categories, fontsize=10)
ax.set_ylabel('Number of Qubits', fontsize=10)
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

ax = axes[0, 1]
scenario_names = ['No Eve\n(Scenario 1)', 'Eve Present\n(Scenario 2)']
error_rates = [res1['error_rate'] * 100, res2['error_rate'] * 100]
colors = ['#2ecc71' if e < 11 else '#e74c3c' for e in error_rates]

bars = ax.bar(scenario_names, error_rates, color=colors,
              edgecolor='white', linewidth=1.5, width=0.5)
for bar, rate in zip(bars, error_rates):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.4,
            f'{rate:.1f}%', ha='center', va='bottom',
            fontsize=13, fontweight='bold')

ax.axhline(11, color='#f39c12', linestyle='--', linewidth=2,
           label='Security threshold (11%)')
ax.axhline(25, color='#e74c3c', linestyle=':', linewidth=1.5,
           label='Expected Eve error (~25%)')
ax.set_title('Sifted Key Error Rate\n(Eavesdropping Detection)', fontsize=11, fontweight='bold')
ax.set_ylabel('Error Rate (%)', fontsize=10)
ax.set_ylim(0, 40)
ax.legend(fontsize=9)
ax.grid(axis='y', alpha=0.3)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

ax = axes[1, 0]
key_length = min(res1['sifted_len'], 30)
x_bits = range(key_length)
alice_show = res1['sifted_alice'][:key_length]
bob_show   = res1['sifted_bob'][:key_length]
errors_show = [a != b for a, b in zip(alice_show, bob_show)]

ax.scatter(x_bits, alice_show, color='#3498db', s=60, label="Alice's key", zorder=5)
ax.scatter(x_bits, [b + 0.05 for b in bob_show], color='#2ecc71', s=60,
           marker='^', label="Bob's key", zorder=5)
for xi, err in enumerate(errors_show):
    if err:
        ax.axvspan(xi - 0.4, xi + 0.4, color='#e74c3c', alpha=0.3)
ax.set_title(f'Sifted Key Bits -- No Eve\n(First {key_length} of {res1["sifted_len"]} bits)',
             fontsize=11, fontweight='bold')
ax.set_xlabel('Bit Position', fontsize=10)
ax.set_ylabel('Bit Value', fontsize=10)
ax.set_yticks([0, 1]); ax.set_yticklabels(['0', '1'])
ax.set_ylim(-0.3, 1.5)
ax.legend(fontsize=9)
ax.grid(axis='y', alpha=0.2)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

ax = axes[1, 1]
key_length2 = min(res2['sifted_len'], 30)
x_bits2 = range(key_length2)
alice_show2 = res2['sifted_alice'][:key_length2]
bob_show2   = res2['sifted_bob'][:key_length2]
errors_show2 = [a != b for a, b in zip(alice_show2, bob_show2)]

ax.scatter(x_bits2, alice_show2, color='#3498db', s=60, label="Alice's key", zorder=5)
ax.scatter(x_bits2, [b + 0.05 for b in bob_show2], color='#e74c3c', s=60,
           marker='^', label="Bob's key (Eve disturbed)", zorder=5)
for xi, err in enumerate(errors_show2):
    if err:
        ax.axvspan(xi - 0.4, xi + 0.4, color='#e74c3c', alpha=0.3, label='_')
ax.set_title(f'Sifted Key Bits -- Eve Present\n(First {key_length2} of {res2["sifted_len"]} bits, '
             f'errors highlighted)',
             fontsize=11, fontweight='bold')
ax.set_xlabel('Bit Position', fontsize=10)
ax.set_ylabel('Bit Value', fontsize=10)
ax.set_yticks([0, 1]); ax.set_yticklabels(['0', '1'])
ax.set_ylim(-0.3, 1.5)
ax.legend(fontsize=9)
ax.grid(axis='y', alpha=0.2)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

plt.suptitle('BB84 Quantum Key Distribution\n'
             'Eavesdropping is physically detectable via error rate spike',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
out_path = os.path.join(charts_dir, '11_bb84_key_distribution.png')
plt.savefig(out_path, dpi=150, bbox_inches='tight')
plt.close()

print(f"Chart saved to: {out_path}")
print()
print("Conclusion: Without Eve, error rate is approx 0% (secure channel).")
print("With Eve, error rate is approx 25% -- eavesdropping is unambiguously detected.")
print("BB84 provides information-theoretically secure key exchange.")
