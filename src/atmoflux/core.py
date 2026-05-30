"""
atmoflux.core
=================
Defines shared data structures and base classes used across atmoflux. 
Includes common containers and abstractions for surface, atmospheric, 
or flux state that are not tied to a single physical process.

"""

from __future__ import annotations

# Standard imports
from dataclasses import dataclass

# Outside imports
import numpy as np

@dataclass
class EnergyBalance:
    """
    Container for surface energy-balance components and derived diagnostics.

    Stores the four primary energy-budget terms and computes the budget
    residual and Bowen ratio on construction. All terms use the sign convention
    that net radiation is positive downward (into the surface) and the turbulent
    and storage fluxes are positive when directed away from the surface, so a
    perfectly closed budget gives ``residual == 0``.

    Each field accepts a scalar or a NumPy array; derived attributes broadcast to
    the shape of the inputs.

    Parameters
    ----------
    net_radiation : Net all-wave radiation, Rn (W/m²).
    sensible_heat : Sensible heat flux, H (W/m²).
    latent_heat : Latent heat flux, LE (W/m²).
    ground_heat : Ground (storage) heat flux, G (W/m²), default 0.0.

    Attributes
    ----------
    net_radiation : float or numpy.ndarray
        Net all-wave radiation, Rn (W/m²).
    sensible_heat : float or numpy.ndarray
        Sensible heat flux, H (W/m²).
    latent_heat : float or numpy.ndarray
        Latent heat flux, LE (W/m²).
    ground_heat : float or numpy.ndarray
        Ground heat flux, G (W/m²).
    residual : float or numpy.ndarray
        Budget closure residual, Rn - G - H - LE (W/m²).
    bowen_ratio : float or numpy.ndarray
        Bowen ratio, H / LE (dimensionless); ``inf`` or ``nan`` where LE is 0.

    Examples
    --------
    >>> eb = EnergyBalance(net_radiation=400.0, sensible_heat=150.0,
    ...                    latent_heat=200.0, ground_heat=50.0)
    >>> eb.residual
    0.0
    >>> round(eb.bowen_ratio, 2)
    0.75
    >>> eb
    EnergyBalance(Rn=400.0, H=150.0, LE=200.0, G=50.0, residual=0.0)
    """

    net_radiation: float | np.ndarray
    sensible_heat: float | np.ndarray
    latent_heat: float | np.ndarray
    ground_heat: float | np.ndarray = 0.0

    def __post_init__(self) -> None:
        """Compute the budget residual and Bowen ratio from the stored fluxes."""
        self.residual = (
            self.net_radiation
            - self.ground_heat
            - self.sensible_heat
            - self.latent_heat
        )
        with np.errstate(divide="ignore", invalid="ignore"):
            self.bowen_ratio = np.divide(self.sensible_heat, self.latent_heat)
        # Preserve Python scalars for scalar inputs rather than 0-d arrays.
        if np.ndim(self.bowen_ratio) == 0:
            self.bowen_ratio = float(self.bowen_ratio)

    def __repr__(self) -> str:
        """Compact representation that summarizes arrays by shape and mean."""

        def fmt(value: float | np.ndarray) -> str:
            arr = np.asarray(value, dtype=float)
            if arr.ndim == 0:
                return f"{float(arr):.1f}"
            return f"<array shape={arr.shape}, mean={np.nanmean(arr):.1f}>"

        return (
            f"EnergyBalance(Rn={fmt(self.net_radiation)}, "
            f"H={fmt(self.sensible_heat)}, LE={fmt(self.latent_heat)}, "
            f"G={fmt(self.ground_heat)}, residual={fmt(self.residual)})"
        )

    def to_dict(self) -> dict:
        """
        Convert the energy balance to a dictionary.

        Returns
        -------
        Dictionary containing all primary fluxes and derived diagnostics.

        Examples
        --------
        >>> eb = EnergyBalance(400.0, 150.0, 200.0, 50.0)
        >>> eb.to_dict()["residual"]
        0.0
        """
        return {
            "net_radiation": self.net_radiation,
            "sensible_heat": self.sensible_heat,
            "latent_heat": self.latent_heat,
            "ground_heat": self.ground_heat,
            "residual": self.residual,
            "bowen_ratio": self.bowen_ratio,
        }