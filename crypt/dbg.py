from crypt import PLAIN, vigenere, vigenere_key_lengths, ic, xor, xor_key_lengths, hamming
ct = vigenere(PLAIN, "LEMON")
print("vigenere scores (len, IC):")
for s,l in sorted(vigenere_key_lengths(ct), key=lambda x: x[1]):
    print(f"  {l:2d} {s:.4f}")
data = PLAIN.encode(); ct2 = xor(data, b"operator")
print("xor scores (len, dist):")
for s,l in sorted(xor_key_lengths(ct2), key=lambda x: x[1]):
<<<<<<< HEAD
    print(f"  {l:2d} {s:.4f}")
=======
    print(f"  {l:2d} {s:.4f}")
>>>>>>> d160e37 (Add toolkit files)
