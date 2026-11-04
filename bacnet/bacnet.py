# bacnet.py - BACnet/IP frame construction, no library.
import struct

ANALOG_INPUT, ANALOG_VALUE, DEVICE = 0, 2, 8
PROP_PRESENT_VALUE = 77


def obj_id(obj_type: int, instance: int) -> bytes:
    return struct.pack(">I", (obj_type << 22) | instance)


def read_obj_id(raw: bytes):
    value = struct.unpack(">I", raw)[0]
    return value >> 22, value & 0x3FFFFF


def bvlc(npdu: bytes) -> bytes:
    return struct.pack(">BBH", 0x81, 0x0A, len(npdu) + 4) + npdu


def npdu(apdu: bytes) -> bytes:
    return b"\x01\x00" + apdu


def apdu_who_is() -> bytes:
    return bytes([0x10, 0x08])


def apdu_read_property(obj_type, instance, prop=PROP_PRESENT_VALUE) -> bytes:
    return (bytes([0x00, 0x05, 0x00, 0x0C])
            + b"\x0c" + obj_id(obj_type, instance)
            + bytes([0x19, prop]))


def apdu_write_real(obj_type, instance, value, prop=PROP_PRESENT_VALUE) -> bytes:
    return (bytes([0x00, 0x05, 0x01, 0x0F])
            + b"\x0c" + obj_id(obj_type, instance)
            + bytes([0x19, prop])
            + b"\x3e\x44" + struct.pack(">f", value) + b"\x3f")


def parse_complex_ack(data: bytes) -> float:
    idx = data.index(b"\x44")
<<<<<<< HEAD
    return struct.unpack(">f", data[idx + 1:idx + 5])[0]
=======
    return struct.unpack(">f", data[idx + 1:idx + 5])[0]
>>>>>>> d160e37 (Add toolkit files)
