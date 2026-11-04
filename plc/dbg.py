import socket, struct
s = socket.create_connection(("127.0.0.1", 15020), timeout=3)
pdu = bytes([0x2B, 0x0E, 0x01, 0x00])
s.sendall(struct.pack(">HHHB", 1, 0, len(pdu)+1, 1) + pdu)
head = s.recv(7)
print("head", head.hex(), len(head))
if len(head) >= 7:
    tid, proto, length, unit = struct.unpack(">HHHB", head)
    print("len", length)
    body = b""
    while len(body) < length-1:
        c = s.recv(length-1-len(body)); print("got", len(c)); 
        if not c: break
        body += c
<<<<<<< HEAD
    print(len(body), body.hex())
=======
    print(len(body), body.hex())
>>>>>>> d160e37 (Add toolkit files)
