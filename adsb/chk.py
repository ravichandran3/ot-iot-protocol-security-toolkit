import math
from adsb import cpr_nl, cpr_encode
lat, lon = 51.47, -0.4543
print("NL", cpr_nl(lat))
for odd in (0,1):
    dlat = 360/(60-odd)
    yz = int(math.floor(2**17*((lat % dlat)/dlat)+0.5))
    rlat = dlat*(yz/2**17 + math.floor(lat/dlat))
    print("odd",odd,"yz",yz,"rlat",rlat,"NL(rlat)",cpr_nl(rlat))
    dlon = 360/max(cpr_nl(rlat)-odd,1)
    xz = int(math.floor(2**17*((lon % dlon)/dlon)+0.5))
    print("   dlon",dlon,"xz",xz,"lon%dlon",lon%dlon)
