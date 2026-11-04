# tc.py - CCSDS telecommand frame, FECF, replay and forgery against a spacecraft model.
import struct

MODES = {0x01: "SAFE", 0x02: "MANOEUVRE", 0x03: "NOMINAL"}


def crc16(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc


def tc_frame(scid: int, vcid: int, fsn: int, data: bytes) -> bytes:
    total = 5 + len(data) + 2
    w0 = scid & 0xFF
    w1 = ((vcid & 0x3F) << 10) | ((total - 1) & 0x3FF)
    body = struct.pack(">HHB", w0, w1, fsn) + data
    return body + struct.pack(">H", crc16(body))


def parse(frame: bytes):
    w0, w1, fsn = struct.unpack(">HHB", frame[:5])
    return {"scid": w0 & 0xFF, "vcid": w1 >> 10,
            "length": (w1 & 0x3FF) + 1, "fsn": fsn, "data": frame[5:-2]}


class Spacecraft:
    def __init__(self, cop1: bool = False):
        self.cop1 = cop1
        self.last = None
        self.mode = "NOMINAL"

    def receive(self, frame: bytes) -> str:
        if crc16(frame[:-2]) != int.from_bytes(frame[-2:], "big"):
            return "REJECTED frame error control"
        f = parse(frame)
        if self.cop1 and f["fsn"] == self.last:
            return "REJECTED duplicate (COP-1)"
        self.last = f["fsn"]
        if f["data"]:
            self.mode = MODES.get(f["data"][0], "UNKNOWN")
        return f"ACCEPTED mode={self.mode}"


if __name__ == "__main__":
    print("crc check 0x%04x" % crc16(b"123456789"))
    legit = tc_frame(0x2A, 1, 10, bytes([0x01]))
    print("frame", legit.hex(), "crc_ok", crc16(legit[:-2]) == int.from_bytes(legit[-2:], "big"))

    s = Spacecraft()
    print("no COP-1, first  ->", s.receive(legit))
    print("no COP-1, replay ->", s.receive(legit))

    c = Spacecraft(cop1=True)
    print("COP-1,   first   ->", c.receive(legit))
    print("COP-1,   replay  ->", c.receive(legit))

    forged = tc_frame(0x2A, 1, 11, bytes([0x02]))
    print("forged fsn=11    ->", c.receive(forged))

    tampered = bytearray(tc_frame(0x2A, 1, 12, bytes([0x02])))
    tampered[6] ^= 0x01
<<<<<<< HEAD
    print("tampered         ->", c.receive(bytes(tampered)))

=======
    print("tampered         ->", c.receive(bytes(tampered)))

>>>>>>> d160e37 (Add toolkit files)
