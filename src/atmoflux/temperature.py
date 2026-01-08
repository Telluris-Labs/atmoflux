"""
atmoflux.temperature
=================


"""
# Standard imports

# Outside imports
import numpy as np

def convert_temperature(temp: float, input_unit: str, output_unit: str) -> float:
    """
    Convert temperature between Celsius, Fahrenheit, and Kelvin.
    
    Parameters
    ----------
    temp : Temperature value.
    input_unit : Unit of input temperature: "C", "F", or "K".
    output_unit : Unit of output temperature: "C", "F", or "K".
    
    Returns
    -------
    Temperature in the specified output unit.
    
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
    >>> a, b, c = 80,"F","C"
    >>> temp = convert_temperature(a, b, c)
    >>> print(f"{a}°{b} is equal to {round(temp,2)}°{c}.")
    80°F is equal to 26.67°C.
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
        
def dewpoint_temperature(temp: float, rh: float, unit: str ="C") -> float:
    """
    Calculate dew point temperature from temperature and relative humidity.
    
    Uses the Magnus formula, which is accurate for normal atmospheric conditions.
    
    Parameters
    ----------
    temp : Air temperature.
    rh : Relative humidity (%).
    unit : Unit of input/output temperature: "C", "F", or "K" (default is "C").
    
    Returns
    -------
    Dew point temperature in the same unit as input.
    
    Notes
    -----
    Uses the Magnus-Tetens approximation:
    Td = (b * alpha) / (a - alpha)
    where alpha = ln(RH/100) + (a*T)/(b+T)
    Constants: a = 17.27, b = 237.3°C
    
    Valid for:
    - Temperature range: -40°C to 50°C
    - Relative humidity: 1% to 100%
    
    Examples
    --------
    >>> dewpoint_temperature(30, 50)
    18.44...
    >>> dewpoint_temperature(86, 50, unit="F")
    65.19...
    """
    # Validate relative humidity
    if not 0 < rh <= 100:
        raise ValueError("Relative humidity must be between 0 and 100%")
    
    # Convert temperature to Celsius for calculation
    unit = unit.upper()
    if unit != "C":
        temp_C = convert_temperature(temp, unit, "C")
    else:
        temp_C = temp
    
    # Magnus formula constants
    a = 17.27
    b = 237.3
    
    # Calculate alpha
    alpha = (a * temp_C) / (b + temp_C) + np.log(rh / 100.0)
    
    # Calculate dew point in Celsius
    Td_C = (b * alpha) / (a - alpha)
    
    # Convert back to original unit if necessary
    if unit != "C":
        return convert_temperature(Td_C, "C", unit)
    else:
        return Td_C

def dewpoint_from_avp(avp: float, unit: str ="C") -> float:
    """
    Calculate dew point temperature from actual vapor pressure.
    
    Parameters
    ----------
    avp : Actual vapor pressure (kPa).
    unit: Unit of output temperature: "C", "F", or "K" (default is "C").
    
    Returns
    -------
    Dew point temperature in specified unit
    """
    # Calculate dew point in Celsius using the inverse of the saturation vapor pressure formula
    Td_C = (237.3 * np.log(avp / 0.61078)) / (17.27 - np.log(avp / 0.61078))
    
    # Convert to desired unit if necessary
    unit = unit.upper()
    if unit != "C":
        return convert_temperature(Td_C, "C", unit)
    else:
        return Td_C
