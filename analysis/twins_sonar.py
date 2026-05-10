# Copyright (c) 2026 Stefka Georgieva
# Licensed under CC BY-NC-ND 4.0 with Additional Commercial Terms.
# Contact: georgieva@vpr-research.eu or vpr.model@gmail.com for licensing inquiries.
import collections

class UniversalWaveSonar:
    """
    Deterministic Interference Wave Model (IWM) implementation.
    Analyzes the number line as a wave-interference field to identify 
    Prime Nodes (Zero Density) and Peak Resonance Points.
    """
    def __init__(self, limit):
        self.limit = limit
        # wave_registry: Stores the interference amplitude (hit count) for each coordinate
        self.wave_registry = collections.defaultdict(int)
        # wave_sources: Tracks the contributing wave generators for each coordinate
        self.wave_sources = collections.defaultdict(list)
        # registered_nodes: Stores all detected wave emitters within the progression
        self.registered_nodes = [] 

    def _emit_cascade(self, source):
        """ 
        Projects wave impacts forward based on harmonic interactions.
        Each node projects energy to future coordinates through cross-links and self-resonance.
        """
        # 1. Cross-interference with previously registered nodes
        for prev in self.registered_nodes:
            impact = source * prev
            if impact <= self.limit:
                t = impact
                while t <= self.limit:
                    self.wave_registry[t] += 1
                    if source not in self.wave_sources[t]:
                        self.wave_sources[t].append(source)
                    t += (source * 6)
        
        # 2. Harmonic Resonance (Square-wave impact: p*p)
        square = source * square_factor if (square_factor := source) else source**2
        square = source * source
        if square <= self.limit:
            t = square
            while t <= self.limit:
                self.wave_registry[t] += 1
                if source not in self.wave_sources[t]:
                    self.wave_sources[t].append(source)
                t += (source * 6)

    def run_analysis(self):
        """
        Executes a deterministic scan of the Crown (6n ± 1) progressions.
        Identifies prime pairs (Zero-Impact adjacency) and peak interference nodes.
        """
        prime_pairs = []
        last_prime = -1
        
        print(f"--- INITIALIZING WAVE ANALYSIS (Limit: {self.limit}) ---")
        
        for t in range(5, self.limit + 1):
            # Target only the 6n ± 1 progressions (The Crown)
            if t % 6 not in [1, 5]: continue
            
            # Current interference amplitude at coordinate t
            density = self.wave_registry[t]
            
            # If amplitude is 0, the node is identified as PRIME (Zero Density)
            if density == 0:
                if t - last_prime == 2:
                    prime_pairs.append((last_prime, t))
                last_prime = t
            
            # Propagate energy: Every node contributes to future interference patterns
            self._emit_cascade(t)
            self.registered_nodes.append(t)

        # Identify the global Peak Interference Node
        max_density = 0
        peak_node = 0
        for t, d in self.wave_registry.items():
            if d > max_density:
                max_density = d
                peak_node = t
                
        return prime_pairs, peak_node, max_density, self.wave_sources[peak_node]

# Execution and Reporting
if __name__ == "__main__":
    limit_value = 10000
    sonar = UniversalWaveSonar(limit_value)
    pairs, peak_t, peak_d, sources = sonar.run_analysis()

    print("\n" + "="*60)
    print(f"IWM ANALYTICAL RESULTS (Range: 5 - {limit_value})")
    print("="*60)
    print(f"1. Twin Prime Nodes (Zero-Impact Pairs): {len(pairs)}")
    print(f"2. High-Magnitude Sample Pairs: {pairs[-3:]}")
    print("-" * 60)
    print(f"3. PEAK INTERFERENCE COORDINATE: {peak_t}")
    print(f"4. RESONANCE AMPLITUDE (Total Wave Impacts): {peak_d}")
    print(f"5. Primary Wave Generators at Peak Node: {sorted(sources)[:15]}...")
    print("="*60)