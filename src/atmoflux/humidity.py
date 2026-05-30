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
    svp = SVP_A * np.exp((SVP_B * temp_C) / (temp_C + SVP_C))
    return svp


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
    avp = SVP_A * np.exp((SVP_B * Td_C) / (Td_C + SVP_C))
    return avp


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
    return 4098.0 * es / (temp_C + SVP_C) ** 2


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
    return 100.0 * ea / es


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
    return RMW * vapor_pressure / (pressure - (1 - RMW) * vapor_pressure)


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
    return RMW * vapor_pressure / (pressure - vapor_pressure)


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
    return es * (1 - rh / 100.0)


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
    e_pa = vapor_pressure * 1000.0
    return e_pa / (R_VAPOR * temp_K)