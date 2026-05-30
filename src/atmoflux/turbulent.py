"""
atmoflux.turbulent
=================
Calculates turbulent fluxes driven by wind and surface-air gradients.
Includes moist air density, bulk-aerodynamic sensible and latent heat fluxes, and
neutral bulk transfer coefficients.

"""

from __future__ import annotations

# Outside imports
import numpy as np

# imports from within atmoflux
from .constants import CP_AIR, LV, R_AIR, KARMAN
from .exceptions import OutOfRangeError
from .temperature import convert_temperature


def air_density(temp: float, pressure: float, unit: str = "C") -> float:
    """
    Density of dry air from temperature and pressure (ideal gas law).

    Parameters
    ----------
    temp : Air temperature.
    pressure : Air pressure (kPa), must be positive.
    unit : Unit of temp: "C", "F", or "K" (default "C").

    Returns
    -------
    Air density in kg/m³.

    Raises
    ------
    OutOfRangeError
        If pressure is not positive.
    InvalidUnitError
        If unit is invalid.

    Notes
    -----
    Ideal gas law for dry air:
    rho = P / (R_air * T)
    with P in pascals and T in kelvin.

    Examples
    --------
    >>> print(round(air_density(15, 101.325), 4))
    1.225
    """
    if np.any(pressure <= 0):
        raise OutOfRangeError("Pressure must be positive.")
    temp_K = convert_temperature(temp, unit.upper(), "K")
    p_pa = pressure * 1000.0  # kPa -> Pa
    return p_pa / (R_AIR * temp_K)


def sensible_heat_flux(
    density: float,
    wind_speed: float,
    temp_air: float,
    temp_surface: float,
    transfer_coeff: float,
    unit: str = "C",
) -> float:
    """
    Bulk-aerodynamic sensible heat flux.

    Parameters
    ----------
    density : Air density (kg/m³).
    wind_speed : Wind speed at the reference height (m/s).
    temp_air : Air temperature at the reference height.
    temp_surface : Surface (skin) temperature.
    transfer_coeff : Bulk transfer coefficient for heat (dimensionless).
    unit : Unit of the input temperatures: "C", "F", or "K" (default "C").

    Returns
    -------
    Sensible heat flux H (W/m²), positive when directed from surface to air.

    Raises
    ------
    InvalidUnitError
        If unit is invalid.

    Notes
    -----
    Bulk-aerodynamic form:
    H = rho * cp * Ch * U * (Ts - Ta)
    Temperatures are converted to kelvin so the difference is independent of the
    input scale.

    Examples
    --------
    >>> print(round(sensible_heat_flux(1.2, 3.0, 20.0, 25.0, 0.0013), 4))
    23.517
    """
    ts_K = convert_temperature(temp_surface, unit.upper(), "K")
    ta_K = convert_temperature(temp_air, unit.upper(), "K")
    return density * CP_AIR * transfer_coeff * wind_speed * (ts_K - ta_K)


def latent_heat_flux(
    density: float,
    wind_speed: float,
    q_air: float,
    q_surface: float,
    transfer_coeff: float,
) -> float:
    """
    Bulk-aerodynamic latent heat flux.

    Parameters
    ----------
    density : Air density (kg/m³).
    wind_speed : Wind speed at the reference height (m/s).
    q_air : Specific humidity of the air (kg/kg).
    q_surface : Specific humidity at the surface (kg/kg).
    transfer_coeff : Bulk transfer coefficient for moisture (dimensionless).

    Returns
    -------
    Latent heat flux LE (W/m²), positive for evaporation (surface to air).

    Notes
    -----
    Bulk-aerodynamic form:
    LE = rho * Lv * Ce * U * (q_s - q_a)

    Examples
    --------
    >>> print(round(latent_heat_flux(1.2, 3.0, 0.008, 0.012, 0.0013), 4))
    45.864
    """
    return density * LV * transfer_coeff * wind_speed * (q_surface - q_air)


def bulk_transfer_coefficient(
    height: float, roughness: float, displacement: float = 0.0, karman: float = KARMAN
) -> float:
    """
    Neutral bulk transfer coefficient from surface-layer geometry.

    Parameters
    ----------
    height : Reference height (m), above displacement + roughness.
    roughness : Aerodynamic roughness length z0 (m), must be positive.
    displacement : Zero-plane displacement height d (m), default 0.0.
    karman : von Kármán constant (default from constants).

    Returns
    -------
    Neutral bulk transfer coefficient (dimensionless).

    Raises
    ------
    OutOfRangeError
        If roughness is not positive or height is not above d + z0.

    Notes
    -----
    Assumes neutral stability and equal momentum and scalar roughness lengths:
    C = k ** 2 / ln((z - d) / z0) ** 2

    Examples
    --------
    >>> print(round(bulk_transfer_coefficient(10.0, 0.03), 6))
    0.004741
    """
    if np.any(roughness <= 0):
        raise OutOfRangeError("Roughness length must be positive.")
    if np.any((height - displacement) <= roughness):
        raise OutOfRangeError("Height must exceed displacement plus roughness length.")
    return karman**2 / np.log((height - displacement) / roughness) ** 2