import statistics, string
import timing
from timing import naive_compare, SECRET
pc = timing.pc
ALPHA = (string.ascii_lowercase + string.digits).encode()
timing.WORK = 800
def measure(fn, g, s, reps=10, passes=10):
    best=None
    for _ in range(passes):
        t0=pc()
        for _ in range(reps): fn(g,s)
        dt=pc()-t0
        best=dt if best is None else min(best,dt)
    return best/reps
for _ in range(2000): naive_compare(b"x"*8, SECRET)
known=b""; slots=[]
for pos in range(8):
    times={c: measure(naive_compare, known+bytes([c])+b"\x00"*(7-pos), SECRET) for c in ALPHA}
    ranked=sorted(times.items(), key=lambda kv:-kv[1])
    med=statistics.median(times.values()); sd=statistics.pstdev(times.values()) or 1
    known+=bytes([ranked[0][0]])
    slots.append((ranked[0][0], times[SECRET[pos]]/med, (times[SECRET[pos]]-med)/sd, ranked[0][1]-ranked[1][1]))
    print(f"pos {pos} true={chr(SECRET[pos])!r} picked={chr(ranked[0][0])!r} z={(times[SECRET[pos]]-med)/sd:+.1f} gap={ranked[0][1]-ranked[1][1]:.0f}ns")
print("recovered", known, "correct", known==SECRET)
