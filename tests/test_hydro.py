"""Tests for atmoflux.hydro."""
import pytest

from atmoflux import hydro as Hy
from atmoflux.exceptions import OutOfRangeError


def test_latent_heat_to_evaporation_value():
    assert Hy.latent_heat_to_evaporation(100.0) == pytest.approx(3.527, abs=1e-3)


def test_latent_heat_to_evaporation_zero():
    assert Hy.latent_heat_to_evaporation(0.0) == pytest.approx(0.0)


def test_latent_heat_to_evaporation_bad_density():
    with pytest.raises(OutOfRangeError):
        Hy.latent_heat_to_evaporation(100.0, density_water=0.0)


def test_penman_evaporation_value():
    result = Hy.penman_evaporation(15.0, 0.0, 25.0, 2.0, 3.169, 1.9, 101.3)
    assert result == pytest.approx(6.326, abs=1e-3)


def test_penman_evaporation_bad_wind():
    with pytest.raises(OutOfRangeError):
        Hy.penman_evaporation(15.0, 0.0, 25.0, -2.0, 3.169, 1.9)


def test_penman_monteith_value():
    result = Hy.penman_monteith(150.0, 20.0, 25.0, 1.5, 1.2, 50.0, 70.0)
    assert result == pytest.approx(6.133, abs=1e-3)


def test_penman_monteith_bad_resistance():
    with pytest.raises(OutOfRangeError):
        Hy.penman_monteith(150.0, 20.0, 25.0, 1.5, 1.2, 0.0, 70.0)


def test_penman_monteith_negative_vpd():
    with pytest.raises(OutOfRangeError):
        Hy.penman_monteith(150.0, 20.0, 25.0, -0.1, 1.2, 50.0, 70.0)


def test_potential_evapotranspiration_value():
    result = Hy.potential_evapotranspiration(15.0, 0.0, 25.0, 2.0, 3.169, 1.9, 101.3)
    assert result == pytest.approx(5.539, abs=1e-3)


def test_open_water_exceeds_reference_et():
    # Open-water Penman evaporation should exceed grass reference ET0.
    pe = Hy.penman_evaporation(15.0, 0.0, 25.0, 2.0, 3.169, 1.9, 101.3)
    et0 = Hy.potential_evapotranspiration(15.0, 0.0, 25.0, 2.0, 3.169, 1.9, 101.3)
    assert pe > et0
