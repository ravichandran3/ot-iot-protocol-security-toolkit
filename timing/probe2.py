import statistics, time, random
from timing import naive_compare, constant_compare, SECRET
pc = time.perf_counter_ns

def paired(fn, a, b, ref, secret, n=20):
    d = 0
    for i in range(n):
        if i % 2 == 0:
            t0 = pc(); fn(a, secret); t1 = pc(); fn(ref, secret); t2 = pc()
            d += (t1 - t0) - (t2 - t1)
        else:
            t0 = pc(); fn(ref, secret); t1 = pc(); fn(a, secret); t2 = pc()
            d += (t2 - t1) - (t1 - t0)
    return d / n

for _ in range(2000): naive_compare(b"xxxxxxxx", SECRET)
ref = b"\x00" * len(SECRET)
for pos in (0, 3, 7):
    known = SECRET[:pos]
    scores = {}
    order = list(range(256)); random.shuffle(order)
    for cand in order:
        g = known + bytes([cand]) + b"\x00" * (len(SECRET)-pos-1)
        scores[cand] = paired(naive_compare, g, SECRET, ref, SECRET, 20)
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    med = statistics.median(scores.values()); sd = statistics.pstdev(scores.values())
    print(f"pos {pos}: correct rank {[k for k,_ in ranked].index(SECRET[pos])+1} z={(scores[SECRET[pos]]-med)/sd:+.1f} top={ranked[0][0]:#04x} correct_d={scores[SECRET[pos]]:.0f}ns top_d={ranked[0][1]:.0f}ns")
