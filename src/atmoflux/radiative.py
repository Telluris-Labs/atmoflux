"""
atmoflux.radiative
=================
Computes radiative fluxes at the surface or in the atmosphere. 
Includes blackbody emission, net shortwave and longwave components, net all-wave
radiation, and clear-sky atmospheric emissivity.

"""

from __future__ import annotations

# Outside imports
import numpy as np

# imports from within atmoflux
from .constants import STEFAN_BOLTZMANN
from .exceptions import OutOfRangeError
from .temperature import convert_temperature


def blackbody_radiation(
    temp: float, emissivity: float = 1.0, unit: str = "K"
) -> float:
    """
    Radiant emittance of a surface from the Stefan-Boltzmann law.

    Parameters
    ----------
    temp : Surface temperature.
    emissivity : Surface emissivity in (0, 1] (default 1.0 for a blackbody).
    unit : Unit of input temperature: "C", "F", or "K" (default "K").

    Returns
    -------
    Emitted longwave radiative flux in W/m².

    Raises
    ------
    OutOfRangeError
        If emissivity is outside (0, 1].
    InvalidUnitError
        If unit is invalid.

    Notes
    -----
    Stefan-Boltzmann law:
    L = emissivity * sigma * T ** 4
    with T in kelvin and sigma the Stefan-Boltzmann constant.

    Examples
    --------
    >>> print(round(blackbody_radiation(288.0), 2))
    390.11
    >>> print(round(blackbody_radiation(15.0, 0.97, unit="C"), 2))
    379.19
    """
    if np.any(emissivity <= 0) or np.any(emissivity > 1):
        raise OutOfRangeError("Emissivity must be in the interval (0, 1].")
    temp_K = convert_temperature(temp, unit.upper(), "K")
    return emissivity * STEFAN_BOLTZMANN * temp_K**4


def net_shortwave(sw_down: float, albedo: float) -> float:
    """
    Net shortwave radiation absorbed at a surface.

    Parameters
    ----------
    sw_down : Incoming (downwelling) shortwave irradiance (W/m²).
    albedo : Surface shortwave albedo (reflectance) in [0, 1].

    Returns
    -------
    Net shortwave radiation absorbed by the surface (W/m²).

    Raises
    ------
    OutOfRangeError
        If albedo is outside [0, 1].

    Notes
    -----
    SW_net = sw_down * (1 - albedo)

    Examples
    --------
    >>> print(net_shortwave(800.0, 0.2))
    640.0
    """
    if np.any(albedo < 0) or np.any(albedo > 1):
        raise OutOfRangeError("Albedo must be in the interval [0, 1].")
    return sw_down * (1 - albedo)


def net_longwave(
    lw_down: float, temp_surface: float, emissivity: float = 1.0, unit: str = "K"
) -> float:
    """
    Net longwave radiation at a surface (positive into the surface).

    Parameters
    ----------
    lw_down : Incoming (downwelling) longwave irradiance (W/m²).
    temp_surface : Surface (skin) temperature.
    emissivity : Surface emissivity in (0, 1] (default 1.0).
    unit : Unit of temp_surface: "C", "F", or "K" (default "K").

    Returns
    -------
    Net longwave radiation (W/m²); positive values indicate a net gain by the
    surface, negative values a net loss.

    Raises
    ------
    OutOfRangeError
        If emissivity is outside (0, 1].
    InvalidUnitError
        If unit is invalid.

    Notes
    -----
    Upwelling longwave includes emitted plus reflected components:
    LW_up = emissivity * sigma * Ts ** 4 + (1 - emissivity) * lw_down
    LW_net = lw_down - LW_up

    Examples
    --------
    >>> print(round(net_longwave(350.0, 288.0), 2))
    -40.11
    """
    if np.any(emissivity <= 0) or np.any(emissivity > 1):
        raise OutOfRangeError("Emissivity must be in the interval (0, 1].")
    ts_K = convert_temperature(temp_surface, unit.upper(), "K")
    lw_up = emissivity * STEFAN_BOLTZMANN * ts_K**4 + (1 - emissivity) * lw_down
    return lw_down - lw_up


def net_radiation(
    sw_down: float,
    lw_down: float,
    albedo: float,
    temp_surface: float,
    emissivity: float = 1.0,
    unit: str = "K",
) -> float:
    """
    Net all-wave radiation at a surface.

    Combines the net shortwave and net longwave components into the total net
    radiation, positive downward (into the surface).

    Parameters
    ----------
    sw_down : Incoming shortwave irradiance (W/m²).
    lw_down : Incoming longwave irradiance (W/m²).
    albedo : Surface shortwave albedo in [0, 1].
    temp_surface : Surface (skin) temperature.
    emissivity : Surface emissivity in (0, 1] (default 1.0).
    unit : Unit of temp_surface: "C", "F", or "K" (default "K").

    Returns
    -------
    Net all-wave radiation Rn (W/m²).

    Raises
    ------
    OutOfRangeError
        If albedo or emissivity is outside its valid range.
    InvalidUnitError
        If unit is invalid.

    Notes
    -----
    Rn = SW_net + LW_net = sw_down * (1 - albedo) + (lw_down - LW_up)

    Examples
    --------
    >>> print(round(net_radiation(800.0, 350.0, 0.2, 288.0), 2))
    599.89
    """
    sw_net = net_shortwave(sw_down, albedo)
    lw_net = net_longwave(lw_down, temp_surface, emissivity, unit)
    return sw_net + lw_net


def clear_sky_emissivity(temp_air: float, vapor_pressure: float, unit: str = "C") -> float:
    """
    Clear-sky atmospheric emissivity using Brutsaert's relation.

    Estimates the effective emissivity of a cloudless atmosphere from screen-level
    air temperature and vapor pressure, for use in downwelling longwave
    estimates.

    Parameters
    ----------
    temp_air : Air temperature.
    vapor_pressure : Near-surface actual vapor pressure (kPa), must be positive.
    unit : Unit of temp_air: "C", "F", or "K" (default "C").

    Returns
    -------
    Clear-sky atmospheric emissivity (dimensionless).

    Raises
    ------
    OutOfRangeError
        If vapor_pressure is not positive.
    InvalidUnitError
        If unit is invalid.

    Notes
    -----
    Brutsaert (1975):
    emissivity = 1.24 * (e / T) ** (1 / 7)
    with e in hectopascals (hPa) and T in kelvin. Vapor pressure supplied in kPa
    is converted to hPa internally.

    Examples
    --------
    >>> print(round(clear_sky_emissivity(20, 1.5), 4))
    0.8109
    """
    if np.any(vapor_pressure <= 0):
        raise OutOfRangeError("Vapor pressure must be positive.")
    temp_K = convert_temperature(temp_air, unit.upper(), "K")
    e_hpa = vapor_pressure * 10.0  # kPa -> hPa
    return 1.24 * (e_hpa / temp_K) ** (1.0 / 7.0)