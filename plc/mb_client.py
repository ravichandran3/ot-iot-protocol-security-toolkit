# mb_client.py - raw Modbus/TCP client: no library, no auth, full visibility.
import argparse, socket, struct


def transact(sock, tid, unit, pdu):
    sock.sendall(struct.pack(">HHHB", tid, 0, len(pdu) + 1, unit) + pdu)
    head = sock.recv(7)
    rtid, proto, length, runit = struct.unpack(">HHHB", head)
    body = b""
    while len(body) < length - 1:
        body += sock.recv(length - 1 - len(body))
    return rtid, runit, body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
<<<<<<< HEAD
    ap.add_argument("--port", type=int, default=15020)
=======
    ap.add_argument("--port", type=int, default=15020)
>>>>>>> d160e37 (Add toolkit files)
    ap.add_argument("--unit", type=int, default=1)
    a = ap.parse_args()

    s = socket.create_connection((a.host, a.port), timeout=3)

    _, _, pdu = transact(s, 1, 1, bytes([0x2B, 0x0E, 0x01, 0x00]))
    n, pos, objects = pdu[6], 7, {}
    for _ in range(n):
        oid, olen = pdu[pos], pdu[pos + 1]
        objects[oid] = pdu[pos + 2:pos + 2 + olen].decode()
        pos += 2 + olen
    print("device", objects)

    _, _, pdu = transact(s, 2, 1, struct.pack(">BHH", 1, 0, 8))
    print("coils before", format(pdu[2], "08b"))

    _, _, pdu = transact(s, 3, a.unit, struct.pack(">BHH", 5, 3, 0xFF00))
    print("write coil 3 ->", "accepted" if pdu[0] == 5 else f"rejected fc=0x{pdu[0]:02x}")

    _, _, pdu = transact(s, 4, 1, struct.pack(">BHH", 1, 0, 8))
    print("coils after ", format(pdu[2], "08b"))

    for unit in (1, 17, 255):
        _, u, pdu = transact(s, 10 + unit, unit, struct.pack(">BHH", 3, 0, 1))
        print(f"unit {unit:3d} -> answered unit {u} register0={int.from_bytes(pdu[2:4], 'big')}")

    s.close()


if __name__ == "__main__":
<<<<<<< HEAD
    main()

=======
    main()

>>>>>>> d160e37 (Add toolkit files)
