"""
atmoflux.temperature
=================


"""
# Standard imports

# Outside imports
import numpy as np

def convert_temperature(temp, input_unit, output_unit):
    """
    Convert temperature between Celsius, Fahrenheit, and Kelvin.
    
    Parameters
    ----------
    temp: float
        Temperature value
    input_unit: str
        Unit of input temperature: "C", "F", or "K"
    output_unit: str
        Unit of output temperature: "C", "F", or "K"
    
    Returns
    -------
    float
        Temperature in the specified output unit
    
    Raises
    ------
    ValueError
        If temp is not numeric or units are invalid.
    
    Examples
    --------
    >>> convert_temperature(100, "C", "F")
    212.0
    >>> convert_temperature(273.15, "K", "C")
    0.0
    """
    # Check temp is numeric
    if not isinstance(temp, (int, float, np.number)):
        raise ValueError("Temperature must be numeric.")
    
    # Normalize units to uppercase
    input_unit = input_unit.upper()
    output_unit = output_unit.upper()
    
    # Validate units
    valid_units = {"C", "F", "K"}
    if input_unit not in valid_units:
        raise ValueError(f"Input unit must be one of {valid_units}")
    if output_unit not in valid_units:
        raise ValueError(f"Output unit must be one of {valid_units}")
    
    # If units are the same, return the temperature as-is
    if input_unit == output_unit:
        return temp
    
    if input_unit == "C":
        if output_unit == "F":
            return temp * 9/5 + 32
        else:  # output_unit == "K"
            return temp + 273.15
    
    elif input_unit == "F":
        if output_unit == "C":
            return (temp - 32) * 5/9
        else:  # output_unit == "K"
            return (temp - 32) * 5/9 + 273.15
    
    else:  # input_unit == "K"
        if output_unit == "C":
            return temp - 273.15
        else:  # output_unit == "F"
            return (temp - 273.15) * 9/5 + 32