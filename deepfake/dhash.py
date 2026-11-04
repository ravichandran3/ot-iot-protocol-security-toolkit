# dhash.py - perceptual hashing to cluster near-duplicate media without metadata.
import numpy as np

SIZE = 8


def scene(seed: int, shift: int = 0, noise: float = 0.0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    x = np.linspace(0, 1, 64)
    img = np.outer(np.sin(6 * x + rng.uniform(0, 3)), np.cos(4 * x))
    img = img + 0.3 * rng.normal(size=(64, 64))
    img[24 + shift:44 + shift, 20:40] += 1.5
    return img + noise * rng.normal(size=(64, 64))


def dhash(img: np.ndarray, size: int = SIZE) -> int:
    h, w = img.shape
    small = img.reshape(size, h // size, size, w // size).mean(axis=(1, 3))
    bits = (small[:, 1:] > small[:, :-1]).flatten()
    return sum(int(b) << i for i, b in enumerate(bits))


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def main():
    seeds = (11, 22, 33)
    hashes, truth = [], []
    for group, seed in enumerate(seeds):
        for variant in range(4):
            hashes.append(dhash(scene(seed, shift=variant, noise=0.05 * variant)))
            truth.append(group)

    print("images", len(hashes), "scenes", len(seeds), "variants 4")
    print("hash[0] 0x%016x hash[4] 0x%016x hash[8] 0x%016x" %
          (hashes[0], hashes[4], hashes[8]))

    intra = [hamming(hashes[i], hashes[j]) for i in range(len(hashes))
             for j in range(i + 1, len(hashes)) if truth[i] == truth[j]]
    inter = [hamming(hashes[i], hashes[j]) for i in range(len(hashes))
             for j in range(i + 1, len(hashes)) if truth[i] != truth[j]]
    print("max intra-cluster distance", max(intra))
    print("min inter-cluster distance", min(inter))

    times = [1_760_000_000 + g * 420 + v * 90
             for g in range(len(seeds)) for v in range(4)]

    threshold = 8
    clusters, seen = [], set()
    for i in range(len(hashes)):
        if i in seen:
            continue
        group = [j for j in range(len(hashes)) if hamming(hashes[i], hashes[j]) <= threshold]
        seen |= set(group)
        clusters.append(group)
    print("clusters", clusters)
    for c in clusters:
        span = max(times[j] for j in c) - min(times[j] for j in c)
        print(f"cluster {c} accounts {len(c)} upload_span_s {span}")


if __name__ == "__main__":
<<<<<<< HEAD
    main()

=======
    main()

>>>>>>> d160e37 (Add toolkit files)
