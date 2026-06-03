"""
atmoflux.humidity
=================
Contains functions and derived variables related to atmospheric moisture. 
Includes saturation and actual vapor pressure, the slope of the saturation
curve, relative and specific humidity, mixing ratio, vapor pressure deficit, and
absolute humidity.

"""

from __future__ import annotations

# Outside imports
import numpy as np

# imports from within atmoflux
from .constants import SVP_A, SVP_B, SVP_C, RMW, R_VAPOR
from .exceptions import OutOfRangeError
from .temperature import convert_temperature


def saturation_vp(temp: float, unit: str = "C") -> float:
    """
    Saturation vapor pressure of water (kPa) using the Tetens formula.
   
    Parameters
    -----
    temp: Air temperature.
    unit: Unit of temperature. "C", "F", or "K" (default is "C").
    
    Returns
    -----
    Saturation vapor pressure of water in kilopascals (kPa).

    Raises
    ------
    ValidationError
        If temp is not numeric.
    InvalidUnitError
        If unit is invalid.

    Examples
    --------
    >>> print(round(saturation_vp(20), 4))
    2.3382
    """
    unit = unit.upper()

    if unit != "C":
        temp_C = convert_temperature(temp, unit, "C")
    else:
        temp_C = temp

    es = SVP_A * np.exp((SVP_B * temp_C) / (temp_C + SVP_C))

    return es


def actual_vp(dewpoint: float, unit: str = "C") -> float:
    """
    Actual vapor pressure of water (kPa) from dew point using the Tetens formula.

    Parameters
    -----
    dewpoint: Dew point temperature.
    unit : Unit of temperature: "C", "F", or "K" (default is "C").

    Returns
    -----
    Actual vapor pressure of water in kilopascals (kPa).

    Raises
    ------
    ValidationError
        If dewpoint is not numeric.
    InvalidUnitError
        If unit is invalid.

    Examples
    --------
    >>> print(round(actual_vp(10), 4))
    1.2279
    """
    unit = unit.upper()

    if unit != "C":
        Td_C = convert_temperature(dewpoint, unit, "C")
    else:
        Td_C = dewpoint

    e = SVP_A * np.exp((SVP_B * Td_C) / (Td_C + SVP_C))

    return e


def saturation_vp_slope(temp: float, unit: str = "C") -> float:
    """
    Slope of the saturation vapor pressure curve (kPa/°C).

    The slope (commonly denoted delta) is the rate of change of saturation vapor
    pressure with temperature and is a key term in the Penman and
    Penman-Monteith evaporation equations.

    Parameters
    ----------
    temp : Air temperature.
    unit : Unit of temperature: "C", "F", or "K" (default is "C").

    Returns
    -------
    Slope of the saturation vapor pressure curve in kPa per degree Celsius.

    Raises
    ------
    ValidationError
        If temp is not numeric.
    InvalidUnitError
        If unit is invalid.

    Notes
    -----
    delta = 4098 * es(T) / (T + 237.3) ** 2
    where es(T) is the Tetens saturation vapor pressure in kPa and T is in °C.

    Examples
    --------
    >>> print(round(saturation_vp_slope(20), 4))
    0.1447
    """
    unit = unit.upper()
    if unit != "C":
        temp_C = convert_temperature(temp, unit, "C")
    else:
        temp_C = temp

    es = saturation_vp(temp_C, "C")
    delta = 4098.0 * es / (temp_C + SVP_C) ** 2

    return delta


def relative_humidity(temp: float, dewpoint: float, unit: str = "C") -> float:
    """
    Relative humidity (%) from temperature and dew point.

    Parameters
    ----------
    temp : Air temperature.
    dewpoint : Dew point temperature (same unit as temp).
    unit : Unit of the input temperatures: "C", "F", or "K" (default "C").

    Returns
    -------
    Relative humidity as a percentage.

    Raises
    ------
    InvalidUnitError
        If unit is invalid.

    Notes
    -----
    RH = 100 * e(Td) / es(T)
    the ratio of actual to saturation vapor pressure.

    Examples
    --------
    >>> print(round(relative_humidity(20, 10), 1))
    52.5
    """
    es = saturation_vp(temp, unit)
    ea = actual_vp(dewpoint, unit)
    rh = 100.0 * ea / es

    return rh


