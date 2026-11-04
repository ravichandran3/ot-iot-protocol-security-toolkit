import statistics, time, random
from timing import naive_compare, constant_compare, burn, SECRET

def measure(fn, a, b, passes, reps):
    ts = []
    for _ in range(passes):
        t0 = time.perf_counter_ns()
        for _ in range(reps):
            fn(a, b)
        ts.append(time.perf_counter_ns() - t0)
    return statistics.median(ts)

for _ in range(3000): naive_compare(b"xxxxxxxx", SECRET)
for _ in range(3000): constant_compare(b"xxxxxxxx", SECRET)

for pos in (0, 3, 7):
    known = SECRET[:pos]
    samples = {}
    order = list(range(256)); random.shuffle(order)
    for cand in order:
        g = known + bytes([cand]) + b"\x00" * (len(SECRET)-pos-1)
        samples[cand] = measure(naive_compare, g, SECRET, 7, 10)
    med = statistics.median(samples.values())
    sd = statistics.pstdev(samples.values())
    good = samples[SECRET[pos]]
    ranked = sorted(samples.items(), key=lambda kv: -kv[1])
    print(f"pos {pos}: correct {SECRET[pos]:#04x} t={good} med={med:.0f} z={(good-med)/sd:+.2f} rank={[k for k,_ in ranked].index(SECRET[pos])+1} top={ranked[0][0]:#04x} top_ratio={ranked[0][1]/med:.2f}")
