"""Tests for atmoflux.turbulent."""
import numpy as np
import pytest

from atmoflux import turbulent as Tu
from atmoflux.exceptions import OutOfRangeError


def test_air_density_value():
    assert Tu.air_density(15, 101.325) == pytest.approx(1.225, abs=1e-3)


def test_air_density_bad_pressure():
    with pytest.raises(OutOfRangeError):
        Tu.air_density(15, -1.0)


def test_sensible_heat_flux_value():
    assert Tu.sensible_heat_flux(1.2, 3.0, 20.0, 25.0, 0.0013) == pytest.approx(
        23.517, abs=1e-3
    )


def test_sensible_heat_flux_sign():
    # Warmer surface than air -> upward (positive) sensible heat flux.
    assert Tu.sensible_heat_flux(1.2, 3.0, 20.0, 25.0, 0.0013) > 0
    assert Tu.sensible_heat_flux(1.2, 3.0, 25.0, 20.0, 0.0013) < 0


def test_latent_heat_flux_value():
    assert Tu.latent_heat_flux(1.2, 3.0, 0.008, 0.012, 0.0013) == pytest.approx(
        45.864, abs=1e-3
    )


def test_bulk_transfer_coefficient_value():
    assert Tu.bulk_transfer_coefficient(10.0, 0.03) == pytest.approx(
        0.004741, abs=1e-6
    )


def test_bulk_transfer_coefficient_bad_roughness():
    with pytest.raises(OutOfRangeError):
        Tu.bulk_transfer_coefficient(10.0, 0.0)


def test_air_density_array():
    out = Tu.air_density(np.array([15.0, 15.0]), 101.325)
    assert np.allclose(out, 1.225, atol=1e-3)