def specific_humidity(vapor_pressure: float, pressure: float) -> float:
    """
    Specific humidity (kg/kg) from vapor pressure and total pressure.

    Specific humidity is the mass of water vapor per unit mass of moist air.

    Parameters
    ----------
    vapor_pressure : Actual vapor pressure (kPa).
    pressure : Total air pressure (kPa), must exceed vapor_pressure.

    Returns
    -------
    Specific humidity in kg of water vapor per kg of moist air.

    Raises
    ------
    OutOfRangeError
        If pressure is not greater than vapor_pressure.

    Notes
    -----
    q = RMW * e / (P - (1 - RMW) * e)
    where RMW is the ratio of molecular weights of water vapor to dry air.

    Examples
    --------
    >>> print(round(specific_humidity(1.2279, 101.325), 5))
    0.00757
    """
    if np.any(pressure <= vapor_pressure):
        raise OutOfRangeError("Total pressure must exceed vapor pressure.")
    
    q = RMW * vapor_pressure / (pressure - (1 - RMW) * vapor_pressure)

    return q


def mixing_ratio(vapor_pressure: float, pressure: float) -> float:
    """
    Mixing ratio (kg/kg) from vapor pressure and total pressure.

    The mixing ratio is the mass of water vapor per unit mass of dry air.

    Parameters
    ----------
    vapor_pressure : Actual vapor pressure (kPa).
    pressure : Total air pressure (kPa), must exceed vapor_pressure.

    Returns
    -------
    Mixing ratio in kg of water vapor per kg of dry air.

    Raises
    ------
    OutOfRangeError
        If pressure is not greater than vapor_pressure.

    Notes
    -----
    w = RMW * e / (P - e)

    Examples
    --------
    >>> print(round(mixing_ratio(1.2279, 101.325), 5))
    0.00763
    """
    if np.any(pressure <= vapor_pressure):
        raise OutOfRangeError("Total pressure must exceed vapor pressure.")
    
    w = RMW * vapor_pressure / (pressure - vapor_pressure)

    return w


def vapor_pressure_deficit(temp: float, rh: float, unit: str = "C") -> float:
    """
    Vapor pressure deficit (kPa) from temperature and relative humidity.

    The vapor pressure deficit (VPD) is the difference between the saturation and
    actual vapor pressures and indicates the drying capacity of the air.

    Parameters
    ----------
    temp : Air temperature.
    rh : Relative humidity (%), in the interval (0, 100].
    unit : Unit of temperature: "C", "F", or "K" (default "C").

    Returns
    -------
    Vapor pressure deficit in kilopascals (kPa).

    Raises
    ------
    OutOfRangeError
        If rh is not in the interval (0, 100].
    InvalidUnitError
        If unit is invalid.

    Notes
    -----
    VPD = es(T) * (1 - RH / 100)

    Examples
    --------
    >>> print(round(vapor_pressure_deficit(25, 60), 4))
    1.2671
    """
    if np.any(rh <= 0) or np.any(rh > 100):
        raise OutOfRangeError("Relative humidity must be between 0 and 100%")
    
    es = saturation_vp(temp, unit)
    vpd = es * (1 - rh / 100.0)

    return vpd


def absolute_humidity(vapor_pressure: float, temp: float, unit: str = "C") -> float:
    """
    Absolute humidity (kg/m³) from vapor pressure and temperature.

    Absolute humidity is the density of water vapor in the air.

    Parameters
    ----------
    vapor_pressure : Actual vapor pressure (kPa).
    temp : Air temperature.
    unit : Unit of temperature: "C", "F", or "K" (default "C").

    Returns
    -------
    Absolute humidity in kg of water vapor per cubic meter.

    Raises
    ------
    InvalidUnitError
        If unit is invalid.

    Notes
    -----
    Ideal gas law for water vapor:
    rho_v = e / (R_vapor * T)
    with e in pascals and T in kelvin.

    Examples
    --------
    >>> print(round(absolute_humidity(1.2279, 20), 5))
    0.00908
    """
    temp_K = convert_temperature(temp, unit.upper(), "K")

    # Convert vapor pressure from kPa to Pa for SI consistency.
    e = vapor_pressure * 1000.0
    rho_v = e / (R_VAPOR * temp_K)

    return rho_v


