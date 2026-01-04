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
        t_c = temp - 273.15
    elif unit == "F":
        t_c = (temp - 32) * 5/9
    else:
        raise ValueError("Unit must be 'K' or 'F' when using convert_to_celsius")
    return t_c
    
def convert_to_fahrenheit(temp,unit):
    """
    Convert temperature to Fahrenheit.
    
    Parameters
    -----
    temp: float
        Temperature value
    unit: str
        Unit of temperature: "K" or "C"

    Returns
    -----
    float
        Temperature in Fahrenheit

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
        t_f = (temp - 273.15) * 9/5 + 32
    elif unit == "C":
        t_f = (temp * 9/5) + 32
    else:
        raise ValueError("Unit must be 'K' or 'C' when using convert_to_fahrenheit") 
    return t_f

def convert_to_kelvin(temp,unit):
    """
    Convert temperature to Kelvin.
    
    Parameters
    -----
    temp: float
        Temperature value
    unit: str
        Unit of temperature: "C" or "F"

    Returns
    -----
    float
        Temperature in Kelvin

    Raises
    -----
    ValueError
        If temp is not numeric or unit is invalid.
    """
    # Check temp is numeric
    if not isinstance(temp,(int, float, np.number)):
        raise ValueError("Temperature must be numeric.")
    
    unit = unit.upper()
    if unit == "C":
        t_k = temp + 273.15
    elif unit == "F":
        t_k = (temp - 32) * 5/9 + 273.15
    else:
        raise ValueError("Unit must be 'C' or 'F' when using convert_to_kelvin") 
    return t_k