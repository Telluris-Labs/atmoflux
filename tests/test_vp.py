# Import from atmoflux package
from atmoflux.humidity import saturation_vp, actual_vp
from atmoflux.temperature import convert_temperature

# Example usage with equivalen values in C, F, and K
T_c = 30.0
Td_c = 12.5
T_f = 86.0
Td_f = 54.5
T_k = 303.15   
Td_k = 285.65  

avp1 = actual_vp(T_k, "K")
avp2 = actual_vp(T_f, "F")
avp3 = actual_vp(T_c, "C")

svp1 = saturation_vp(Td_k, "K")
svp2 = saturation_vp(Td_f, "F")
svp3 = saturation_vp(Td_c, "C")

avp = [avp1, avp2, avp3]
svp = [svp1, svp2, svp3]

for a in avp:
    print(f"Actual vapor pressure: {a}")

for s in svp:
    print(f"Saturation vapor pressure: {s}")