# feed.py - ranking exposure before, during and after a sockpuppet boost.
import numpy as np

N = 40
USERS = 200
TARGET = 7


def top(engagements, k=10):
    return sorted(range(len(engagements)), key=lambda i: -engagements[i])[:k]


def rank_of(engagements, item):
    return sorted(range(len(engagements)), key=lambda i: -engagements[i]).index(item) + 1


def main():
    rng = np.random.default_rng(5)
    organic = rng.integers(20, 120, N).astype(int)
    organic[TARGET] = int(np.median(organic))

    baseline = organic.copy()
    boosted = organic.copy()
    sockpuppets = 60
    boosted[TARGET] += sockpuppets

    trust = organic.copy()
    trust[TARGET] = organic[TARGET]

    print(f"items {N} users {USERS} sockpuppets {sockpuppets}")
    print(f"baseline  rank {rank_of(baseline, TARGET):2d} engagements {baseline[TARGET]:3d}")
    print(f"boosted   rank {rank_of(boosted, TARGET):2d} engagements {boosted[TARGET]:3d}")
    print(f"filtered  rank {rank_of(trust, TARGET):2d} engagements {trust[TARGET]:3d}")

    share = sockpuppets / boosted[TARGET]
    print(f"sockpuppet share of target engagements {share:.3f}")
    print("top10 before", top(baseline))
    print("top10 after ", top(boosted))
    print("top10 overlap", len(set(top(baseline)) & set(top(boosted))), "of 10")


if __name__ == "__main__":
<<<<<<< HEAD
    main()

=======
    main()

>>>>>>> d160e37 (Add toolkit files)
