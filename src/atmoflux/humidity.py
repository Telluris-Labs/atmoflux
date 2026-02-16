"""
atmoflux.humidity
=================
Contains functions and derived variables related to atmospheric moisture. 
Includes relative humidity, specific humidity, mixing ratio, vapor pressure, and saturation calculations.

"""
# Standard imports

# Outside imports
import numpy as np

# imports from within atmoflux
from .constants import *
from .temperature import convert_temperature

def saturation_vp(temp: float, unit: str = "C") -> float:
    """
    Saturation vapor pressure of water (kPa) using Tetens formula.
   
    Parameters
    -----
    temp: Air temperature.
    unit: Unit of temperature. "C", "F", or "K" (default is "C").
        - "K" for Kelvin
        - "F" for Fahrenheit
    
    Returns
    -----
    Saturation vapor pressure of water in kilopascals (kPa).

    Raises
    -----
    ValueError
        If temp is not numeric or unit is invalid.
    """
    unit = unit.upper()
    if unit != "C":
        temp_C = convert_temperature(temp, unit, "C")
    else:
        temp_C = temp
    svp = SVP_A * np.exp((SVP_B * temp_C) / (temp_C + SVP_C))
    return svp

def actual_vp(dewpoint: float, unit: str = "C") -> float:
    """
    Actual vapor pressure of water (kPa) from dew point using Tetens formula.

    Parameters
    -----
    dewpoint: Dew point temperature.
    unit: Unit of temperature. Options: "C', "F", or "K" (default is "C").

    
    Returns
    -----
    Actual vapor pressure of water in kilopascals (kPa).

    Raises
    -----
    ValueError
        If dewpoint is not numeric or unit is invalid.
    """
    unit = unit.upper()
    if unit != "C":
        Td_C = convert_temperature(dewpoint, unit, "C")
    else:
        Td_C = dewpoint
    avp = SVP_A * np.exp((SVP_B * Td_C) / (Td_C + SVP_C))
    return avp