import math, string
from crypt import PLAIN, ENGLISH, vigenere, xor, hamming

TOTAL = sum(ENGLISH.values())
PROB = {k: v / TOTAL for k, v in ENGLISH.items()}


def letters(text):
    return "".join(c for c in text.lower() if c in string.ascii_lowercase)


def ic(text):
    t = letters(text); n = len(t)
    if n < 2: return 0.0
    return sum(t.count(c) * (t.count(c) - 1) for c in set(t)) / (n * (n - 1))


ct = letters(vigenere(PLAIN, "LEMON"))
print("letters", len(ct), "IC", round(ic(ct), 4))
cols = []
for L in range(1, 21):
    ics = [ic(ct[i::L]) for i in range(L)]
    cols.append((sum(ics) / L, L))
for s, L in sorted(cols, reverse=True)[:6]:
    print(f"  L={L:2d} IC={s:.4f}")
