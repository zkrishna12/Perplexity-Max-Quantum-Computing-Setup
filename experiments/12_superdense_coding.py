"""
Superdense Coding
==================
Superdense coding is the reverse of quantum teleportation: instead of sending
a quantum state using classical bits, it sends 2 classical bits of information
using just 1 qubit! This is possible because Alice and Bob share a pre-entangled
Bell pair, which acts as a communication resource.

THE PROTOCOL:
  1. Pre-shared entanglement: Alice and Bob share a Bell pair |Phi+>.
     Alice holds qubit 0, Bob holds qubit 1.

  2. Alice encodes her 2-bit message by applying one of four operations:
       '00' -> Nothing (I gate)     -> |Phi+>
       '01' -> X gate on her qubit  -> |Psi+>
       '10' -> Z gate on her qubit  -> |Phi->
       '11' -> X then Z gates       -> |Psi->
     Each operation produces a different Bell state.

  3. Alice sends her single qubit to Bob.

  4. Bob decodes by applying CNOT(0,1) then H(0) to his two qubits.
     This maps each Bell state back to a unique 2-bit computational state:
       |Phi+> -> |00>
       |Psi+> -> |01>
       |Phi-> -> |10>
       |Psi-> -> |11>

  5. Bob measures both qubits and reads Alice's 2-bit message.

This experiment tests all 4 messages and shows 100% correct reception.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, X, Z, CNOT, measure

# -- Output directory --
charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'charts')
os.makedirs(charts_dir, exist_ok=True)

print("=" * 60)
print("  EXPERIMENT 12 - Superdense Coding")
print("=" * 60)
print()
print("Sending 2 classical bits using 1 qubit (via pre-shared entanglement).")
print()

SHOTS = 10000

messages = ['00', '01', '10', '11']
encoding_ops = {
    '00': 'I   (nothing)',
    '01': 'X',
    '10': 'Z',
    '11': 'X then Z',
}

results = {}

print(f"{'Message':>10}  {'Encoding':>14}  {'Decoded':>10}  {'Accuracy':>10}")
print("-" * 55)

for msg in messages:
    circuit = QCircuit()

    # Step 1: Create Bell pair |Phi+> -- Alice holds q0, Bob holds q1
    circuit << H(0) << CNOT(0, 1)

    # Step 2: Alice encodes her message
    if msg == '01':
        circuit << X(0)
    elif msg == '10':
        circuit << Z(0)
    elif msg == '11':
        circuit << X(0) << Z(0)
    # '00' -> no operation (identity)

    # Step 3: Bob decodes (CNOT then H on Alice's qubit side)
    circuit << CNOT(0, 1) << H(0)

    prog = QProg()
    prog << circuit << measure(0, 0) << measure(1, 1)

    qvm = CPUQVM()
    qvm.run(prog, shots=SHOTS)
    counts = qvm.result().get_counts()

    # QPanda3 bit ordering: output string "ab" -> cbit1=a, cbit0=b
    # decoded message = q0 then q1 = output[1] + output[0] = reversed string
    decoded_counts = {}
    for k, v in counts.items():
        ks = k.zfill(2)
        decoded = ks[1] + ks[0]   # flip to get q0q1 order = msg[0]msg[1]
        decoded_counts[decoded] = decoded_counts.get(decoded, 0) + v

    target_count = decoded_counts.get(msg, 0)
    accuracy = 100 * target_count / SHOTS
    results[msg] = (decoded_counts, accuracy)

    enc_op = encoding_ops[msg]
    top_decoded = max(decoded_counts, key=decoded_counts.get)
    print(f"  '{msg}'     {enc_op:>16}     '{top_decoded}'     {accuracy:6.1f}%")

print()
print("All 4 messages decoded with ~100% accuracy -- superdense coding works!")
print()

# -- Plot --
fig, axes = plt.subplots(2, 2, figsize=(12, 9))
axes = axes.flatten()

for i, msg in enumerate(messages):
    ax = axes[i]
    decoded_counts, accuracy = results[msg]

    all_outcomes = {'00': 0, '01': 0, '10': 0, '11': 0}
    all_outcomes.update(decoded_counts)

    labels = list(all_outcomes.keys())
    values = list(all_outcomes.values())
    colors = ['#2ecc71' if lbl == msg else '#3498db' for lbl in labels]

    bars = ax.bar(labels, values, color=colors, edgecolor='white',
                  linewidth=1.5, width=0.6)
    for bar, val in zip(bars, values):
        if val > 10:
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 50,
                    f'{100*val/SHOTS:.1f}%',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax.set_title(f"Alice sends: '{msg}' ({encoding_ops[msg]})\n"
                 f"Bob decodes with {accuracy:.1f}% accuracy",
                 fontsize=11, fontweight='bold')
    ax.set_xlabel('Decoded Message', fontsize=10)
    ax.set_ylabel('Count', fontsize=10)
    ax.set_ylim(0, SHOTS * 1.2)
    ax.grid(axis='y', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    from matplotlib.patches import Patch
    legend_elems = [Patch(color='#2ecc71', label=f"Correct '{msg}'"),
                    Patch(color='#3498db', label='Other outcomes')]
    ax.legend(handles=legend_elems, fontsize=9)

plt.suptitle('Superdense Coding -- Sending 2 Classical Bits per 1 Qubit\n'
             'All 4 messages decoded with ~100% accuracy via entanglement',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
out_path = os.path.join(charts_dir, '12_superdense_coding.png')
plt.savefig(out_path, dpi=150, bbox_inches='tight')
plt.close()

# -- Summary accuracy bar chart --
fig2, ax2 = plt.subplots(figsize=(8, 4))
msg_labels = [f"'{m}'\n({encoding_ops[m]})" for m in messages]
accuracies = [results[m][1] for m in messages]
bar_colors = ['#2ecc71' if a > 90 else '#e74c3c' for a in accuracies]

bars = ax2.bar(range(len(messages)), accuracies, color=bar_colors,
               edgecolor='white', linewidth=1.5, width=0.5)
for bar, acc in zip(bars, accuracies):
    ax2.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + 0.4,
             f'{acc:.1f}%', ha='center', va='bottom',
             fontsize=12, fontweight='bold')

ax2.axhline(100, color='#27ae60', linestyle='--', linewidth=1.5, label='Perfect 100%')
ax2.set_title('Superdense Coding -- Decoding Accuracy for All 4 Messages',
              fontsize=12, fontweight='bold')
ax2.set_xticks(range(len(messages)))
ax2.set_xticklabels(msg_labels, fontsize=9)
ax2.set_ylabel('Decoding Accuracy (%)', fontsize=11)
ax2.set_ylim(0, 115)
ax2.legend(fontsize=10)
ax2.grid(axis='y', alpha=0.3)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
plt.tight_layout()
summary_path = os.path.join(charts_dir, '12_superdense_coding_summary.png')
plt.savefig(summary_path, dpi=150, bbox_inches='tight')
plt.close()

print(f"Charts saved to: {out_path}")
print(f"              and {summary_path}")
print()
print("Conclusion: Superdense coding allows Alice to send 2 bits of classical")
print("information by transmitting just 1 qubit, doubling the channel capacity")
print("through the pre-shared quantum entanglement resource.")
