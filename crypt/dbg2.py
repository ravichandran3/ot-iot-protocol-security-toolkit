from crypt import PLAIN, xor, hamming
ct2 = xor(PLAIN.encode(), b"operator")
def byte_ic(data: bytes) -> float:
    n = len(data)
    if n < 2: return 0.0
    from collections import Counter
    c = Counter(data)
    return sum(v*(v-1) for v in c.values())/(n*(n-1))
print("len  byteIC")
for L in range(1,21):
    cols=[ct2[i::L] for i in range(L)]
    print(f"{L:3d}  {sum(byte_ic(c) for c in cols)/L:.4f}")
