"""
atmoflux.wind
=================
Contains functions and profiles related to atmospheric wind. 
Includes wind speed unit conversion, speed and direction from vector components,
logarithmic and power-law height adjustment, friction velocity, and wind shear.

"""

from __future__ import annotations

# Outside imports
import numpy as np

# imports from within atmoflux
from .constants import KARMAN
from .exceptions import InvalidUnitError, OutOfRangeError

# Conversion factors to meters per second.
_WIND_TO_MS = {
    "m/s": 1.0,
    "mph": 0.44704,
    "km/h": 1000.0 / 3600.0,
    "knots": 0.514444,
}


def convert_wind_speed(speed: float, from_unit: str, to_unit: str) -> float:
    """
    Convert wind speed between m/s, mph, km/h, and knots.

    Parameters
    ----------
    speed : Wind speed value (scalar or array-like), must be non-negative.
    from_unit : Input unit: "m/s", "mph", "km/h", or "knots".
    to_unit : Output unit: "m/s", "mph", "km/h", or "knots".

    Returns
    -------
    Wind speed in the specified output unit.

    Raises
    ------
    OutOfRangeError
        If speed is negative.
    InvalidUnitError
        If from_unit or to_unit is not a recognized wind-speed unit.

    Examples
    --------
    >>> print(round(convert_wind_speed(10, "m/s", "km/h"), 1))
    36.0
    >>> print(round(convert_wind_speed(20, "mph", "m/s"), 4))
    8.9408
    """
    if np.any(speed < 0):
        raise OutOfRangeError("Wind speed must be non-negative.")

    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    if from_unit not in _WIND_TO_MS:
        raise InvalidUnitError(f"from_unit must be one of {set(_WIND_TO_MS)}")
    if to_unit not in _WIND_TO_MS:
        raise InvalidUnitError(f"to_unit must be one of {set(_WIND_TO_MS)}")

    speed_ms = speed * _WIND_TO_MS[from_unit]
    return speed_ms / _WIND_TO_MS[to_unit]


def wind_speed(u: float, v: float) -> float:
    """
    Wind speed magnitude from zonal and meridional components.

    Parameters
    ----------
    u : Zonal (west-east) wind component.
    v : Meridional (south-north) wind component.

    Returns
    -------
    Wind speed magnitude in the same unit as the components.

    Examples
    --------
    >>> print(wind_speed(3.0, 4.0))
    5.0
    """
    return np.hypot(u, v)


def wind_direction(u: float, v: float) -> float:
    """
    Meteorological wind direction from zonal and meridional components.

    Returns the compass direction the wind is blowing *from*, in degrees, where
    0 (or 360) is from the north, 90 from the east, 180 from the south, and 270
    from the west.

    Parameters
    ----------
    u : Zonal (west-east) wind component, positive eastward.
    v : Meridional (south-north) wind component, positive northward.

    Returns
    -------
    Wind direction in degrees on [0, 360).

    Notes
    -----
    direction = (270 - degrees(atan2(v, u))) mod 360

    Examples
    --------
    >>> print(wind_direction(0.0, -1.0))
    0.0
    >>> print(wind_direction(-1.0, 0.0))
    90.0
    """
    return (270.0 - np.degrees(np.arctan2(v, u))) % 360.0


