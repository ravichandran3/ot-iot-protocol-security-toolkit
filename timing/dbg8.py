import statistics
from timing import naive_compare, measure, SECRET, ALPHA
known = SECRET[:7]
times = {}
for cand in ALPHA:
    times[cand] = measure(naive_compare, known + bytes([cand]), SECRET)
ranked = sorted(times.items(), key=lambda kv: -kv[1])
print("true", SECRET[7], times[SECRET[7]]/1000)
for c, t in ranked[:5]:
    print(f"  {chr(c)!r} {t/1000:.0f}us")
