"""
Quantum Coin Game (Quantum Strategy Always Wins)
=================================================
This experiment demonstrates the power of quantum strategies in a simple game
that illustrates quantum advantage in game theory.

THE GAME:
  A coin starts as Heads (|0>). Two players alternate moves:
    - Player 1 (Alice, the quantum player) acts first.
    - Opponent flips the coin or leaves it (classical random action).
    - Alice acts again.
  Whoever gets Heads at the end wins.

CLASSICAL STRATEGY:
  Alice randomly flips (random 0 or 1). Opponent randomly flips. Win rate ~50%.

QUANTUM STRATEGY (always wins):
  Alice applies H (superposition). The coin enters a quantum superposition.
  Opponent applies X (flip) -- but flipping a superposition still leaves it in
  superposition: H(|0>) + H(|1>) = same superposition, just a phase change.
  Alice applies H again. The two H gates cancel: H*X*H = Z, and H*H = I.
  So Z|0> = |0> -> Alice always wins regardless of opponent's move!

  Circuit: H(0) -> X(0) [opponent] -> H(0) -> measure
  Result: always '0' (Heads = win for Alice).

What this experiment does:
  1. Runs 1000 classical games (random flip each time) -> ~50% win rate.
  2. Runs 1000 quantum games (H then X then H strategy) -> 100% win rate.
  3. Shows a comparison bar chart.
"""

import os
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, X, measure

# -- Output directory --
charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'charts')
os.makedirs(charts_dir, exist_ok=True)

print("=" * 60)
print("  EXPERIMENT 07 - Quantum Coin Game")
print("=" * 60)
print()
print("The game: Start with Heads (|0>). Alice moves, Opponent moves,")
print("Alice moves. Alice wins if final state is Heads (0).")
print()

GAMES = 1000

# -- Classical Strategy --
classical_wins = 0
classical_losses = 0

for _ in range(GAMES):
    coin = 0  # Start Heads
    if random.randint(0, 1) == 1:
        coin = 1 - coin
    if random.randint(0, 1) == 1:
        coin = 1 - coin
    if random.randint(0, 1) == 1:
        coin = 1 - coin
    if coin == 0:
        classical_wins += 1
    else:
        classical_losses += 1

classical_win_pct = 100 * classical_wins / GAMES
print(f"Classical strategy ({GAMES} games):")
print(f"  Wins: {classical_wins}  ({classical_win_pct:.1f}%)")
print(f"  Losses: {classical_losses}  ({100 - classical_win_pct:.1f}%)")
print()

# -- Quantum Strategy --
# H(0) -> X(0) [opponent always flips] -> H(0) -> measure
# H*X*H = Z, and Z|0> = |0> -> always wins!
circuit_q = QCircuit()
circuit_q << H(0) << X(0) << H(0)     # Alice(H), Opponent(X), Alice(H)

prog_q = QProg()
prog_q << circuit_q << measure(0, 0)

qvm = CPUQVM()
qvm.run(prog_q, shots=GAMES)
q_counts = qvm.result().get_counts()

quantum_wins   = q_counts.get('0', 0)  # '0' = Heads = win
quantum_losses = q_counts.get('1', 0)
quantum_win_pct = 100 * quantum_wins / GAMES

print(f"Quantum strategy ({GAMES} games):")
print(f"  Wins: {quantum_wins}  ({quantum_win_pct:.1f}%)")
print(f"  Losses: {quantum_losses}  ({100 - quantum_win_pct:.1f}%)")
print()
print("Why does the quantum strategy always win?")
print("  H|0> = |+>  (superposition)")
print("  X|+> = |+>  (flip doesn't change superposition, only phase)")
print("  H|+> = |0>  (Hadamard undoes the superposition -> always Heads)")
print("  The two H gates form a 'quantum lock' -- no classical move can break it!")
print()

# -- Plot --
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

strategies = ['Classical\n(Random)', 'Quantum\n(H*X*H)']
win_rates  = [classical_win_pct, quantum_win_pct]
loss_rates = [100 - w for w in win_rates]
bar_colors = ['#3498db', '#2ecc71']

x = np.arange(len(strategies))
width = 0.4

bars_win  = axes[0].bar(x - width/2, win_rates,  width, label='Wins',
                         color=bar_colors, edgecolor='white', linewidth=1.5)
bars_loss = axes[0].bar(x + width/2, loss_rates, width, label='Losses',
                         color=['#e74c3c', '#e74c3c'], edgecolor='white',
                         linewidth=1.5, alpha=0.7)

for bar, val in zip(bars_win, win_rates):
    axes[0].text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.8,
                 f'{val:.1f}%', ha='center', va='bottom',
                 fontsize=12, fontweight='bold')
for bar, val in zip(bars_loss, loss_rates):
    if val > 0.5:
        axes[0].text(bar.get_x() + bar.get_width() / 2,
                     bar.get_height() + 0.8,
                     f'{val:.1f}%', ha='center', va='bottom',
                     fontsize=12, fontweight='bold')

axes[0].axhline(50, color='#f39c12', linestyle='--', linewidth=1.5,
                label='Chance level (50%)')
axes[0].set_title(f'Coin Game Win Rate\n({GAMES} games each)',
                  fontsize=13, fontweight='bold')
axes[0].set_ylabel('Win/Loss Rate (%)', fontsize=11)
axes[0].set_xticks(x)
axes[0].set_xticklabels(strategies, fontsize=11)
axes[0].set_ylim(0, 115)
axes[0].legend(fontsize=10)
axes[0].grid(axis='y', alpha=0.3)
axes[0].spines['top'].set_visible(False)
axes[0].spines['right'].set_visible(False)

cumulative_wins = []
cum = 0
shots_list = ['0'] * quantum_wins + ['1'] * quantum_losses
random.shuffle(shots_list)
for i, outcome in enumerate(shots_list):
    if outcome == '0':
        cum += 1
    cumulative_wins.append(100 * cum / (i + 1))

axes[1].plot(range(1, GAMES + 1), cumulative_wins,
             color='#2ecc71', linewidth=1.5, alpha=0.9, label='Quantum win rate')
axes[1].axhline(100, color='#27ae60', linestyle='--', linewidth=2,
                label='Perfect 100%')
axes[1].axhline(50, color='#f39c12', linestyle='--', linewidth=1.5,
                label='Classical baseline (50%)')
axes[1].fill_between(range(1, GAMES + 1), cumulative_wins, 50,
                     alpha=0.15, color='#2ecc71')
axes[1].set_title('Quantum Strategy - Cumulative Win Rate\n(per game, 1000 games)',
                  fontsize=13, fontweight='bold')
axes[1].set_xlabel('Game Number', fontsize=11)
axes[1].set_ylabel('Win Rate (%)', fontsize=11)
axes[1].set_ylim(0, 115)
axes[1].legend(fontsize=10)
axes[1].grid(alpha=0.3)
axes[1].spines['top'].set_visible(False)
axes[1].spines['right'].set_visible(False)

plt.suptitle("Quantum Coin Game - Quantum Strategy Always Wins!",
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
out_path = os.path.join(charts_dir, '07_coin_game.png')
plt.savefig(out_path, dpi=150, bbox_inches='tight')
plt.close()

print(f"Chart saved to: {out_path}")
print()
print("Conclusion: The quantum strategy wins 100% of games by exploiting")
print("the property that H gates create a state immune to X gate interference.")
