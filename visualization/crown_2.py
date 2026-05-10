# Copyright (c) 2026 Stefka Georgieva
# Licensed under CC BY-NC-ND 4.0 with Additional Commercial Terms.
# Contact: georgieva@vpr-research.eu or vpr.model@gmail.com for licensing inquiries.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.spatial import ConvexHull
from scipy.interpolate import make_interp_spline

def crown_of_primes(limit=500):
    """Visualization of the 'Crown of Primes'"""
   
    def sieve_primes(limit):
        sieve = np.ones(limit + 1, dtype=bool)
        sieve[0:2] = False
        for i in range(2, int(limit**0.5) + 1):
            if sieve[i]:
                sieve[i*i:limit+1:i] = False
        return np.where(sieve)[0]
   
    all_primes = sieve_primes(limit)
   
    # Analysis of both sequences
    max_n_plus = (limit - 1) // 6
    n_plus = np.arange(1, max_n_plus + 1)
    numbers_plus = 6 * n_plus + 1
   
    max_n_minus = (limit + 1) // 6
    n_minus = np.arange(1, max_n_minus + 1)
    numbers_minus = 6 * n_minus - 1
   
    # Finding prime numbers
    is_prime_plus = np.ones(len(numbers_plus), dtype=bool)
    is_prime_minus = np.ones(len(numbers_minus), dtype=bool)
   
    for p in all_primes:
        p_int = int(p)
        if p_int < 5:
            continue
       
        # For 6n+1
        try:
            inv6 = pow(6, -1, p_int)
            n0 = ((-1) * inv6) % p_int
            if n0 == 0:
                n0 = p_int
        except ValueError:
            continue
       
        first_n = n0
        if first_n <= max_n_plus and 6*first_n + 1 == p_int:
            first_n = n0 + p_int
       
        for n in range(first_n, max_n_plus + 1, p_int):
            if n-1 < len(is_prime_plus):
                is_prime_plus[n-1] = False
       
        # For 6n-1
        try:
            n0 = (1 * inv6) % p_int
            if n0 == 0:
                n0 = p_int
        except ValueError:
            continue
       
        first_n = n0
        if first_n <= max_n_minus and 6*first_n - 1 == p_int:
            first_n = n0 + p_int
       
        for n in range(first_n, max_n_minus + 1, p_int):
            if n-1 < len(is_prime_minus):
                is_prime_minus[n-1] = False
   
    # Get the coordinates
    primes_plus = numbers_plus[is_prime_plus]
    primes_minus = numbers_minus[is_prime_minus]
   
    # Create the figure
    fig = plt.figure(figsize=(18, 12))
   
    # 1. THE CROWN - main visualization
    ax1 = plt.subplot(2, 3, 1, projection='polar')
   
    # Convert numbers to polar coordinates
    r_plus = primes_plus / max(primes_plus.max(), primes_minus.max())
    theta_plus = np.linspace(0, np.pi, len(primes_plus))
   
    r_minus = primes_minus / max(primes_plus.max(), primes_minus.max())
    theta_minus = np.linspace(np.pi, 2*np.pi, len(primes_minus))
   
    ax1.scatter(theta_plus, r_plus, c='red', s=10, alpha=0.7, label='6n+1')
    ax1.scatter(theta_minus, r_minus, c='blue', s=10, alpha=0.7, label='6n-1')
   
    # Connect symmetric points
    min_len = min(len(primes_plus), len(primes_minus))
    for i in range(min_len):
        ax1.plot([theta_plus[i], theta_minus[i]], [r_plus[i], r_minus[i]],
                'gray', linewidth=0.3, alpha=0.3)
   
    ax1.set_title('👑 Crown of Primes', fontsize=14, pad=20)
    ax1.legend(loc='upper right')
   
    # 2. SYMMETRIC TRIANGLES
    ax2 = plt.subplot(2, 3, 2)
   
    # Create "triangles" using points and their mirror reflections
    x_plus = primes_plus
    y_plus = np.sin(np.linspace(0, np.pi, len(primes_plus)))
   
    x_minus = primes_minus
    y_minus = -np.sin(np.linspace(0, np.pi, len(primes_minus)))
   
    ax2.scatter(x_plus, y_plus, c='red', s=15, alpha=0.7, label='6n+1 (Upper Crown)')
    ax2.scatter(x_minus, y_minus, c='blue', s=15, alpha=0.7, label='6n-1 (Lower Crown)')
   
    # Connect points to form triangles
    for i in range(min_len):
        ax2.plot([x_plus[i], x_minus[i]], [y_plus[i], y_minus[i]],
                'purple', linewidth=0.5, alpha=0.3)
   
    ax2.set_xlabel('Number')
    ax2.set_ylabel('Amplitude')
    ax2.set_title('🔺 Symmetric Triangles (Crown and Reflection)', fontsize=12)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
   
    # 3. FRACTAL STRUCTURE - self-similarity
    ax3 = plt.subplot(2, 3, 3)
   
    # Divide into segments and look for self-similarity
    segment_size = 50
    segments = []
    for i in range(0, len(primes_plus), segment_size):
        segment = primes_plus[i:i+segment_size]
        if len(segment) > 10:
            segments.append(segment)
   
    for i, seg in enumerate(segments[:5]):
        normalized = (seg - seg.min()) / (seg.max() - seg.min())
        ax3.plot(normalized + i, 'o-', alpha=0.6, label=f'Segment {i+1}')
   
    ax3.set_title('🌿 Fractal Structure (Self-Similarity)', fontsize=12)
    ax3.set_xlabel('Position in Segment')
    ax3.set_ylabel('Normalized Value')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
   
    # 4. SPECTRAL CROWN - FFT in wave form
    ax4 = plt.subplot(2, 3, 4)
   
    # Create a complex signal from both sequences
    signal = np.zeros(max(len(primes_plus), len(primes_minus)))
    signal[:len(primes_plus)] = np.sin(primes_plus / 100)
    signal[:len(primes_minus)] += np.cos(primes_minus / 100)
   
    fft_signal = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal))
   
    ax4.plot(freqs[:len(freqs)//2], np.abs(fft_signal[:len(fft_signal)//2]),
            'gold', linewidth=1.5, alpha=0.8)
    ax4.fill_between(freqs[:len(freqs)//2], 0, np.abs(fft_signal[:len(fft_signal)//2]),
                     alpha=0.3, color='gold')
    ax4.set_xlabel('Frequency')
    ax4.set_ylabel('Spectral Power')
    ax4.set_title('📡 Spectral Crown (Frequency Comb)', fontsize=12)
    ax4.grid(True, alpha=0.3)
   
    # 5. CONCENTRIC CIRCLES - new metaphor
    ax5 = plt.subplot(2, 3, 5, projection='polar')
   
    # Represent primes as concentric circles
    radii = np.sqrt(primes_plus[:200])  # first 200 primes
    angles = np.linspace(0, 2*np.pi, len(radii))
   
    ax5.scatter(angles, radii, c=primes_plus[:200] % 360,
               s=20, cmap='viridis', alpha=0.7)
    ax5.set_title('🎯 Primes as Concentric Circles', fontsize=12)
   
    # 6. DENSITY AND RHYTHM - wave model
    ax6 = plt.subplot(2, 3, 6)
   
    # Create a "sound wave" from the prime numbers
    # Each prime generates a wave packet
    t = np.linspace(0, 2*np.pi, 1000)
    sound_wave = np.zeros(1000)
   
    for p in primes_plus[:50]:  # first 50 primes
        freq = 50 / p
        wave = np.sin(freq * t * 2*np.pi) * np.exp(-((t - np.pi)**2) / 2)
        sound_wave += wave
   
    ax6.plot(t, sound_wave / np.max(np.abs(sound_wave)), 'purple', linewidth=1)
    ax6.fill_between(t, -0.5, sound_wave / np.max(np.abs(sound_wave)),
                     alpha=0.3, color='violet')
    ax6.set_xlabel('Time')
    ax6.set_ylabel('Amplitude')
    ax6.set_title('🎵 Sound of Prime Numbers (Wave Superposition)', fontsize=12)
    ax6.grid(True, alpha=0.3)
   
    plt.suptitle('👑 CROWN OF PRIMES 👑\nTwo Symmetric Triangles - Crown and Reflection',
                 fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.show()
   
    # Additional 3D visualization of the "crown"
    fig_3d = plt.figure(figsize=(14, 10))
    ax_3d = fig_3d.add_subplot(111, projection='3d')
   
    # Create 3D crown
    theta = np.linspace(0, 2*np.pi, max(len(primes_plus), len(primes_minus)))
    r_3d = np.ones_like(theta)
   
    z_plus = np.zeros(len(primes_plus))
    z_minus = np.zeros(len(primes_minus))
   
    x_3d_plus = primes_plus * np.cos(np.linspace(0, np.pi, len(primes_plus)))
    y_3d_plus = primes_plus * np.sin(np.linspace(0, np.pi, len(primes_plus)))
    z_3d_plus = np.ones(len(primes_plus))
   
    x_3d_minus = primes_minus * np.cos(np.linspace(np.pi, 2*np.pi, len(primes_minus)))
    y_3d_minus = primes_minus * np.sin(np.linspace(np.pi, 2*np.pi, len(primes_minus)))
    z_3d_minus = -np.ones(len(primes_minus))
   
    ax_3d.scatter(x_3d_plus, y_3d_plus, z_3d_plus, c='red', s=20, alpha=0.7, label='6n+1 (Upper Crown)')
    ax_3d.scatter(x_3d_minus, y_3d_minus, z_3d_minus, c='blue', s=20, alpha=0.7, label='6n-1 (Lower Crown)')
   
    # Connect both halves
    min_3d = min(len(x_3d_plus), len(x_3d_minus))
    for i in range(min_3d):
        ax_3d.plot([x_3d_plus[i], x_3d_minus[i]],
                  [y_3d_plus[i], y_3d_minus[i]],
                  [z_3d_plus[i], z_3d_minus[i]],
                  'gray', alpha=0.3, linewidth=0.5)
   
    ax_3d.set_title('👑 3D CROWN - Symmetry of Prime Numbers', fontsize=14)
    ax_3d.set_xlabel('X')
    ax_3d.set_ylabel('Y')
    ax_3d.set_zlabel('Z')
    ax_3d.legend()
   
    plt.tight_layout()
    plt.show()
   
    # Beauty statistics
    print(f"\n{'='*60}")
    print(f"👑 CROWN STATISTICS 👑")
    print(f"{'='*60}")
    print(f"📊 Total primes up to {limit}: {len(primes_plus) + len(primes_minus)}")
    print(f"📊 Upper Crown (6n+1): {len(primes_plus)} primes")
    print(f"📊 Lower Crown (6n-1): {len(primes_minus)} primes")
    print(f"📊 Symmetry: {abs(len(primes_plus) - len(primes_minus))} difference")
    print(f"🎯 Crown Perfection: {min(len(primes_plus), len(primes_minus)) / max(len(primes_plus), len(primes_minus)) * 100:.2f}%")
   
    # Beautiful ASCII art crown
    print(f"\n{'🎭'*30}")
    print("👑 CROWN IN ASCII ART:")
    crown_ascii = [
        " ★ ",
        " ★ ★ ",
        " ★ ★ ",
        " ★ ★ ",
        " ★ ★ ",
        " ★ ★ ",
        "★ ★",
        " ☆ ☆ ",
        " ☆ ☆ ",
        " ☆ "
    ]
    for line in crown_ascii:
        print(line)
    print(f"{'🎭'*30}")
   
    return primes_plus, primes_minus


# Running
if __name__ == "__main__":
    print("👑 Starting the construction of the CROWN OF PRIMES 👑")
    print("=" * 60)
   
    # Choose crown size
    try:
        limit = int(input("Up to which number should the crown be built? (recommended: 500-2000): ") or 1000)
    except:
        limit = 1000
   
    primes_plus, primes_minus = crown_of_primes(limit=limit)
   
    print(f"\n✨ The Crown is complete! ✨")
    print(f"👑 {len(primes_plus)} pearls in the upper crown")
    print(f"👑 {len(primes_minus)} pearls in the lower crown")
    print(f"💎 Total pearls: {len(primes_plus) + len(primes_minus)}")