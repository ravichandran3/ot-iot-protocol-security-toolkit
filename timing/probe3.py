import statistics, time, random, string
from timing import naive_compare, SECRET
pc = time.perf_counter_ns
ALPHA = (string.ascii_letters + string.digits).encode()

def paired(fn, a, ref, secret, n=40):
    ds = []
    for i in range(n):
        if i % 2 == 0:
            t0 = pc(); fn(a, secret); t1 = pc(); fn(ref, secret); t2 = pc()
            ds.append((t1 - t0) - (t2 - t1))
        else:
            t0 = pc(); fn(ref, secret); t1 = pc(); fn(a, secret); t2 = pc()
            ds.append((t2 - t1) - (t1 - t0))
    return statistics.median(ds)

for _ in range(2000): naive_compare(b"xxxxxxxx", SECRET)
ref = b"\x00" * len(SECRET)
for pos in (1, 3, 7):
    known = SECRET[:pos]
    scores = {}
    order = list(ALPHA); random.shuffle(order)
    for cand in order:
        g = known + bytes([cand]) + b"\x00" * (len(SECRET)-pos-1)
        scores[cand] = paired(naive_compare, g, ref, SECRET, 40)
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    med = statistics.median(scores.values()); sd = statistics.pstdev(scores.values()) or 1
    print(f"pos {pos}: rank {[k for k,_ in ranked].index(SECRET[pos])+1}/{len(ALPHA)} z={(scores[SECRET[pos]]-med)/sd:+.1f} correct={scores[SECRET[pos]]/1000:.0f}us top={ranked[0][0]:#04x} top_d={ranked[0][1]/1000:.0f}us second={ranked[1][1]/1000:.0f}us")
