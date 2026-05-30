"""
atmoflux.balance
=================
Calculates net energy budgets and surface energy balance diagnostics. 
Aggregates radiative, turbulent, and storage fluxes to compute Bowen ratios,
closure residuals, and an EnergyBalance container.

"""

from __future__ import annotations

# Outside imports
import numpy as np

# imports from within atmoflux
from .core import EnergyBalance
from .exceptions import OutOfRangeError

def surface_energy_residual(
        net_radiation: float, 
        sensible_heat: float, 
        latent_heat: float, 
        ground_heat: float = 0.0,
) -> float:
    """
    Surface energy balance closure residual.

    Parameters
    ----------
    net_radiation : Net all-wave radiation Rn (W/m²).
    sensible_heat : Sensible heat flux H (W/m²).
    latent_heat : Latent heat flux LE (W/m²).
    ground_heat : Ground heat flux G (W/m²), default 0.0.

    Returns
    -------
    Closure residual Rn - G - H - LE (W/m²); zero for a perfectly closed budget.

    Notes
    -----
    residual = Rn - G - H - LE
    A nonzero residual indicates lack of energy balance closure, commonly seen in
    eddy-covariance observations.

    Examples
    --------
    >>> surface_energy_residual(400.0, 150.0, 200.0, 50.0)
    0.0
    """
    return net_radiation - ground_heat - sensible_heat - latent_heat


def bowen_ratio(sensible_heat: float, latent_heat: float) -> float:
    """
    Bowen ratio of sensible to latent heat flux.

    Parameters
    ----------
    sensible_heat : Sensible heat flux H (W/m²).
    latent_heat : Latent heat flux LE (W/m²), should be nonzero.

    Returns
    -------
    Bowen ratio H / LE (dimensionless); ``inf`` or ``nan`` where LE is 0.

    Notes
    -----
    beta = H / LE
    Values well above 1 indicate dry surfaces dominated by sensible heating;
    values below 1 indicate moist surfaces dominated by evaporation.

    Examples
    --------
    >>> round(bowen_ratio(150.0, 200.0), 3)
    0.75
    """
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.divide(sensible_heat, latent_heat)
    if np.ndim(ratio) == 0:
        return float(ratio)
    return ratio


def energy_balance(
    net_radiation: float,
    sensible_heat: float,
    latent_heat: float,
    ground_heat: float = 0.0,
) -> EnergyBalance:
    """
    Assemble an EnergyBalance container from surface flux components.

    Parameters
    ----------
    net_radiation : Net all-wave radiation Rn (W/m²).
    sensible_heat : Sensible heat flux H (W/m²).
    latent_heat : Latent heat flux LE (W/m²).
    ground_heat : Ground heat flux G (W/m²), default 0.0.

    Returns
    -------
    An :class:`atmoflux.core.EnergyBalance` with the fluxes and derived residual
    and Bowen ratio.

    Examples
    --------
    >>> eb = energy_balance(400.0, 150.0, 200.0, 50.0)
    >>> eb.residual
    0.0
    >>> round(eb.bowen_ratio, 2)
    0.75
    """
    return EnergyBalance(
        net_radiation=net_radiation,
        sensible_heat=sensible_heat,
        latent_heat=latent_heat,
        ground_heat=ground_heat,
    )