# bms.py - BACnet/IP device with no authentication.
import socket
import bacnet

DEVICE = (bacnet.DEVICE, 1234)
VENDOR = 665
VALUES = {(bacnet.ANALOG_INPUT, 1): 21.5, (bacnet.ANALOG_INPUT, 2): 18.0}


def handle(apdu, addr, sock):
    kind, service = apdu[0] >> 4, apdu[1] if len(apdu) > 1 else None
    if kind == 1 and service == 0x08:                       # Who-Is
        i_am = (bytes([0x10, 0x00]) + bacnet.obj_id(*DEVICE)
                + (480).to_bytes(3, "big") + b"\x00" + VENDOR.to_bytes(2, "big"))
        sock.sendto(bacnet.bvlc(bacnet.npdu(i_am)), addr)
        print("who-is -> i-am", flush=True)
        return
    if kind == 0 and len(apdu) >= 8:                        # Confirmed-Request
        invoke, svc = apdu[2], apdu[3]
        _, inst = bacnet.read_obj_id(apdu[5:9])
        prop = apdu[10]
        if svc == 0x0C:                                     # ReadProperty
            value = VALUES.get((bacnet.ANALOG_INPUT, inst), 0.0)
            body = (bytes([0x20, invoke, 0x0C]) + b"\x3e\x44"
                    + __import__("struct").pack(">f", value) + b"\x3f")
            sock.sendto(bacnet.bvlc(bacnet.npdu(body)), addr)
            print(f"read ai{inst} p{prop} -> {value}", flush=True)
        elif svc == 0x0F:                                   # WriteProperty
            value = bacnet.parse_complex_ack(apdu)
            VALUES[(bacnet.ANALOG_INPUT, inst)] = value
            sock.sendto(bacnet.bvlc(bacnet.npdu(bytes([0x20, invoke, 0x0F]))), addr)
            print(f"WRITE ai{inst} p{prop} = {value}", flush=True)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 47808))
    print("BACnet/IP device on 127.0.0.1:47808", flush=True)
    while True:
        data, addr = s.recvfrom(4096)
        if data[:2] != b"\x81\x0a":
            continue
        handle(data[6:], addr, s)


if __name__ == "__main__":
    main()

