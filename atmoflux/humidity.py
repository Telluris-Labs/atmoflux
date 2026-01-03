"""
atmoflux.humidity
=================


"""
# Standard imports

# Outside imports
import numpy as np

# imports from within atmoflux
from .temperature import convert_to_celsius

def saturation_vp(temp, unit="C"):
    """
    Saturation vapor pressure of water (kPa) using Tetens formula.
   
    Parameters
    -----
    temp: float
        Air temperature.
    unit: str, optional
        Unit of temperature. Options:
        - "C" for Celsius (default)
        - "K" for Kelvin
        - "F" for Fahrenheit
    
    Returns
    -----
    float
        Saturation vapor pressure of water in kilopascals (kPa).

    Raises
    -----
    ValueError
        If temp is not numeric or unit is invalid.
    """
    unit = unit.upper()
    if unit != "C":
        temp_C = convert_to_celsius(temp, unit)
    else:
        temp_C = temp
    svp = 0.61078 * np.exp((17.27 * temp_C) / (temp_C + 237.3))
    return svp

def actual_vp(dewpoint, unit="C"):
    """
    Actual vapor pressure of water (kPa) from dew point using Tetens formula.

    Parameters
    -----
    dewpoint: float
        Dew point temperature.
    unit: str, optional
        Unit of temperature. Options:
        - "C" for Celsius (default)
        - "K" for Kelvin
        - "F" for Fahrenheit
    
    Returns
    -----
    float
        Actual vapor pressure of water in kilopascals (kPa).

    Raises
    -----
    ValueError
        If dewpoint is not numeric or unit is invalid.
    """
    unit = unit.upper()
    if unit != "C":
        Td_C = convert_to_celsius(dewpoint, unit)
    else:
        Td_C = dewpoint
    avp = 0.61078 * np.exp((17.27 * Td_C) / (Td_C + 237.3))
    return avp