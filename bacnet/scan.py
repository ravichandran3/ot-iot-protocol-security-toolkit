# scan.py - BACnet/IP client: discover, read, then write present-value.
import socket, sys
import bacnet

TARGET = ("127.0.0.1", 47808)


def transact(sock, apdu, expect_ack=False):
    sock.sendto(bacnet.bvlc(bacnet.npdu(apdu)), TARGET)
    data, _ = sock.recvfrom(4096)
    return data[6:]


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(2)

    reply = transact(s, bacnet.apdu_who_is())
    obj_type, instance = bacnet.read_obj_id(reply[2:6])
    vendor = int.from_bytes(reply[10:12], "big")
    print(f"i-am device {instance} vendor {vendor}")

    reply = transact(s, bacnet.apdu_read_property(bacnet.ANALOG_INPUT, 1))
    print("present-value", bacnet.parse_complex_ack(reply))

    reply = transact(s, bacnet.apdu_write_real(bacnet.ANALOG_INPUT, 1, 99.0))
    print("write 99.0 ->", "ack" if reply[0] == 0x20 else f"nack 0x{reply[0]:02x}")

    reply = transact(s, bacnet.apdu_read_property(bacnet.ANALOG_INPUT, 1))
    print("present-value", bacnet.parse_complex_ack(reply))


if __name__ == "__main__":
<<<<<<< HEAD
    main()

=======
    main()

>>>>>>> d160e37 (Add toolkit files)
