# crypt.py - Vigenere and repeating-key XOR recovered from the ciphertext alone.
import string

PLAIN = (
    "the landing station operator noticed the link was down at zero four hundred "
    "and reported it to the network operations centre which opened a ticket and "
    "escalated it to the shift supervisor who then called the vendor hotline and "
    "waited for a call back that arrived after the maintenance window had closed "
    "so the fault was carried overnight and resolved the following morning when "
    "the replacement line card was installed and the link was tested end to end"
).replace("\n", " ")

ENGLISH = {
    "a": 8.17, "b": 1.49, "c": 2.78, "d": 4.25, "e": 12.70, "f": 2.23,
    "g": 2.02, "h": 6.09, "i": 6.97, "j": 0.15, "k": 0.77, "l": 4.03,
    "m": 2.41, "n": 6.75, "o": 7.51, "p": 1.93, "q": 0.10, "r": 5.99,
    "s": 6.33, "t": 9.06, "u": 2.76, "v": 0.98, "w": 2.36, "x": 0.15,
    "y": 1.97, "z": 0.07, " ": 18.0,
}


def vigenere(text: str, key: str, sign: int = 1) -> str:
    out, j = [], 0
    for ch in text:
        if ch.isalpha():
            k = ord(key[j % len(key)].lower()) - 97
            out.append(chr((ord(ch.lower()) - 97 + sign * k) % 26 + 97))
            j += 1
        else:
            out.append(ch)
    return "".join(out)


def ic(text: str) -> float:
    letters = [c for c in text if c in string.ascii_lowercase]
    n = len(letters)
    if n < 2:
        return 0.0
    counts = {c: letters.count(c) for c in set(letters)}
    return sum(v * (v - 1) for v in counts.values()) / (n * (n - 1))


def vigenere_key_lengths(ct: str, max_len: int = 20):
    scores = []
    for length in range(1, max_len + 1):
        cols = ["".join(ct[i::length]) for i in range(length)]
        scores.append((sum(ic(c) for c in cols) / length, length))
    return sorted(scores, reverse=True)


def chi_square(text: str) -> float:
    letters = [c for c in text.lower() if c in ENGLISH]
    n = len(letters) or 1
    score = 0.0
    for ch, expected in ENGLISH.items():
        observed = letters.count(ch)
        score += (observed - n * expected / 100) ** 2 / (n * expected / 100)
    return score


def vigenere_recover_key(ct: str, length: int) -> str:
    key = ""
    for i in range(length):
        col = ct[i::length]
        best = min(range(26), key=lambda s: chi_square(vigenere(col, chr(97 + s), -1)))
        key += chr(97 + best)
    return key


def xor(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def text_score(data: bytes) -> float:
    """English-ness of raw bytes; non-printable bytes are heavily penalised."""
    bad = sum(1 for b in data if not (32 <= b <= 126))
    return chi_square(data.decode("latin-1")) + 100.0 * bad


def hamming(a: bytes, b: bytes) -> int:
    return sum(bin(x ^ y).count("1") for x, y in zip(a, b))


def xor_key_lengths(ct: bytes, max_len: int = 20):
    scores = []
    for length in range(1, max_len + 1):
        blocks = [ct[i:i + length] for i in range(0, len(ct) - length, length)]
        pairs = [(blocks[i], blocks[i + 1]) for i in range(len(blocks) - 1)]
        dist = sum(hamming(a, b) / length for a, b in pairs) / max(len(pairs), 1)
        scores.append((dist, length))
    return sorted(scores)


def xor_recover_key(ct: bytes, length: int) -> bytes:
    key = bytearray()
    for i in range(length):
        col = ct[i::length]
        best = min(range(32, 127), key=lambda k: text_score(bytes(b ^ k for b in col)))
        key.append(best)
    return bytes(key)


if __name__ == "__main__":
    ct = vigenere(PLAIN, "LEMON")
    print("plaintext", len(PLAIN), "chars; vigenere ciphertext", len(ct), "chars")
    print("cipher head", ct[:44])
    print("IC of ciphertext %.4f (English ~0.066, random ~0.038)" % ic(ct))

    top = vigenere_key_lengths(ct)[:3]
    print("vigenere key-length candidates", [(l, round(s, 4)) for s, l in top])
    vkey = vigenere_recover_key(ct, top[0][1])
    print("vigenere recovered key", vkey, "correct", vkey == "lemon",
          "plaintext match", vigenere(ct, vkey, -1) == PLAIN)

    data = PLAIN.encode()
    ct2 = xor(data, b"operator")
    print("xor ciphertext", len(ct2), "bytes")
    best = xor_key_lengths(ct2)[:3]
    print("xor hamming candidates", [(l, round(s, 3)) for s, l in best])
    scored = sorted(((text_score(xor(ct2, xor_recover_key(ct2, L))), L) for L in range(1, 21)))
    print("xor validated lengths", [(L, round(s, 1)) for s, L in scored[:3]])
    xkey = xor_recover_key(ct2, scored[0][1])
    print("xor recovered key", xkey, "correct", xkey == b"operator",
          "plaintext match", xor(ct2, xkey) == data)

    short = vigenere(PLAIN[:24], "LEMON")
    print("short ciphertext", len(short), "chars -> IC best length",
          vigenere_key_lengths(short)[0][1], "(true 6)")
