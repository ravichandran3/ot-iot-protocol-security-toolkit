# pqc.py - hybrid TLS 1.3 ClientHello, downgrade test, harvest-now exposure model.
import struct

X25519, X25519MLKEM768 = 0x001D, 0x11EC
AES128_GCM, AES256_GCM, CHACHA20 = 0x1301, 0x1302, 0x1303
ED25519, ECDSA_P256 = 0x0807, 0x0403


def u8(n):  return struct.pack(">B", n)
def u16(n): return struct.pack(">H", n)
def u24(n): return struct.pack(">I", n)[1:]
def vec8(b):  return u8(len(b)) + b
def vec16(b): return u16(len(b)) + b
def ext(t, body): return u16(t) + vec16(body)


def key_share(*shares):
    body = b"".join(u16(g) + vec16(k) for g, k in shares)
    return vec16(body)


def client_hello(pq: bool, seed: int = 1) -> bytes:
    import random
    rng = random.Random(seed)
    shares = [(X25519, bytes(rng.randrange(256) for _ in range(32)))]
    if pq:
        shares.insert(0, (X25519MLKEM768, bytes(rng.randrange(256) for _ in range(1216))))
    exts = b"".join([
        ext(0x0000, vec16(b"lab.example")),
        ext(0x000A, vec16(u16(X25519MLKEM768) + u16(X25519))),
        ext(0x002B, vec8(u16(0x0304))),
        ext(0x0033, key_share(*shares)),
        ext(0x000D, vec16(u16(ED25519) + u16(ECDSA_P256))),
    ])
    body = (u16(0x0303) + bytes(rng.randrange(256) for _ in range(32))
            + vec8(bytes(rng.randrange(256) for _ in range(32)))
            + vec16(u16(AES128_GCM) + u16(AES256_GCM) + u16(CHACHA20))
            + vec8(b"\x00") + vec16(exts))
    hs = b"\x01" + u24(len(body)) + body
    return b"\x16\x03\x01" + vec16(hs)


def parse(record: bytes):
    assert record[0] == 0x16
    hs_len = struct.unpack(">H", record[3:5])[0]
    hs = record[5:5 + hs_len]
    body = hs[4:]
    pos = 2 + 32
    sid_len = body[pos]; pos += 1 + sid_len
    cs_len = struct.unpack(">H", body[pos:pos + 2])[0]; pos += 2 + cs_len
    comp_len = body[pos]; pos += 1 + comp_len
    ext_len = struct.unpack(">H", body[pos:pos + 2])[0]; pos += 2
    end, found = pos + ext_len, {"key_share": [], "supported_versions": [], "groups": []}
    while pos < end:
        t, ln = struct.unpack(">HH", body[pos:pos + 4]); pos += 4
        data = body[pos:pos + ln]; pos += ln
        if t == 0x0033:
            p = 2
            while p < len(data):
                g, kl = struct.unpack(">HH", data[p:p + 4])
                found["key_share"].append((g, kl)); p += 4 + kl
        elif t == 0x002B:
            found["supported_versions"] = [struct.unpack(">H", data[i:i + 2])[0]
                                           for i in range(1, len(data), 2)]
        elif t == 0x000A:
            found["groups"] = [struct.unpack(">H", data[i:i + 2])[0]
                               for i in range(2, len(data), 2)]
    found["record_bytes"] = len(record)
    return found


DATA_CLASSES = [
    ("payment records", 7, 240),
    ("clinical records", 30, 90),
    ("subscriber metadata", 3, 1200),
    ("telemetry", 1, 800),
    ("signing keys (HSM)", 15, 1),
]

if __name__ == "__main__":
    full = client_hello(pq=True)
    classic = client_hello(pq=False)
    f, c = parse(full), parse(classic)
    print("hybrid record bytes", f["record_bytes"],
          "classical", c["record_bytes"],
          "ratio %.2f" % (f["record_bytes"] / c["record_bytes"]))
    print("hybrid key_shares", [(hex(g), n) for g, n in f["key_share"]])
    print("groups advertised", [hex(g) for g in f["groups"]])
    print("supported_versions", [hex(v) for v in f["supported_versions"]])

    stripped = client_hello(pq=False)
    s = parse(stripped)
    print("stripped record bytes", s["record_bytes"],
          "still advertises hybrid group", X25519MLKEM768 in s["groups"],
          "negotiable share", [hex(g) for g, _ in s["key_share"]])

    migration_done, crqc = 2030, 2035
    gap = crqc - migration_done
    print(f"migration complete {migration_done}, CRQC {crqc}, gap {gap} years")
    total = 0
    for name, years, tb in DATA_CLASSES:
        exposed = max(0, years - gap)
        risk = tb * exposed / years
        total += risk
        print(f"{name:<22} retention {years:2d}y bytes_TB {tb:5d} exposed_y {exposed:2d} at_risk_TB {risk:7.1f}")
    print(f"total at risk {total:.0f} TB of {sum(t for _, _, t in DATA_CLASSES)} TB")
