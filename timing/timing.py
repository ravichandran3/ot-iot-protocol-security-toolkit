# timing.py - byte-at-a-time timing attack on a naive compare, then the fix.
import hmac
import statistics
import string
import time

SECRET = b"tr0ub4do"
ALPHA = (string.ascii_lowercase + string.digits).encode()
WORK = 800
REPS = 10
PASSES = 10
pc = time.perf_counter_ns


def burn(n=WORK):
    x = 1
    for _ in range(n):
        x = (x * 1103515245 + 12345) & 0x7FFFFFFF
    return x


def naive_compare(a: bytes, b: bytes) -> bool:
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if x != y:
            return False
        burn()
    return True


def constant_compare(a: bytes, b: bytes) -> bool:
    if len(a) != len(b):
        return False
    diff = 0
    for x, y in zip(a, b):
        diff |= x ^ y
        burn()
    return diff == 0


def measure(fn, guess: bytes, secret: bytes) -> float:
    best = None
    for _ in range(PASSES):
        t0 = pc()
        for _ in range(REPS):
            fn(guess, secret)
        dt = pc() - t0
        best = dt if best is None else min(best, dt)
    return best / REPS


def attack(compare, secret: bytes, alphabet=ALPHA):
    for _ in range(2000):
        compare(b"x" * len(secret), secret)
    known, stats = b"", []
    for pos in range(len(secret)):
        times = {}
        for cand in alphabet:
            guess = known + bytes([cand]) + b"\x00" * (len(secret) - pos - 1)
            times[cand] = measure(compare, guess, secret)
        ranked = sorted(times.items(), key=lambda kv: -kv[1])
        med = statistics.median(times.values())
        sd = statistics.pstdev(times.values()) or 1.0
        known += bytes([ranked[0][0]])
        stats.append((ranked[0][0], times[secret[pos]] / med,
                      (times[secret[pos]] - med) / sd, ranked[0][1] - ranked[1][1]))
    return known, stats


if __name__ == "__main__":
    print(f"secret {len(SECRET)} bytes, alphabet {len(ALPHA)}, work {WORK}, "
          f"{REPS} reps x {PASSES} passes")
    recovered, st = attack(naive_compare, SECRET)
    print("naive      recovered", recovered, "correct", recovered == SECRET)
    print("naive      per-byte lift", " ".join(f"{l:.2f}x" for _, l, _, _ in st))
    print("naive      per-byte z   ", " ".join(f"{z:+.1f}" for _, _, z, _ in st))
    print("naive      last-byte gap %.0f ns" % st[-1][3])

    hard, hs = attack(constant_compare, SECRET)
    print("constant   recovered", hard, "correct", hard == SECRET)
    print("constant   per-byte lift", " ".join(f"{l:.2f}x" for _, l, _, _ in hs))
    print("constant   per-byte z   ", " ".join(f"{z:+.1f}" for _, _, z, _ in hs))
    print("constant   last-byte gap %.0f ns" % hs[-1][3])

    ok = all(constant_compare(SECRET[:i] + bytes([SECRET[i] ^ 1]) + SECRET[i + 1:], SECRET) is False
             for i in range(len(SECRET)))
    print("constant   rejects every single-byte mutation", ok)
    print("hmac       compare_digest agrees", hmac.compare_digest(SECRET, SECRET),
          hmac.compare_digest(SECRET, SECRET[:-1] + b"x"))

