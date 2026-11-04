# gnss.py - GPS C/A code acquisition, jamming and spoofing, at baseband.
import numpy as np

CHIPS = 1023
ACQ_THRESHOLD = 8.0
METRES_PER_CHIP = 293.05          # c / 1.023e6


def ca_code(prn: int = 1) -> np.ndarray:
    """Generate the 1023-chip C/A code for one PRN, as +/-1 floats."""
    taps = {1: (2, 6), 2: (3, 7), 3: (4, 8), 4: (5, 9), 5: (1, 9),
            6: (2, 10), 7: (1, 8), 8: (2, 9), 9: (3, 10), 10: (2, 3)}
    a, b = taps[prn]
    g1, g2, chips = [1] * 10, [1] * 10, []
    for _ in range(CHIPS):
        chips.append(g1[9] ^ g2[a - 1] ^ g2[b - 1] ^ 1)
        fb1 = g1[2] ^ g1[9]
        fb2 = g2[1] ^ g2[2] ^ g2[5] ^ g2[7] ^ g2[8] ^ g2[9]
        g1 = [fb1] + g1[:9]
        g2 = [fb2] + g2[:9]
    return np.array([1.0 if c == 0 else -1.0 for c in chips])


def acquire(signal: np.ndarray, code: np.ndarray):
    """Circular correlation against the local replica; return (lag, peak, ratio)."""
    corr = np.array([np.dot(signal, np.roll(code, lag)) for lag in range(CHIPS)]) / CHIPS
    peak = float(np.max(np.abs(corr)))
    lag = int(np.argmax(np.abs(corr)))
    ratio = peak / (float(np.std(corr)) + 1e-12)
    return lag, peak, ratio


def main():
    rng = np.random.default_rng(7)
    code = ca_code(1)
    print("chips", code.size, "first 10", "".join("1" if c > 0 else "0" for c in code[:10]))

    clean = code.copy()
    lag, peak, ratio = acquire(clean, code)
    print(f"clean   lag={lag:<4d} peak={peak:6.3f} ratio={ratio:8.1f} acquired={ratio > ACQ_THRESHOLD}")

    noisy = code + rng.normal(0, 1.0, CHIPS)
    lag, peak, ratio = acquire(noisy, code)
    print(f"noise 1 lag={lag:<4d} peak={peak:6.3f} ratio={ratio:8.1f} acquired={ratio > ACQ_THRESHOLD}")

    jammed = code + rng.normal(0, 20.0, CHIPS)
    lag, peak, ratio = acquire(jammed, code)
    print(f"jammer  lag={lag:<4d} peak={peak:6.3f} ratio={ratio:8.1f} acquired={ratio > ACQ_THRESHOLD}")

    spoofed = code + 3.0 * np.roll(code, 120) + rng.normal(0, 0.5, CHIPS)
    lag, peak, ratio = acquire(spoofed, code)
    corr = np.array([np.dot(spoofed, np.roll(code, l)) for l in range(CHIPS)]) / CHIPS
    print(f"spoof   lag={lag:<4d} peak={peak:6.3f} ratio={ratio:8.1f} "
          f"offset_km={lag * METRES_PER_CHIP / 1000:.1f}")
    print(f"        authentic={abs(corr[0]):.3f} spoofer={abs(corr[120]):.3f}")


if __name__ == "__main__":
<<<<<<< HEAD
    main()


=======
    main()


>>>>>>> d160e37 (Add toolkit files)
