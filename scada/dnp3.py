# dnp3.py - DNP3 link-layer framing and CRC-16/DNP, from the spec.
import struct

POLY = 0xA6BC          # reflected 0x3D65


def crc16(data: bytes) -> int:
    crc = 0
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ POLY if crc & 1 else crc >> 1
    return crc ^ 0xFFFF


def link_frame(ctrl: int, dest: int, src: int, user_data: bytes = b"") -> bytes:
    length = 5 + len(user_data)
    head = struct.pack("<HBBHH", 0x0564, length, ctrl, dest, src)
    out = head + struct.pack("<H", crc16(head))
    for i in range(0, len(user_data), 16):
        block = user_data[i:i + 16]
        out += block + struct.pack("<H", crc16(block))
    return out


def parse_link(frame: bytes):
    if len(frame) < 10 or frame[:2] != b"\x64\x05":
        raise ValueError("not a DNP3 frame")
    head, head_crc = frame[:8], struct.unpack("<H", frame[8:10])[0]
    if crc16(head) != head_crc:
        raise ValueError("header CRC mismatch")
    start = struct.unpack("<H", frame[:2])[0]
    length = frame[2]
    ctrl, dest, src = head[2], struct.unpack("<H", head[4:6])[0], struct.unpack("<H", head[6:8])[0]
    body, pos, bad = b"", 10, 0
    while len(body) < length - 5:
        size = min(16, length - 5 - len(body))
        block = frame[pos:pos + size]
        crc = struct.unpack("<H", frame[pos + size:pos + size + 2])[0]
        if crc16(block) != crc:
            bad += 1
        body += block
        pos += size + 2
    return {"start": start, "length": length, "ctrl": ctrl, "dest": dest,
            "src": src, "user_data": body, "bad_blocks": bad}


if __name__ == "__main__":
    print("check", hex(crc16(b"123456789")))
    f = link_frame(0xC4, 10, 3, bytes.fromhex("c0c0013c01000007"))
    print("frame", f.hex())
    print(parse_link(f))

    bad_head = bytearray(f)
    bad_head[4] ^= 0x01
    try:
        parse_link(bytes(bad_head))
    except ValueError as exc:
        print("header tamper ->", exc)

    bad_data = bytearray(f)
    bad_data[12] ^= 0x01
    print("data tamper ->", parse_link(bytes(bad_data))["bad_blocks"], "bad block")