def saturation_vp_ice(temp: float, unit: str = "C") -> float:
    """
    Saturation vapor pressure over ice (kPa) using the Tetens ice formula.

    Parameters
    ----------
    temp : Air temperature (typically <= 0 °C).
    unit : Unit of temperature: "C", "F", or "K" (default is "C").

    Returns
    -------
    Saturation vapor pressure over ice in kilopascals (kPa).

    Raises
    ------
    InvalidUnitError
        If unit is invalid.

    Notes
    -----
    Tetens formula with ice coefficients:
    es_ice = 0.61078 * exp(21.875 * T / (T + 265.5))
    with T in °C.

    Examples
    --------
    >>> print(round(saturation_vp_ice(-10), 4))
    0.2595
    """
    temp_C = convert_temperature(temp, unit.upper(), "C")
    es_ice = SVP_A * np.exp(21.875 * temp_C / (temp_C + 265.5))

    return es_ice


def specific_humidity_from_dewpoint(
    dewpoint: float, pressure: float, unit: str = "C"
) -> float:
    """
    Specific humidity (kg/kg) from dew point and total pressure.

    Parameters
    ----------
    dewpoint : Dew point temperature.
    pressure : Total air pressure (kPa), must exceed the vapor pressure.
    unit : Unit of dewpoint: "C", "F", or "K" (default "C").

    Returns
    -------
    Specific humidity in kg of water vapor per kg of moist air.

    Raises
    ------
    OutOfRangeError
        If pressure is not greater than the actual vapor pressure.
    InvalidUnitError
        If unit is invalid.

    Notes
    -----
    Computes actual vapor pressure from the dew point, then applies
    q = RMW * e / (P - (1 - RMW) * e).

    Examples
    --------
    >>> print(round(specific_humidity_from_dewpoint(10, 101.325), 5))
    0.00757
    """
    e = actual_vp(dewpoint, unit)

    if np.any(pressure <= e):
        raise OutOfRangeError("Total pressure must exceed vapor pressure.")
    
    q = RMW * e / (pressure - (1 - RMW) * e)

    return q


def relative_humidity_from_specific_humidity(
    specific_humidity: float, temp: float, pressure: float, unit: str = "C"
) -> float:
    """
    Relative humidity (%) from specific humidity, temperature, and pressure.

    Parameters
    ----------
    specific_humidity : Specific humidity (kg/kg), non-negative.
    temp : Air temperature.
    pressure : Total air pressure (kPa), must be positive.
    unit : Unit of temp: "C", "F", or "K" (default "C").

    Returns
    -------
    Relative humidity as a percentage.

    Raises
    ------
    OutOfRangeError
        If specific_humidity is negative or pressure is not positive.
    InvalidUnitError
        If unit is invalid.

    Notes
    -----
    Inverts the specific-humidity definition to recover vapor pressure,
    e = q * P / (RMW + (1 - RMW) * q), then divides by saturation vapor pressure.

    Examples
    --------
    >>> print(round(relative_humidity_from_specific_humidity(0.00757, 20, 101.325), 1))
    52.5
    """
    if np.any(specific_humidity < 0):
        raise OutOfRangeError("Specific humidity must be non-negative.")
    if np.any(pressure <= 0):
        raise OutOfRangeError("Pressure must be positive.")
    
    e = specific_humidity * pressure / (RMW + (1 - RMW) * specific_humidity)
    es = saturation_vp(temp, unit)
    rh = 100.0 * e / es

    return rh


def precipitable_water(specific_humidity: float, pressure: float) -> float:
    """
    Column precipitable water from layer-mean specific humidity.

    Estimates the depth of liquid water that would result if all the water vapor
    in an atmospheric column were condensed, using a single layer-mean specific
    humidity and the surface pressure.

    Parameters
    ----------
    specific_humidity : Layer-mean specific humidity (kg/kg), non-negative.
    pressure : Surface pressure (kPa), must be positive.

    Returns
    -------
    Precipitable water in millimeters.

    Raises
    ------
    OutOfRangeError
        If specific_humidity is negative or pressure is not positive.

    Notes
    -----
    Single-layer approximation:
    PW = q * P / (rho_water * g)
    with P converted to pascals and the result expressed in millimeters.

    Examples
    --------
    >>> print(round(precipitable_water(0.01, 101.325), 2))
    103.32
    """
    if np.any(specific_humidity < 0):
        raise OutOfRangeError("Specific humidity must be non-negative.")
    if np.any(pressure <= 0):
        raise OutOfRangeError("Pressure must be positive.")
    
    g = 9.80665
    rho_water = 1000.0
    p_pa = pressure * 1000.0

    # Depth of water in meters, converted to millimeters.
    pw = specific_humidity * p_pa / (rho_water * g) * 1000.0

    return pw