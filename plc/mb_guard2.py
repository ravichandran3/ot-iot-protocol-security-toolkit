# mb_guard.py - protocol-aware proxy: allow reads, drop writes outside the engineering unit.
import socket, struct, threading

LISTEN, UPSTREAM = ("127.0.0.1", 15021), ("127.0.0.1", 15020)
ALLOWED_WRITE_UNIT = 1
WRITE_FCS = {5, 6, 15, 16}


def pump(src, dst):
    try:
        while True:
            data = src.recv(4096)
            if not data:
                break
            dst.sendall(data)
    except OSError:
        pass
    finally:
        for s in (src, dst):
            try:
                s.close()
            except OSError:
                pass


def handle(client):
    up = socket.create_connection(UPSTREAM, timeout=3)
    head = client.recv(7)
    tid, proto, length, unit = struct.unpack(">HHHB", head)
    body = b""
    while len(body) < length - 1:
        body += client.recv(length - 1 - len(body))

<<<<<<< HEAD
    print("GOT", unit, body[0], flush=True)
=======
    print("GOT", unit, body[0], flush=True)
>>>>>>> d160e37 (Add toolkit files)
    if body[0] in WRITE_FCS and unit != ALLOWED_WRITE_UNIT:
        print(f"DROP write fc={body[0]} unit={unit}", flush=True)
        client.sendall(struct.pack(">HHHB", tid, 0, 3, unit) + bytes([body[0] | 0x80, 0x01]))
        client.close()
        up.close()
        return

    up.sendall(head + body)
    threading.Thread(target=pump, args=(up, client), daemon=True).start()
    pump(client, up)


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
