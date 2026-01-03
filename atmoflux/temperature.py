"""
atmoflux.temperature
=================


"""
# Standard imports

# Outside imports
import numpy as np

def convert_to_celsius(temp,unit):
    """
    Convert temperature to Celsius.
    
    Parameters
    -----
    temp: float
        Temperature value
    unit: str
        Unit of temperature: "K" or "F"

    Returns
    -----
    float
        Temperature in Celsius

    Raises
    -----
    ValueError
        If temp is not numeric or unit is invalid.
    """
    # Check temp is numeric
    if not isinstance(temp,(int, float, np.number)):
        raise ValueError("Temperature must be numeric.")
    
    unit = unit.upper()
    if unit == "K":
        return temp - 273.15
    elif unit == "F":
        return (temp - 32) * 5/9
    else:
        raise ValueError("Unit must be 'K' or 'F' when using convert_to_celsius")