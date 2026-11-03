# outstation.py - minimal DNP3 outstation: link layer, class-0 poll, cold restart.
import socket, threading
import dnp3

STATE = {"points": 0b00000101, "restarts": 0}


def read_exact(conn, n):
    buf = b""
    while len(buf) < n:
        chunk = conn.recv(n - len(buf))
        if not chunk:
            return None
        buf += chunk
    return buf


def read_frame(conn):
    head = read_exact(conn, 10)
    if head is None:
        return None
    length = head[2]
    user = length - 5
    blocks = (user + 15) // 16
    tail = read_exact(conn, user + 2 * blocks)
    if tail is None:
        return None
    return head + tail


def handle(conn, peer):
    with conn:
        while True:
            frame = read_frame(conn)
            if frame is None:
                return
            info = dnp3.parse_link(frame)
            app = info["user_data"][1:]          # skip the transport header
            fc = app[1] if len(app) > 1 else None
            print(f"{peer} fc=0x{fc:02x} bad_blocks={info['bad_blocks']}", flush=True)
            if fc == 0x01:                        # class-0 read
                payload = bytes([0xC0, 0xC0, 0x81, 0x00, 0x00,
                                 0x3C, 0x01, 0x01, 0x00, 0x00, 0x07,
                                 STATE["points"]])
            elif fc == 0x0D:                      # cold restart: no auth, no confirm
                STATE["restarts"] += 1
                print(f"COLD RESTART #{STATE['restarts']} accepted from {peer}", flush=True)
                payload = bytes([0xC0, 0xC0, 0x81, 0x00, 0x01])
            else:
                payload = bytes([0xC0, 0xC0, 0x81, 0x00, 0x04])   # IIN FUNC_NOT_SUPPORTED
            conn.sendall(dnp3.link_frame(0x44, info["src"], 10, payload))


def main():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 20000))
    s.listen(5)
    print("DNP3 outstation on 127.0.0.1:20000", flush=True)
    while True:
        conn, peer = s.accept()
        threading.Thread(target=handle, args=(conn, peer), daemon=True).start()


if __name__ == "__main__":
    main()

