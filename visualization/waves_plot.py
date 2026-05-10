# Copyright (c) 2026 Stefka Georgieva
# Licensed under CC BY-NC-ND 4.0 with Additional Commercial Terms.
# Contact: georgieva@vpr-research.eu or vpr.model@gmail.com for licensing inquiries.
import matplotlib.pyplot as plt
import numpy as np

def plot_wave_dna_fixed(limit):
    fig, ax = plt.subplots(figsize=(16, 10))
    strand_a_y, strand_b_y = 1, -1
    
    
    waves = {}  # 
    node_types = {} # 
    
    # 1. GENERATION OF ALL POINTS AND WAVES
    all_positions = []
    for n in range(1, (limit // 6) + 2):
        if 6*n-1 <= limit: all_positions.append((6*n-1, strand_a_y))
        if 6*n+1 <= limit: all_positions.append((6*n+1, strand_b_y))

    # Wave flow simulation
    discovered_primes = []
    for pos, y in all_positions:
        # 
        hit_by = [src for src, targets in waves.items() if pos in targets]
        
        if not hit_by:
            node_types[pos] = 'prime'
            discovered_primes.append(pos)
        else:
            node_types[pos] = 'composite'
        
        # 
        # 
        current_targets = []
        for p in discovered_primes:
            collision = pos * p
            if collision <= limit:
                t = collision
                while t <= limit:
                    current_targets.append(t)
                    t += (pos * 6)
        waves[pos] = list(set(current_targets))

    
    for src, targets in waves.items():
        is_prime = node_types[src] == 'prime'
        y_src = 1 if src % 6 == 5 else -1
        
        color = 'green' if is_prime else 'red'
        alpha = 0.3 if is_prime else 0.15
        z = 2 if is_prime else 1
        
        for tg in targets:
            y_tg = 1 if tg % 6 == 5 else -1
            x_arc = np.linspace(src, tg, 100)
            amp = abs(tg - src) * 0.1
            y_arc = np.linspace(y_src, y_tg, 100) + amp * np.sin(np.pi * (x_arc - src) / (tg - src))
            ax.plot(x_arc, y_arc, color=color, alpha=alpha, linewidth=0.8, zorder=z)

    
    for pos, y in all_positions:
        if node_types[pos] == 'prime':
            ax.plot(pos, y, 'go', markersize=10, zorder=5)
            ax.annotate(str(pos), (pos, y), xytext=(0, 15 if y > 0 else -25), 
                        textcoords="offset points", ha='center', color='green', fontweight='normal', fontsize=7)
        else:
            ax.plot(pos, y, 'ro', markersize=7, zorder=4)
           
            ax.annotate(str(pos), (pos, y), xytext=(0, 10 if y > 0 else -20), 
                        textcoords="offset points", ha='center', color='red', fontsize=7)

    ax.set_title('The Wave Map (Primes as Sources, Composites as Repeaters)')
    ax.set_yticks([-1, 1]); ax.set_yticklabels(['Strand B (6n+1)', 'Strand A (6n-1)'])
    
   
    for spine in ['top', 'right', 'bottom', 'left']:
        ax.spines[spine].set_visible(False)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_wave_dna_fixed(250)