def log_wind_profile(
    speed_ref: float,
    height_ref: float,
    height: float,
    roughness: float,
    displacement: float = 0.0,
) -> float:
    """
    Adjust wind speed to a new height using the logarithmic wind profile.

    Applies the neutral-stability logarithmic profile to scale a measured wind
    speed from a reference height to a target height over a surface with a given
    aerodynamic roughness length.

    Parameters
    ----------
    speed_ref : Wind speed measured at the reference height.
    height_ref : Reference measurement height (m), above displacement + roughness.
    height : Target height (m), above displacement + roughness.
    roughness : Aerodynamic roughness length z0 (m), must be positive.
    displacement : Zero-plane displacement height d (m), default 0.0.

    Returns
    -------
    Wind speed at the target height, same unit as speed_ref.

    Raises
    ------
    OutOfRangeError
        If roughness is not positive or either height is not above d + z0.

    Notes
    -----
    Neutral logarithmic profile:
    u(z) = u_ref * ln((z - d) / z0) / ln((z_ref - d) / z0)

    Examples
    --------
    >>> print(round(log_wind_profile(5.0, 10.0, 2.0, 0.03), 3))
    3.615
    """
    if np.any(roughness <= 0):
        raise OutOfRangeError("Roughness length must be positive.")
    if np.any((height - displacement) <= roughness) or np.any(
        (height_ref - displacement) <= roughness
    ):
        raise OutOfRangeError("Heights must exceed displacement plus roughness length.")

    return speed_ref * (
        np.log((height - displacement) / roughness)
        / np.log((height_ref - displacement) / roughness)
    )


def power_law_profile(
    speed_ref: float, height_ref: float, height: float, exponent: float
) -> float:
    """
    Adjust wind speed to a new height using the power-law wind profile.

    Parameters
    ----------
    speed_ref : Wind speed measured at the reference height.
    height_ref : Reference measurement height (m), must be positive.
    height : Target height (m), must be positive.
    exponent : Power-law (Hellmann) exponent, typically 0.1-0.4 by terrain.

    Returns
    -------
    Wind speed at the target height, same unit as speed_ref.

    Raises
    ------
    OutOfRangeError
        If either height is not positive.

    Notes
    -----
    Power law:
    u(z) = u_ref * (z / z_ref) ** exponent

    Examples
    --------
    >>> print(round(power_law_profile(5.0, 10.0, 50.0, 0.143), 3))
    6.294
    """
    if np.any(height <= 0) or np.any(height_ref <= 0):
        raise OutOfRangeError("Heights must be positive.")
    return speed_ref * (height / height_ref) ** exponent


def friction_velocity(
    speed: float,
    height: float,
    roughness: float,
    displacement: float = 0.0,
    karman: float = KARMAN,
) -> float:
    """
    Friction velocity from a single wind measurement (neutral stability).

    Parameters
    ----------
    speed : Wind speed at the measurement height.
    height : Measurement height (m), above displacement + roughness.
    roughness : Aerodynamic roughness length z0 (m), must be positive.
    displacement : Zero-plane displacement height d (m), default 0.0.
    karman : von Kármán constant (default from constants).

    Returns
    -------
    Friction velocity u* in the same unit as speed.

    Raises
    ------
    OutOfRangeError
        If roughness is not positive or height is not above d + z0.

    Notes
    -----
    Neutral surface-layer relation:
    u* = k * u / ln((z - d) / z0)

    Examples
    --------
    >>> print(round(friction_velocity(5.0, 10.0, 0.03), 4))
    0.3443
    """
    if np.any(roughness <= 0):
        raise OutOfRangeError("Roughness length must be positive.")
    if np.any((height - displacement) <= roughness):
        raise OutOfRangeError("Height must exceed displacement plus roughness length.")

    return karman * speed / np.log((height - displacement) / roughness)


def wind_shear(
    speed_lower: float, speed_upper: float, height_lower: float, height_upper: float
) -> float:
    """
    Vertical wind shear between two heights.

    Parameters
    ----------
    speed_lower : Wind speed at the lower height.
    speed_upper : Wind speed at the upper height.
    height_lower : Lower height (m).
    height_upper : Upper height (m), must differ from height_lower.

    Returns
    -------
    Wind shear (du/dz) in speed units per meter.

    Raises
    ------
    OutOfRangeError
        If the two heights are equal.

    Notes
    -----
    shear = (u_upper - u_lower) / (z_upper - z_lower)

    Examples
    --------
    >>> print(round(wind_shear(3.0, 7.0, 10.0, 50.0), 3))
    0.1
    """
    if np.any(height_upper == height_lower):
        raise OutOfRangeError("Upper and lower heights must differ.")
    return (speed_upper - speed_lower) / (height_upper - height_lower)