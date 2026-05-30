"""Tests for atmoflux.wind."""
import numpy as np
import pytest

from atmoflux import wind as W
from atmoflux.exceptions import InvalidUnitError, OutOfRangeError


@pytest.mark.parametrize(
    "speed, src, dst, expected",
    [
        (10, "m/s", "km/h", 36.0),
        (20, "mph", "m/s", 8.9408),
        (1, "knots", "m/s", 0.514444),
        (5, "m/s", "m/s", 5.0),
    ],
)
def test_convert_wind_speed(speed, src, dst, expected):
    assert W.convert_wind_speed(speed, src, dst) == pytest.approx(expected, abs=1e-4)


def test_convert_wind_speed_negative():
    with pytest.raises(OutOfRangeError):
        W.convert_wind_speed(-1, "m/s", "mph")


def test_convert_wind_speed_bad_unit():
    with pytest.raises(InvalidUnitError):
        W.convert_wind_speed(5, "m/s", "furlongs")


def test_wind_speed_pythagorean():
    assert W.wind_speed(3.0, 4.0) == pytest.approx(5.0)


@pytest.mark.parametrize(
    "u, v, expected",
    [
        (0.0, -1.0, 0.0),   # from north
        (-1.0, 0.0, 90.0),  # from east
        (0.0, 1.0, 180.0),  # from south
        (1.0, 0.0, 270.0),  # from west
    ],
)
def test_wind_direction(u, v, expected):
    assert W.wind_direction(u, v) == pytest.approx(expected)


def test_log_wind_profile_value():
    assert W.log_wind_profile(5.0, 10.0, 2.0, 0.03) == pytest.approx(3.615, abs=1e-3)


def test_log_wind_profile_identity_at_reference():
    assert W.log_wind_profile(5.0, 10.0, 10.0, 0.03) == pytest.approx(5.0)


def test_log_wind_profile_bad_roughness():
    with pytest.raises(OutOfRangeError):
        W.log_wind_profile(5.0, 10.0, 2.0, 0.0)


def test_power_law_profile_value():
    assert W.power_law_profile(5.0, 10.0, 50.0, 0.143) == pytest.approx(6.294, abs=1e-3)


def test_power_law_profile_bad_height():
    with pytest.raises(OutOfRangeError):
        W.power_law_profile(5.0, 10.0, -50.0, 0.143)


def test_friction_velocity_value():
    assert W.friction_velocity(5.0, 10.0, 0.03) == pytest.approx(0.3443, abs=1e-4)


def test_friction_velocity_bad_height():
    with pytest.raises(OutOfRangeError):
        W.friction_velocity(5.0, 0.01, 0.03)


def test_wind_shear_value():
    assert W.wind_shear(3.0, 7.0, 10.0, 50.0) == pytest.approx(0.1)


def test_wind_shear_equal_heights():
    with pytest.raises(OutOfRangeError):
        W.wind_shear(3.0, 7.0, 10.0, 10.0)


def test_log_wind_profile_array():
    out = W.log_wind_profile(5.0, 10.0, np.array([2.0, 10.0]), 0.03)
    assert np.allclose(out, [3.615, 5.0], atol=1e-3)
