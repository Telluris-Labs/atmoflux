"""Tests for atmoflux.balance."""
import numpy as np
import pytest

from atmoflux import balance as B
from atmoflux.core import EnergyBalance
from atmoflux.exceptions import OutOfRangeError


def test_surface_energy_residual_closed():
    assert B.surface_energy_residual(400.0, 150.0, 200.0, 50.0) == pytest.approx(0.0)


def test_surface_energy_residual_default_ground():
    assert B.surface_energy_residual(400.0, 150.0, 200.0) == pytest.approx(50.0)


def test_bowen_ratio_value():
    assert B.bowen_ratio(150.0, 200.0) == pytest.approx(0.75)


def test_bowen_ratio_scalar_is_float():
    assert isinstance(B.bowen_ratio(150.0, 200.0), float)


def test_bowen_ratio_zero_latent():
    assert np.isinf(B.bowen_ratio(100.0, 0.0))


def test_bowen_ratio_array():
    out = B.bowen_ratio(np.array([150.0, 100.0]), np.array([200.0, 50.0]))
    assert np.allclose(out, [0.75, 2.0])


def test_energy_balance_returns_container():
    eb = B.energy_balance(400.0, 150.0, 200.0, 50.0)
    assert isinstance(eb, EnergyBalance)
    assert eb.residual == pytest.approx(0.0)
    assert eb.bowen_ratio == pytest.approx(0.75)


def test_energy_balance_matches_helpers():
    eb = B.energy_balance(420.0, 160.0, 190.0, 40.0)
    assert eb.residual == pytest.approx(
        B.surface_energy_residual(420.0, 160.0, 190.0, 40.0)
    )
    assert eb.bowen_ratio == pytest.approx(B.bowen_ratio(160.0, 190.0))


def test_available_energy_value():
    assert B.available_energy(400.0, 50.0) == pytest.approx(350.0)


def test_available_energy_default_ground():
    assert B.available_energy(400.0) == pytest.approx(400.0)


def test_energy_balance_ratio_closed():
    assert B.energy_balance_ratio(150.0, 200.0, 400.0, 50.0) == pytest.approx(1.0)


def test_energy_balance_ratio_scalar_is_float():
    assert isinstance(B.energy_balance_ratio(150.0, 200.0, 400.0, 50.0), float)


def test_energy_balance_ratio_zero_available():
    assert np.isinf(B.energy_balance_ratio(150.0, 200.0, 50.0, 50.0))


def test_ground_heat_fraction_value():
    assert B.ground_heat_fraction(400.0) == pytest.approx(40.0)


def test_ground_heat_fraction_custom():
    assert B.ground_heat_fraction(400.0, 0.2) == pytest.approx(80.0)


def test_ground_heat_fraction_bad_fraction():
    with pytest.raises(OutOfRangeError):
        B.ground_heat_fraction(400.0, 1.5)
