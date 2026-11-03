# ais.py - AIS type-1 position report: 6-bit armouring, checksum, decode and forgery.
import math

FIELDS = [("type", 6), ("repeat", 2), ("mmsi", 30), ("status", 4), ("rot", 8),
          ("sog", 10), ("accuracy", 1), ("lon", 28), ("lat", 27), ("cog", 12),
          ("heading", 9), ("ts", 6), ("maneuver", 2), ("spare", 3),
          ("raim", 1), ("radio", 19)]


def pack(bits: str) -> str:
    out = ""
    for i in range(0, len(bits), 6):
        v = int(bits[i:i + 6].ljust(6, "0"), 2)
        out += chr(v + 48) if v < 40 else chr(v + 56)
    return out


def unpack(payload: str) -> str:
    bits = ""
    for ch in payload:
        v = ord(ch) - 48
        if v > 40:
            v -= 8
        bits += format(v, "06b")
    return bits


def checksum(body: str) -> str:
    x = 0
    for ch in body:
        x ^= ord(ch)
    return f"{x:02X}"


def encode(sentence_type: str, payload: str, channel: str = "A") -> str:
    body = f"AIVDM,1,1,,{channel},{payload},0"
    return f"!{body}*{checksum(body)}"


def type1(mmsi: int, lat: float, lon: float, sog: float, cog: float, ts: int = 0) -> str:
    values = {"type": 1, "repeat": 0, "mmsi": mmsi, "status": 0, "rot": 0,
              "sog": int(round(sog * 10)), "accuracy": 1,
              "lon": int(round(lon * 600000)), "lat": int(round(lat * 600000)),
              "cog": int(round(cog * 10)), "heading": 511, "ts": ts,
              "maneuver": 0, "spare": 0, "raim": 0, "radio": 0}
    bits = "".join(format(values[name] & ((1 << w) - 1), f"0{w}b") for name, w in FIELDS)
    return encode("1", pack(bits))


def decode(line: str):
    body, cs = line[1:].split("*")
    if checksum(body) != cs:
        raise ValueError("checksum mismatch")
    payload = body.split(",")[5]
    bits = unpack(payload)
    values, pos = {}, 0
    for name, width in FIELDS:
        raw = int(bits[pos:pos + width], 2)
        values[name] = raw - (1 << width) if raw & (1 << (width - 1)) else raw
        pos += width
    values["lat"] /= 600000
    values["lon"] /= 600000
    values["sog"] /= 10
    values["cog"] /= 10
    return values


def haversine(a, b) -> float:
    lat1, lon1, lat2, lon2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = (math.sin((lat2 - lat1) / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2)
    return 2 * 6371000 * math.asin(math.sqrt(h))


if __name__ == "__main__":
    honest = type1(232001234, 51.5000, -0.1000, 12.3, 90.0)
    print("nmea", honest)
    d = decode(honest)
    print("decoded mmsi=%d lat=%.4f lon=%.4f sog=%.1f cog=%.1f" %
          (d["mmsi"], d["lat"], d["lon"], d["sog"], d["cog"]))
    print("encoded length", len(honest.split(",")[5]), "chars =", len(honest.split(",")[5]) * 6, "bits")

    forged = type1(232001234, 51.7000, -0.5000, 12.3, 90.0)
    print("forged nmea", forged)
    f = decode(forged)
    print("forged  mmsi=%d lat=%.4f lon=%.4f" % (f["mmsi"], f["lat"], f["lon"]))
    jump = haversine((d["lat"], d["lon"]), (f["lat"], f["lon"]))
    print("distance %.0f m over 60 s = %.0f knots" % (jump, jump / 60 / 0.514444))

    broken = honest[:-2] + "00"
    try:
        decode(broken)
    except ValueError as exc:
        print("tampered ->", exc)

