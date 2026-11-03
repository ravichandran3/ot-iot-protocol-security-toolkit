# master.py - raw DNP3 master: class-0 poll, then repeated cold restarts.
import socket
import dnp3

READ_CLASS0 = bytes([0xC0, 0xC0, 0x01, 0x3C, 0x01, 0x00, 0x00, 0x07])
COLD_RESTART = bytes([0xC0, 0xC0, 0x0D])


def exchange(sock, user_data, label):
    sock.sendall(dnp3.link_frame(0xC4, 10, 3, user_data))
    head = sock.recv(10)
    length = head[2]
    user = length - 5
    blocks = (user + 15) // 16
    rest = b""
    while len(rest) < user + 2 * blocks:
        rest += sock.recv(user + 2 * blocks - len(rest))
    info = dnp3.parse_link(head + rest)
    app = info["user_data"][1:]
    iin = int.from_bytes(app[2:4], "big")
    extra = app[4:]
    print(f"{label}: iin=0x{iin:04x} data={extra.hex() or '-'}")
    return iin


def main():
    s = socket.create_connection(("127.0.0.1", 20000), timeout=3)
    exchange(s, READ_CLASS0, "class-0")
    for n in range(1, 4):
        exchange(s, COLD_RESTART, f"cold restart {n}")
    s.close()


if __name__ == "__main__":
    main()

