# arinc.py - ARINC 429 word and MIL-STD-1553 command word, encode + decode.
def getf(word: int, hi: int, lo: int) -> int:
    return (word >> (lo - 1)) & ((1 << (hi - lo + 1)) - 1)


def setf(word: int, hi: int, lo: int, value: int) -> int:
    width = hi - lo + 1
    mask = ((1 << width) - 1) << (lo - 1)
    return (word & ~mask) | ((value & ((1 << width) - 1)) << (lo - 1))


def rev8(value: int) -> int:
    return int(f"{value:08b}"[::-1], 2)


def odd_parity(value: int, nbits: int) -> int:
    return 0 if bin(value & ((1 << nbits) - 1)).count("1") % 2 else 1


def arinc429(label: int, sdi: int, data: int, ssm: int) -> int:
    word = 0
    word = setf(word, 8, 1, rev8(label))
    word = setf(word, 10, 9, sdi)
    word = setf(word, 28, 11, data)
    word = setf(word, 30, 29, ssm)
    word = setf(word, 31, 31, odd_parity(getf(word, 30, 1), 30))
    return word


def parse429(word: int):
    return {"label": rev8(getf(word, 8, 1)),
            "sdi": getf(word, 10, 9),
            "data": getf(word, 28, 11),
            "ssm": getf(word, 30, 29),
            "parity_ok": bin(word & 0x7FFFFFFF).count("1") % 2 == 1}


def bnr(raw: int, resolution: float, bits: int = 18) -> float:
    sign = -1 if raw & (1 << (bits - 1)) else 1
    magnitude = raw & ((1 << (bits - 1)) - 1)
    return sign * magnitude * resolution


def mil1553(rt: int, tx: int, subaddr: int, count: int) -> int:
    word = 0
    word = setf(word, 3, 1, 0b100)          # command sync
    word = setf(word, 8, 4, rt)
    word = setf(word, 9, 9, tx)
    word = setf(word, 14, 10, subaddr)
    word = setf(word, 19, 15, count)
    word = setf(word, 20, 20, odd_parity(getf(word, 19, 1), 19))
    return word


def parse1553(word: int):
    return {"sync": getf(word, 3, 1), "rt": getf(word, 8, 4),
            "tx": getf(word, 9, 9), "subaddr": getf(word, 14, 10),
            "count": getf(word, 19, 15),
            "parity_ok": bin(word).count("1") % 2 == 1}


if __name__ == "__main__":
    w = arinc429(0o203, 0, 350, 0b11)
    p = parse429(w)
    print("ARINC429 word 0x%08x label=%03o sdi=%d ssm=%d altitude=%d ft parity_ok=%s" %
          (w, p["label"], p["sdi"], p["ssm"], bnr(p["data"], 100), p["parity_ok"]))

    forged = setf(w, 28, 11, 3500)           # 350,000 ft, parity untouched
    print("forged, parity untouched -> altitude=%d ft parity_ok=%s" %
          (bnr(parse429(forged)["data"], 100), parse429(forged)["parity_ok"]))

    forged_ok = arinc429(0o203, 0, 3500, 0b11)
    print("forged, parity rebuilt   -> altitude=%d ft parity_ok=%s" %
          (bnr(parse429(forged_ok)["data"], 100), parse429(forged_ok)["parity_ok"]))

    c = mil1553(31, 0, 0, 1)
    print("1553 cmd 0x%04x" % c, parse1553(c))

