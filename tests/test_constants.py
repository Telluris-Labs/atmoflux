"""Tests for atmoflux.constants."""
from atmoflux import constants as c


def test_pressure_constants_in_kpa():
    # Standard sea-level pressure expressed in kPa.
    assert c.P0 == 101.325


def test_psychrometric_constant_kpa_scale():
    # PC was standardized to kPa/K (~0.066), not the old hPa value (~0.66).
    assert 0.05 < c.PC < 0.08


def test_molecular_weight_ratio():
    assert abs(c.RMW - 0.622) < 1e-6


def test_stefan_boltzmann_value():
    assert abs(c.STEFAN_BOLTZMANN - 5.670374419e-8) < 1e-15


def test_karman_constant():
    assert 0.38 <= c.KARMAN <= 0.42
