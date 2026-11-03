# adsb.py - Mode S / ADS-B extended squitter: CRC-24, identification, CPR position.
import math

GENERATOR = 0xFFF409
CHARSET = "#ABCDEFGHIJKLMNOPQRSTUVWXYZ#####_###############0123456789######"


def _remainder(data: int, nbits: int) -> int:
    reg = 0
    for i in range(nbits - 1, -1, -1):
        msb = (reg >> 23) & 1
        reg = ((reg << 1) & 0xFFFFFF) | ((data >> i) & 1)
        if msb:
            reg ^= GENERATOR
    return reg


def crc24(data: int, nbits: int) -> int:
    """Remainder of data * x^24 divided by the Mode S generator."""
    return _remainder(data << 24, nbits + 24)


def syndrome(frame: int) -> int:
    """Zero for an intact 112-bit frame; the ICAO overlay otherwise."""
    return _remainder(frame, 112)


def build(icao: int, me: int, df: int = 17, ca: int = 5) -> int:
    payload = (df << 83) | (ca << 80) | (icao << 56) | me
    return (payload << 24) | crc24(payload, 88)


def fields(frame: int):
    return {"df": frame >> 107, "ca": (frame >> 104) & 0x7,
            "icao": (frame >> 80) & 0xFFFFFF,
            "me": (frame >> 24) & ((1 << 56) - 1),
            "syndrome": syndrome(frame)}


def encode_ident(callsign: str) -> int:
    me = (4 << 51) | (0 << 48)
    for i, ch in enumerate(callsign.ljust(8, "_")[:8]):
        me |= CHARSET.index(ch) << (42 - 6 * i)
    return me


def decode_ident(me: int):
    tc = me >> 51
    chars = [(me >> (42 - 6 * i)) & 0x3F for i in range(8)]
    return tc, "".join(CHARSET[c] for c in chars).strip("_")


def cpr_nl(lat: float) -> int:
    if abs(lat) >= 87:
        return 1
    a = 1 - math.cos(math.pi / 30)
    b = math.cos(math.radians(abs(lat))) ** 2
    return int(math.floor(2 * math.pi / math.acos(1 - a / b)))


def cpr_encode(lat: float, lon: float, odd: int):
    dlat = 360 / (60 - odd)
    yz = int(math.floor(2 ** 17 * ((lat % dlat) / dlat) + 0.5))
    rlat = dlat * (yz / 2 ** 17 + math.floor(lat / dlat))
    dlon = 360 / max(cpr_nl(rlat) - odd, 1)
    xz = int(math.floor(2 ** 17 * ((lon % dlon) / dlon) + 0.5))
    return yz & 0x1FFFF, xz & 0x1FFFF


def encode_position(lat: float, lon: float, alt_ft: int, odd: int) -> int:
    n = (alt_ft + 1000) // 25
    alt12 = ((n & 0xFF0) << 1) | 0x10 | (n & 0x0F)
    yz, xz = cpr_encode(lat, lon, odd)
    me = (11 << 51) | (alt12 << 36) | (odd << 34) | (yz << 17) | xz
    return me


def decode_position(me_even: int, me_odd: int, most_recent: int = 0):
    lat_e, lon_e = (me_even >> 17) & 0x1FFFF, me_even & 0x1FFFF
    lat_o, lon_o = (me_odd >> 17) & 0x1FFFF, me_odd & 0x1FFFF
    j = math.floor(59 * lat_e / 2 ** 17 - 60 * lat_o / 2 ** 17 + 0.5)
    rlat_e = 6.0 * ((j % 60) + lat_e / 2 ** 17)
    rlat_o = 360 / 59 * ((j % 59) + lat_o / 2 ** 17)
    if rlat_e >= 270:
        rlat_e -= 360
    if rlat_o >= 270:
        rlat_o -= 360
    nl = cpr_nl(rlat_e)
    m = math.floor(lon_e * (nl - 1) / 2 ** 17 - lon_o * nl / 2 ** 17 + 0.5)
    if most_recent == 0:
        ni = max(nl, 1)
        lon = (360 / ni) * ((m % ni) + lon_e / 2 ** 17)
    else:
        ni = max(nl - 1, 1)
        lon = (360 / ni) * ((m % ni) + lon_o / 2 ** 17)
    if lon >= 180:
        lon -= 360
    return rlat_e, rlat_o, lon


def decode_altitude(me: int) -> int:
    alt12 = (me >> 36) & 0xFFF
    n = ((alt12 >> 1) & 0x7F0) | (alt12 & 0xF)
    return n * 25 - 1000


if __name__ == "__main__":
    icao = 0x4CA1FA
    f = build(icao, encode_ident("TEST1234"))
    d = fields(f)
    print("ident syndrome", d["syndrome"], "icao %06x" % d["icao"],
          "callsign", decode_ident(d["me"])[1])

    for lat, lon in ((51.47, -0.4543), (-33.94, 151.18), (40.64, -73.78)):
        even = build(icao, encode_position(lat, lon, 38000, 0))
        odd = build(icao, encode_position(lat, lon, 38000, 1))
        de, _, dlon = decode_position(fields(even)["me"], fields(odd)["me"], 0)
        print("sent %8.4f %9.4f -> %8.4f %9.4f alt %d" %
              (lat, lon, de, dlon, decode_altitude(fields(even)["me"])))

    ghost_e = build(icao, encode_position(51.90, 0.20, 38000, 0))
    ghost_o = build(icao, encode_position(51.90, 0.20, 38000, 1))
    glat, _, glon = decode_position(fields(ghost_e)["me"], fields(ghost_o)["me"], 0)
    print("ghost %8.4f %9.4f syndrome %d" % (glat, glon, syndrome(ghost_o)))

    tampered = ghost_o ^ (1 << 40)
    print("tampered syndrome", syndrome(tampered))



