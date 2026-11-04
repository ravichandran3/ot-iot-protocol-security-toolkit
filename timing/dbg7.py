import statistics
from timing import naive_compare, measure, SECRET, ALPHA
known = SECRET[:7]
for cand in (SECRET[7], ord("y"), ord("a"), ord("Z")):
    g = known + bytes([cand])
    ts = [measure(naive_compare, g, SECRET) for _ in range(5)]
    print(f"{chr(cand)!r} {cand:#04x} {[round(t/1000,1) for t in ts]} us")
