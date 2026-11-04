# mb_guard.py - protocol-aware proxy: allow reads, drop writes outside the engineering unit.
import socket, struct, threading

LISTEN, UPSTREAM = ("127.0.0.1", 15021), ("127.0.0.1", 15020)
ALLOWED_WRITE_UNIT = 1
WRITE_FCS = {5, 6, 15, 16}


def read_frame(sock):
    head = b""
    while len(head) < 7:
        chunk = sock.recv(7 - len(head))
        if not chunk:
            return None
        head += chunk
    tid, proto, length, unit = struct.unpack(">HHHB", head)
    body = b""
    while len(body) < length - 1:
        chunk = sock.recv(length - 1 - len(body))
        if not chunk:
            return None
        body += chunk
    return tid, unit, body


def send_frame(sock, tid, unit, body):
    sock.sendall(struct.pack(">HHHB", tid, 0, len(body) + 1, unit) + body)


def handle(client):
    up = socket.create_connection(UPSTREAM, timeout=3)
    try:
        while True:
            frame = read_frame(client)
            if frame is None:
                return
            tid, unit, body = frame
            if body[0] in WRITE_FCS and unit != ALLOWED_WRITE_UNIT:
                print(f"DROP write fc={body[0]} unit={unit}", flush=True)
                send_frame(client, tid, unit, bytes([body[0] | 0x80, 0x01]))
                continue
            send_frame(up, tid, unit, body)
            reply = read_frame(up)
            if reply is None:
                return
            send_frame(client, *reply)
    except OSError:
        pass
    finally:
        client.close()
        up.close()


def main():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(LISTEN)
    s.listen(5)
    print(f"guard on {LISTEN[0]}:{LISTEN[1]} -> {UPSTREAM[0]}:{UPSTREAM[1]}", flush=True)
    while True:
        conn, _ = s.accept()
        threading.Thread(target=handle, args=(conn,), daemon=True).start()


if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> d160e37 (Add toolkit files)
