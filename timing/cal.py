import time
from timing import naive_compare, SECRET
t0=time.perf_counter()
for _ in range(10000):
    naive_compare(b"Tr0ub4dX", SECRET)
print("10000 compares", time.perf_counter()-t0, "s")
t0=time.perf_counter()
from timing import burn
for _ in range(10000):
    burn()
print("10000 burns", time.perf_counter()-t0, "s")
