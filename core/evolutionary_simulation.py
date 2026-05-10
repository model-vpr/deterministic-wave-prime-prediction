# Copyright (c) 2026 Stefka Georgieva
# Licensed under CC BY-NC-ND 4.0 with Additional Commercial Terms.
# Contact: georgieva@vpr-research.eu or vpr.model@gmail.com for licensing inquiries.
import collections

def is_prime_classic(n):
    """Independent mathematical primality test."""
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

class EvolutionarySonar:
    def __init__(self, total_limit, independent_check=True):
        self.limit = total_limit
        self.independent_check = independent_check
        self.wave_registry = collections.defaultdict(list)
        self.history = [] # Пълна история на откритите източници

    def _emit_waves(self, source):
        """Emit waves from the new source by interacting with all previous sources."""
        # 1. Cross-interaction with the past
        for prev in self.history:
            impact = source * prev
            if impact <= self.limit:
                t = impact
                while t <= self.limit:
                    if source not in self.wave_registry[t]:
                        self.wave_registry[t].append(source)
                    t += (source * 6)
        
        # 2. 2. Self-resonance (Squares)
        square = source * source
        if square <= self.limit:
            t = square
            while t <= self.limit:
                if source not in self.wave_registry[t]:
                    self.wave_registry[t].append(source)
                t += (source * 6)

    def run_simulation(self, start_display=1000, end_display=1100):
        print(f"--- Sonar Evolution: 5 to {self.limit} ---")
        print(f"--- Displaying Window: {start_display} to {end_display} ---\n")
        
        for t in range(5, self.limit + 1):
            if t % 6 not in [1, 5]: continue
            
            incoming = self.wave_registry.get(t, [])
            sonar_says_prime = len(incoming) == 0
            
            # 
            self._emit_waves(t)
            self.history.append(t)

            # We only show the desired test window
            if start_display <= t <= end_display:
                status = "PRIME ✅" if sonar_says_prime else f"COMPOSITE (Hits: {sorted(incoming)})"
                report = f"[T={t:4}] Sonar: {status}"
                
                if self.independent_check:
                    actual_is_prime = is_prime_classic(t)
                    if sonar_says_prime == actual_is_prime:
                        report += " | Verifier: OK Match"
                    else:
                        report += " | Verifier: ERROR! ❌"
                
                print(report)


sim = EvolutionarySonar(total_limit=10100, independent_check=True)
sim.run_simulation(start_display=10000, end_display=10100)