import math
from adsb import build, fields, encode_position, decode_position, cpr_nl
lat, lon = 51.47, -0.4543
e = fields(build(0x4CA1FA, encode_position(lat,lon,38000,0)))["me"]
o = fields(build(0x4CA1FA, encode_position(lat,lon,38000,1)))["me"]
lat_e, lon_e = (e>>17)&0x1FFFF, e&0x1FFFF
lat_o, lon_o = (o>>17)&0x1FFFF, o&0x1FFFF
j = math.floor(59*lat_e/2**17 - 60*lat_o/2**17 + 0.5)
rl = 6.0*((j%60)+lat_e/2**17)
nl = cpr_nl(rl)
m = math.floor(lon_e*(nl-1)/2**17 - lon_o*nl/2**17 + 0.5)
print("j",j,"rl",rl,"nl",nl,"m",m,"lon_o frac",lon_o/2**17)
print("cand", 360/max(nl,1)*((m%max(nl,1))+lon_o/2**17))
<<<<<<< HEAD
print("decode_position", decode_position(e,o))
=======
print("decode_position", decode_position(e,o))
>>>>>>> d160e37 (Add toolkit files)
