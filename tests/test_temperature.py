"""Tests for atmoflux.temperature."""
import numpy as np
import pytest

from atmoflux import temperature as T
from atmoflux.exceptions import InvalidUnitError, OutOfRangeError, ValidationError


@pytest.mark.parametrize(
    "value, src, dst, expected",
    [
        (100, "C", "F", 212.0),
        (273.15, "K", "C", 0.0),
        (32, "F", "C", 0.0),
        (0, "C", "K", 273.15),
        (25, "C", "C", 25),
    ],
)
def test_convert_temperature(value, src, dst, expected):
    assert T.convert_temperature(value, src, dst) == pytest.approx(expected)


def test_convert_temperature_array():
    out = T.convert_temperature(np.array([0.0, 100.0]), "C", "F")
    assert np.allclose(out, [32.0, 212.0])


def test_convert_temperature_bad_unit():
    with pytest.raises(InvalidUnitError):
        T.convert_temperature(20, "C", "Z")


def test_convert_temperature_non_numeric():
    with pytest.raises(ValidationError):
        T.convert_temperature("hot", "C", "F")


def test_dewpoint_temperature_value():
    assert T.dewpoint_temperature(30, 50) == pytest.approx(18.438, abs=1e-3)


def test_dewpoint_temperature_full_saturation():
    # At 100% RH the dew point equals the air temperature.
    assert T.dewpoint_temperature(20, 100) == pytest.approx(20.0, abs=1e-6)


def test_dewpoint_temperature_bad_rh():
    with pytest.raises(OutOfRangeError):
        T.dewpoint_temperature(20, 0)


def test_dewpoint_from_avp_roundtrip():
    assert T.dewpoint_from_avp(2.338) == pytest.approx(20.0, abs=1e-2)


def test_dewpoint_from_avp_negative():
    with pytest.raises(OutOfRangeError):
        T.dewpoint_from_avp(-1.0)


def test_potential_temperature_at_reference():
    # At the reference pressure, potential temperature equals temperature.
    assert T.potential_temperature(300.0, 101.325) == pytest.approx(300.0)


def test_potential_temperature_value():
    assert T.potential_temperature(273.15, 80.0) == pytest.approx(292.22, abs=1e-2)


def test_potential_temperature_bad_pressure():
    with pytest.raises(OutOfRangeError):
        T.potential_temperature(300.0, -10.0)


def test_virtual_temperature_exceeds_actual():
    assert T.virtual_temperature(300.0, 0.01) > 300.0


def test_virtual_temperature_dry_air():
    assert T.virtual_temperature(300.0, 0.0) == pytest.approx(300.0)


def test_virtual_temperature_negative_mixing():
    with pytest.raises(OutOfRangeError):
        T.virtual_temperature(300.0, -0.01)


def test_lapse_rate_value():
    assert T.lapse_rate(15.0, 8.5, 0.0, 1000.0) == pytest.approx(0.0065, abs=1e-5)


def test_lapse_rate_inversion_negative():
    # Temperature increasing with height -> negative lapse rate.
    assert T.lapse_rate(10.0, 12.0, 0.0, 500.0) < 0


def test_lapse_rate_equal_heights():
    with pytest.raises(OutOfRangeError):
        T.lapse_rate(15.0, 8.0, 100.0, 100.0)


def test_surface_temperature_from_lw_value():
    assert T.surface_temperature_from_lw(390.0) == pytest.approx(287.98, abs=1e-2)


def test_surface_temperature_from_lw_bad_flux():
    with pytest.raises(OutOfRangeError):
        T.surface_temperature_from_lw(-5.0)


def test_surface_temperature_from_lw_bad_emissivity():
    with pytest.raises(OutOfRangeError):
        T.surface_temperature_from_lw(390.0, emissivity=1.5)
