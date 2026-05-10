# Copyright (c) 2026 Stefka Georgieva
# Licensed under CC BY-NC-ND 4.0 with Additional Commercial Terms.
# Contact: georgieva@vpr-research.eu or vpr.model@gmail.com for licensing inquiries.
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks

def wave_analysis_advanced(limit=500):
    """Advanced wave analysis of prime numbers of the form 6n±1 with FFT spectrum"""
   
    def sieve_primes(limit):
        sieve = np.ones(limit + 1, dtype=bool)
        sieve[0:2] = False
        for i in range(2, int(limit**0.5) + 1):
            if sieve[i]:
                sieve[i*i:limit+1:i] = False
        return np.where(sieve)[0]
   
    all_primes = sieve_primes(limit)
   
    # Analysis of 6n+1
    max_n_plus = (limit - 1) // 6
    n_plus = np.arange(1, max_n_plus + 1)
    numbers_plus = 6 * n_plus + 1
   
    # Analysis of 6n-1
    max_n_minus = (limit + 1) // 6
    n_minus = np.arange(1, max_n_minus + 1)
    numbers_minus = 6 * n_minus - 1
   
    # Interference for 6n+1
    interference_plus = np.zeros(len(n_plus), dtype=float)
    is_prime_plus = np.ones(len(numbers_plus), dtype=bool)
   
    # Interference for 6n-1
    interference_minus = np.zeros(len(n_minus), dtype=float)
    is_prime_minus = np.ones(len(numbers_minus), dtype=bool)
   
    # Processing for 6n+1
    for p in all_primes:
        p_int = int(p)
        if p_int < 5:
            continue
       
        try:
            inv6 = pow(6, -1, p_int)
            n0 = ((-1) * inv6) % p_int
            if n0 == 0:
                n0 = p_int
        except ValueError:
            continue
       
        first_multiple_n = n0
        if first_multiple_n <= max_n_plus and 6*first_multiple_n + 1 == p_int:
            first_multiple_n = n0 + p_int
       
        for n in range(first_multiple_n, max_n_plus + 1, p_int):
            idx = n - 1
            if idx < len(is_prime_plus):
                is_prime_plus[idx] = False
                interference_plus[idx] += 1.0 / p_int
   
    # Processing for 6n-1
    for p in all_primes:
        p_int = int(p)
        if p_int < 5:
            continue
       
        try:
            inv6 = pow(6, -1, p_int)
            n0 = (1 * inv6) % p_int  # For 6n-1: 6n ≡ 1 mod p
            if n0 == 0:
                n0 = p_int
        except ValueError:
            continue
       
        first_multiple_n = n0
        if first_multiple_n <= max_n_minus and 6*first_multiple_n - 1 == p_int:
            first_multiple_n = n0 + p_int
       
        for n in range(first_multiple_n, max_n_minus + 1, p_int):
            idx = n - 1
            if idx < len(is_prime_minus):
                is_prime_minus[idx] = False
                interference_minus[idx] += 1.0 / p_int
   
    # Normalization
    if np.max(interference_plus) > 0:
        interference_plus = interference_plus / np.max(interference_plus)
    if np.max(interference_minus) > 0:
        interference_minus = interference_minus / np.max(interference_minus)
   
    # FFT analysis
    fft_plus = fft(interference_plus)
    fft_minus = fft(interference_minus)
   
    freqs_plus = fftfreq(len(interference_plus))
    freqs_minus = fftfreq(len(interference_minus))
   
    positive_freqs_plus = freqs_plus[:len(freqs_plus)//2]
    positive_fft_plus = np.abs(fft_plus[:len(fft_plus)//2])
   
    positive_freqs_minus = freqs_minus[:len(freqs_minus)//2]
    positive_fft_minus = np.abs(fft_minus[:len(fft_minus)//2])
   
    # Finding peaks in the spectrum
    peaks_plus, _ = find_peaks(positive_fft_plus, height=np.max(positive_fft_plus)*0.1)
    peaks_minus, _ = find_peaks(positive_fft_minus, height=np.max(positive_fft_minus)*0.1)
   
    # Visualization
    fig = plt.figure(figsize=(16, 12))
   
    # 1. Interference pattern - 6n+1
    ax1 = plt.subplot(3, 2, 1)
    ax1.plot(n_plus, interference_plus, 'b-', alpha=0.7, linewidth=0.5)
    prime_idx_plus = np.where(is_prime_plus)[0]
    if len(prime_idx_plus) > 0:
        ax1.scatter(n_plus[prime_idx_plus], interference_plus[prime_idx_plus],
                    c='red', s=20, alpha=0.7, label=f'Primes ({len(prime_idx_plus)})')
    ax1.set_xlabel('n (index)')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('Wave Model - 6n+1')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
   
    # 2. Interference pattern - 6n-1
    ax2 = plt.subplot(3, 2, 2)
    ax2.plot(n_minus, interference_minus, 'g-', alpha=0.7, linewidth=0.5)
    prime_idx_minus = np.where(is_prime_minus)[0]
    if len(prime_idx_minus) > 0:
        ax2.scatter(n_minus[prime_idx_minus], interference_minus[prime_idx_minus],
                    c='red', s=20, alpha=0.7, label=f'Primes ({len(prime_idx_minus)})')
    ax2.set_xlabel('n (index)')
    ax2.set_ylabel('Amplitude')
    ax2.set_title('Wave Model - 6n-1')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
   
    # 3. FFT Spectrum - 6n+1
    ax3 = plt.subplot(3, 2, 3)
    ax3.semilogy(positive_freqs_plus, positive_fft_plus, 'b-', alpha=0.7)
    ax3.scatter(positive_freqs_plus[peaks_plus], positive_fft_plus[peaks_plus],
                c='red', s=50, zorder=5, label='Peaks')
    ax3.set_xlabel('Frequency')
    ax3.set_ylabel('Spectral Power (log)')
    ax3.set_title('FFT Spectrum - 6n+1')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
   
    # 4. FFT Spectrum - 6n-1
    ax4 = plt.subplot(3, 2, 4)
    ax4.semilogy(positive_freqs_minus, positive_fft_minus, 'g-', alpha=0.7)
    ax4.scatter(positive_freqs_minus[peaks_minus], positive_fft_minus[peaks_minus],
                c='red', s=50, zorder=5, label='Peaks')
    ax4.set_xlabel('Frequency')
    ax4.set_ylabel('Spectral Power (log)')
    ax4.set_title('FFT Spectrum - 6n-1')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
   
    # 5. Prime distribution - histogram
    ax5 = plt.subplot(3, 2, 5)
    if len(prime_idx_plus) > 0:
        ax5.hist(n_plus[prime_idx_plus], bins=20, alpha=0.5, color='red', label='6n+1')
    if len(prime_idx_minus) > 0:
        ax5.hist(n_minus[prime_idx_minus], bins=20, alpha=0.5, color='blue', label='6n-1')
    ax5.set_xlabel('n (index)')
    ax5.set_ylabel('Count')
    ax5.set_title('Distribution of Primes by Index')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
   
    # 6. Correlation between the two sequences
    ax6 = plt.subplot(3, 2, 6)
    # Finding common indices (twins)
    min_len = min(len(interference_plus), len(interference_minus))
    correlation = np.correlate(interference_plus[:min_len], interference_minus[:min_len], mode='full')
    lags = np.arange(-min_len+1, min_len)
    ax6.plot(lags, correlation, 'purple', alpha=0.7)
    ax6.set_xlabel('Lag (offset)')
    ax6.set_ylabel('Correlation')
    ax6.set_title('Correlation between 6n+1 and 6n-1')
    ax6.grid(True, alpha=0.3)
   
    plt.tight_layout()
    plt.show()
   
    # Statistics
    print(f"\n{'='*60}")
    print(f"WAVE ANALYSIS - LIMIT {limit}")
    print(f"{'='*60}")
   
    print(f"\n📊 SEQUENCE 6n+1:")
    print(f" Total numbers: {len(numbers_plus)}")
    print(f" Number of primes: {len(prime_idx_plus)}")
    print(f" Density: {len(prime_idx_plus)/len(numbers_plus)*100:.2f}%")
    print(f" Average interference (primes): {np.mean(interference_plus[prime_idx_plus]):.6f}")
    print(f" Average interference (composites): {np.mean(interference_plus[~is_prime_plus]):.6f}")
   
    print(f"\n📊 SEQUENCE 6n-1:")
    print(f" Total numbers: {len(numbers_minus)}")
    print(f" Number of primes: {len(prime_idx_minus)}")
    print(f" Density: {len(prime_idx_minus)/len(numbers_minus)*100:.2f}%")
    print(f" Average interference (primes): {np.mean(interference_minus[prime_idx_minus]):.6f}")
    print(f" Average interference (composites): {np.mean(interference_minus[~is_prime_minus]):.6f}")
   
    print(f"\n🎵 SPECTRAL ANALYSIS:")
    print(f" 6n+1 - Number of FFT peaks: {len(peaks_plus)}")
    print(f" 6n-1 - Number of FFT peaks: {len(peaks_minus)}")
   
    # Finding twin primes
    twins = []
    for i in range(min(len(numbers_plus), len(numbers_minus))):
        if numbers_plus[i] == numbers_minus[i] + 2:
            twins.append((numbers_minus[i], numbers_plus[i]))
   
    print(f"\n👯 TWIN PRIMES (p, p+2) up to {limit}:")
    print(f" Number of pairs: {len(twins)}")
    if len(twins) > 0:
        print(f" First 10: {twins[:10]}")
   
    # Verification with sympy
    try:
        from sympy import isprime
        expected_plus = [6*n+1 for n in range(1, len(numbers_plus)+1) if isprime(6*n+1)]
        found_plus = numbers_plus[is_prime_plus].tolist()
       
        expected_minus = [6*n-1 for n in range(1, len(numbers_minus)+1) if isprime(6*n-1)]
        found_minus = numbers_minus[is_prime_minus].tolist()
       
        if expected_plus == found_plus and expected_minus == found_minus:
            print(f"\n✅ VERIFICATION: 100% accurate!")
        else:
            print(f"\n⚠️ Verification is not accurate!")
    except ImportError:
        print(f"\n⚠️ Sympy is not installed - verification skipped")
   
    return {
        'n_plus': n_plus, 'numbers_plus': numbers_plus, 'is_prime_plus': is_prime_plus,
        'n_minus': n_minus, 'numbers_minus': numbers_minus, 'is_prime_minus': is_prime_minus,
        'interference_plus': interference_plus, 'interference_minus': interference_minus,
        'fft_plus': positive_fft_plus, 'fft_minus': positive_fft_minus,
        'twins': twins
    }


# Running
if __name__ == "__main__":
    print("Starting advanced wave analysis...")
    print("=" * 60)
   
    # Analysis with different limits
    for limit in [200, 1000]:
        results = wave_analysis_advanced(limit=limit)
       
        # Additional question for continuation
        if limit == 200:
            print("\n" + "=" * 60)
            response = input("Do you want to see detailed FFT peak analysis? (y/n): ")
            if response.lower() == 'y':
                print("\n📈 DETAILED FFT ANALYSIS:")
                freqs = np.fft.fftfreq(len(results['interference_plus']))
                positive_freqs = freqs[:len(freqs)//2]
                peaks, _ = find_peaks(results['fft_plus'], height=np.max(results['fft_plus'])*0.1)
               
                print("Peaks in the 6n+1 spectrum (frequencies):")
                for peak in peaks[:10]:
                    freq = positive_freqs[peak]
                    print(f" - {freq:.4f} (1/{1/freq:.1f})")