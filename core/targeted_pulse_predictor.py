# Copyright (c) 2026 Stefka Georgieva
# Licensed under CC BY-NC-ND 4.0 with Additional Commercial Terms.
# Contact: georgieva@vpr-research.eu or vpr.model@gmail.com for licensing inquiries.
import numpy as np
from collections import Counter

# ============================================================
# PRIME GENERATION & UTILS
# ============================================================
def get_primes_sieve(limit):
    """Fast 6k-based sieve to build the wave base."""
    if limit < 5:
        res = []
        if limit >= 2: res.append(2)
        if limit >= 3: res.append(3)
        return res
    
    max_m = (limit + 1) // 6
    is_composite_plus = [False] * (max_m + 1)
    is_composite_minus = [False] * (max_m + 1)
    
    for n in range(1, int(limit**0.5) // 6 + 2):
        for b in range(n, limit // (6*n-1) + 1):
            c1 = (6*n-1)*(6*b-1)
            if c1 <= limit: is_composite_plus[(c1-1)//6] = True
            c2 = (6*n+1)*(6*b+1)
            if c2 <= limit: is_composite_plus[(c2-1)//6] = True
            c3 = (6*n-1)*(6*b+1)
            if c3 <= limit: is_composite_minus[(c3+1)//6] = True
            c4 = (6*n+1)*(6*b-1)
            if c4 <= limit: is_composite_minus[(c4+1)//6] = True
            
    primes = [2, 3]
    for m in range(1, max_m + 1):
        p_minus = 6*m - 1
        if p_minus <= limit and not is_composite_minus[m]: primes.append(p_minus)
        p_plus = 6*m + 1
        if p_plus <= limit and not is_composite_plus[m]: primes.append(p_plus)
    return sorted(primes)

def is_prime_verification(n):
    """Standard prime check for final verification (not for filtering)."""
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

# ============================================================
# WAVE INTERFERENCE PREDICTOR
# ============================================================
class WavePrimePredictor:
    def __init__(self, base_limit=10000):
        # The wave base contains primes that generate the interference
        self.wave_base = get_primes_sieve(base_limit)
        
    def predict_and_verify(self, start_after, num_candidates=10):
        """
        Analyzes candidates based on wave interference.
        Predictions are made by the model, then verified for accuracy.
        """
        print(f"--- Scanning Wave Interference above {start_after} ---")
        results = []
        current_n = start_after + 1
        
        while len(results) < num_candidates:
            # Step 1: Crown Filter (6k +/- 1)
            if current_n % 6 in (1, 5):
                # Step 2: Calculate Interference Amplitude (The Wave Model)
                # Each prime p creates a 'wave' of composite numbers with 1/p energy
                interference = 0.0
                for p in self.wave_base:
                    if p * p > current_n: break
                    if current_n % p == 0:
                        interference += 1.0 / p
                
                # Step 3: Theoretical Prediction (Model's guess)
                # Prediction is 'Prime' if wave interference is zero
                predicted_as_prime = (interference == 0)
                
                # Step 4: Actual Verification (The Truth)
                actual_prime_status = is_prime_verification(current_n)
                
                # Store the data for analysis
                results.append({
                    "number": current_n,
                    "interference": round(interference, 6),
                    "predicted": "PRIME" if predicted_as_prime else "COMPOSITE",
                    "actual": "PRIME" if actual_prime_status else "COMPOSITE",
                    "success": (predicted_as_prime == actual_prime_status)
                })
                
                # Print result to console for transparency
                status_icon = "✅" if (predicted_as_prime == actual_prime_status) else "❌"
                print(f"Num: {current_n} | Wave Noise: {interference:.6f} | "
                      f"Model: {results[-1]['predicted']} | Real: {results[-1]['actual']} {status_icon}")
            
            current_n += 1
            if current_n > start_after + 5000: break # Safety break
            
        return results

# ============================================================
# EXECUTION
# ============================================================
if __name__ == "__main__":
    # Initialize model with wave base up to sqrt(target)
    # For targets around 100M, base should be 10k+
    predictor = WavePrimePredictor(base_limit=15000)
    
    target_zone = 100_357_201
    test_results = predictor.predict_and_verify(start_after=target_zone, num_candidates=15)
    
    # Summary
    correct_preds = sum(1 for r in test_results if r['success'])
    accuracy = (correct_preds / len(test_results)) * 100
    print("\n" + "="*60)
    print(f"PREDICTION SUMMARY FOR ZONE {target_zone}")
    print(f"Total Tested: {len(test_results)}")
    print(f"Model Accuracy: {accuracy:.2f}%")
    print("="*60)