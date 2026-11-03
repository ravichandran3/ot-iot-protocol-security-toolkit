# synth.py - order-level screening bypass by fragmenting a sequence below the k-mer length.
from Bio.Seq import Seq

K = 40
SIGNATURE = (
    "ATGGCGTTACCGGATCCGTTAGCGTAGCTA"
    "GCTAGGCTATTCAGGATCCGTTAGCGTAGC"
    "TAGCTAGGCTACCGATGTAGCTAGGGCTAG"
    "CATCGATCGGGCTAGCTAGCTAGGCTATAA"
)


def kmers(seq: str, k: int = K) -> set:
    return {seq[i:i + k] for i in range(len(seq) - k + 1)}


def screen(seq: str) -> int:
    return len(kmers(seq) & kmers(SIGNATURE))


def assemble(fragments, min_overlap: int = 10):
    pool = [f for f in fragments]
    result = pool.pop(0)
    while pool:
        best, best_len, best_side = None, 0, None
        for frag in pool:
            for length in range(min(len(result), len(frag)), min_overlap - 1, -1):
                if result[-length:] == frag[:length] and length > best_len:
                    best, best_len, best_side = frag, length, "right"
                if frag[-length:] == result[:length] and length > best_len:
                    best, best_len, best_side = frag, length, "left"
        if best is None:
            raise ValueError("fragments do not overlap")
        result = result + best[best_len:] if best_side == "right" else best[:-best_len] + result
        pool.remove(best)
    return result


if __name__ == "__main__":
    print("signature", len(SIGNATURE), "bp; screen k =", K)
    print(f"full order      shared={screen(SIGNATURE):3d} -> "
          f"{'blocked' if screen(SIGNATURE) else 'released'}")

    starts = (0, 20, 40, 60, 80, 100)
    fragments = [SIGNATURE[i:i + 35] for i in starts]
    for n, frag in enumerate(fragments):
        shared = screen(frag)
        print(f"fragment {n} {len(frag):2d} bp shared={shared:3d} -> "
              f"{'blocked' if shared else 'released'}")

    joined = assemble(fragments)
    print("assembled", len(joined), "bp identical", joined == SIGNATURE,
          "protein identical", str(Seq(joined).translate()) == str(Seq(SIGNATURE).translate()))

    control = SIGNATURE[80:125]
    print(f"control {len(control)} bp shared={screen(control):3d} -> "
          f"{'blocked' if screen(control) else 'released'}")

