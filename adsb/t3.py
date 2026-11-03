from adsb import crc24, GENERATOR
p = 0x1234567890
for width in (40,):
    c = crc24(p, width)
    f = (p << 24) | c
    print(hex(c), crc24(f, width+24))
# toy 4-bit poly 0x13 style check
def crc_generic(data, nbits, poly, width):
    reg = 0
    top = 1 << (width-1)
    for i in range(nbits-1, -1, -1):
        msb = reg & top
        reg = ((reg << 1) & ((1<<width)-1)) | ((data >> i) & 1)
        if msb: reg ^= poly
    return reg
for w, poly in ((4, 0x13), (8, 0x07)):
    c = crc_generic(0b1101, 4, poly, w)
    print("toy", w, bin(c), bin(crc_generic((0b1101<<w)|c, 4+w, poly, w)))
