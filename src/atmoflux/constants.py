"""
atmoflux.constants
=================
Provides physical and derived constants used across the package. 
Includes psychrometric constants, molecular ratios, latent heats, and other shared parameters.

"""

'''
Psychometric Constants
Thermodynamic properties defining the relationship between moisture and air temperature.
'''
# Specific heat of dry air at constant pressure
# Measures the thermal energy needed to raise the temperature of 1 kg of dry air by 1 K
# Units: J/(kg·K)
CP_AIR = 1005.0  

# Lv: Latent heat of vaporization of water
# Measures the thermal energy required to convert 1 kg of water from liquid to vapor
# Units: J/kg
LV = 2.45e6  

# Psychometric Constant
# Relates the change in air temperature to the change in vapor pressure during evaporation
# Units: hPa/K
PC = 0.66

# Specific gas constant for dry air
# Relates pressure, density, and temperature for dry air
# Units: J/(kg·K)
R_AIR = 287.058  

# Ratio of the molecular weight of water vapor to dry air
# Units: Dimensionless factor used in humidity calculations
RMW = 0.622  

# Saturation Vapor Pressure constants (Tetens formula)
# Units: A = kPa, B= dimensionless, C = degrees Celsius
SVP_A = 0.61078
SVP_B = 17.27
SVP_C = 237.3