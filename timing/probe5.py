import statistics, time, random, string
from timing import naive_compare, SECRET
pc = time.perf_counter_ns
ALPHA = (string.ascii_letters + string.digits).encode()

def measure(fn, a, secret, reps=20, passes=5):
    best = None
    for _ in range(passes):
        t0 = pc()
        for _ in range(reps):
            fn(a, secret)
        dt = pc() - t0
        best = dt if best is None else min(best, dt)
    return best / reps

for _ in range(2000): naive_compare(b"xxxxxxxx", SECRET)
for pos in (0, 3, 7):
    known = SECRET[:pos]
    scores = {}
    order = list(ALPHA); random.shuffle(order)
    for cand in order:
        g = known + bytes([cand]) + b"\x00" * (len(SECRET)-pos-1)
        scores[cand] = measure(naive_compare, g, SECRET)
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    med = statistics.median(scores.values()); sd = statistics.pstdev(scores.values()) or 1
    print(f"pos {pos}: rank {[k for k,_ in ranked].index(SECRET[pos])+1}/{len(ALPHA)} z={(scores[SECRET[pos]]-med)/sd:+.1f} correct={scores[SECRET[pos]]/1000:.0f}us top={ranked[0][0]:#04x} {ranked[0][1]/1000:.0f}us 2nd={ranked[1][1]/1000:.0f}us")
