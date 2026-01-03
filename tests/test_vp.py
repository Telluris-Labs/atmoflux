# Import from atmoflux package
from atmoflux.humidity import saturation_vp, actual_vp
from atmoflux.temperature import convert_to_celsius

# Example usage
T = 300.0    # Kelvin
Td = 292.5  # Kelvin

ex_svp = saturation_vp(T, unit="K")
ex_avp = actual_vp(Td, unit="K")

print("Saturation vapor pressure:", ex_svp)
print("Actual vapor pressure:", ex_avp)