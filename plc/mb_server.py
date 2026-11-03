# mb_server.py - minimal Modbus/TCP device with no authentication.
import socket, struct, threading

COILS = [False] * 16
REGISTERS = [0] * 16
UNIT = 1


def response(tid, unit, pdu):
    return struct.pack(">HHHB", tid, 0, len(pdu) + 1, unit) + pdu


def handle(conn):
    with conn:
        while True:
            head = conn.recv(7)
            if len(head) < 7:
                return
            tid, proto, length, unit = struct.unpack(">HHHB", head)
            body = b""
            while len(body) < length - 1:
                chunk = conn.recv(length - 1 - len(body))
                if not chunk:
                    return
                body += chunk
            fc = body[0]
            if fc == 1:                                   # read coils
                addr, count = struct.unpack(">HH", body[1:5])
                bits = 0
                for i in range(count):
                    if COILS[addr + i]:
                        bits |= 1 << i
                pdu = bytes([1, count // 8 + 1, bits & 0xFF])
            elif fc == 5:                                 # write single coil
                addr, value = struct.unpack(">HH", body[1:5])
                COILS[addr] = value == 0xFF00
                pdu = body[:5]
            elif fc == 6:                                 # write single register
                addr, value = struct.unpack(">HH", body[1:5])
                REGISTERS[addr] = value
                pdu = body[:5]
            elif fc == 0x2B and body[1] == 0x0E:          # device identification
                ids = [b"LabControls", b"MB-SIM-01", b"1.0.3"]
                pdu = bytes([0x2B, 0x0E, 0x01, 0x01, 0x00, 0x00, len(ids)])
                pdu += b"".join(bytes([i, len(x)]) + x for i, x in enumerate(ids))
            else:
                pdu = bytes([fc | 0x80, 0x01])            # illegal function
            conn.sendall(response(tid, unit, pdu))


def main():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 15020))
    s.listen(5)
    print("modbus device on 127.0.0.1:15020", flush=True)
    while True:
        conn, _ = s.accept()
        threading.Thread(target=handle, args=(conn,), daemon=True).start()


if __name__ == "__main__":
    main()

