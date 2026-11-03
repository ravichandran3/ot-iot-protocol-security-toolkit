from crypt import PLAIN, xor, chi_square
def recover(ct, L):
    key = bytes(min(range(256), key=lambda k: chi_square(bytes(b ^ k for b in ct[i::L]).decode("latin-1"))) for i in range(L))
    return key, xor(ct, key)
ct = xor(PLAIN.encode(), b"operator")
print(" L  key            chi2(decrypted)")
for L in range(1, 21):
    k, pt = recover(ct, L)
    print(f"{L:2d}  {k!r:<16} {chi_square(pt.decode('latin-1')):10.1f}")
