import math
from crypt import PLAIN, ENGLISH, xor
TOTAL = sum(ENGLISH.values()); PROB = {k: v/TOTAL for k, v in ENGLISH.items()}
def cost(data):
    return -sum(math.log(PROB.get(chr(b), 1e-6)) for b in data)
def recover(ct, L):
    key = bytes(min(range(32,127), key=lambda k: cost(bytes(b ^ k for b in ct[i::L]))) for i in range(L))
    return key, cost(xor(ct, key))
ct = xor(PLAIN.encode(), b"operator")
for L in range(1, 21):
    k, c = recover(ct, L)
    if L in (1,2,4,6,8,12,16,20): print(f"L={L:2d} key={k!r:<14} cost={c:9.1f}")
print("best", min((recover(ct,L)[1], L) for L in range(1,21)))
