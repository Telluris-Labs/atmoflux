"""Tests for atmoflux.solar."""
import numpy as np
import pytest

from atmoflux import solar as S
from atmoflux.exceptions import OutOfRangeError


def test_day_of_year_value():
    assert S.day_of_year(2024, 1, 1) == 1
    assert S.day_of_year(2023, 12, 31) == 365


def test_day_of_year_invalid_date():
    with pytest.raises(OutOfRangeError):
        S.day_of_year(2023, 2, 30)


def test_solar_declination_summer_solstice():
    assert S.solar_declination(172) == pytest.approx(23.45, abs=0.01)


def test_solar_declination_winter():
    assert S.solar_declination(355) == pytest.approx(-23.45, abs=0.01)


def test_solar_declination_bad_doy():
    with pytest.raises(OutOfRangeError):
        S.solar_declination(400)


@pytest.mark.parametrize(
    "solar_time, expected", [(12.0, 0.0), (6.0, -90.0), (18.0, 90.0)]
)
def test_hour_angle(solar_time, expected):
    assert S.hour_angle(solar_time) == pytest.approx(expected)


def test_hour_angle_out_of_range():
    with pytest.raises(OutOfRangeError):
        S.hour_angle(24.0)


def test_solar_zenith_overhead():
    assert S.solar_zenith_angle(0.0, 0.0, 0.0) == pytest.approx(0.0, abs=1e-6)


def test_solar_zenith_value():
    assert S.solar_zenith_angle(40.0, 20.0, 0.0) == pytest.approx(20.0, abs=1e-6)


def test_solar_elevation_complements_zenith():
    lat, dec, ha = 35.0, 10.0, 30.0
    z = S.solar_zenith_angle(lat, dec, ha)
    e = S.solar_elevation(lat, dec, ha)
    assert z + e == pytest.approx(90.0)


def test_sunset_hour_angle_equator_equinox():
    assert S.sunset_hour_angle(0.0, 0.0) == pytest.approx(90.0)


def test_daylight_hours_equator_equinox():
    assert S.daylight_hours(0.0, 0.0) == pytest.approx(12.0)


def test_extraterrestrial_radiation_value():
    assert S.extraterrestrial_radiation(0.0, 172) == pytest.approx(33.22, abs=0.05)


def test_extraterrestrial_radiation_bad_doy():
    with pytest.raises(OutOfRangeError):
        S.extraterrestrial_radiation(0.0, 0)


def test_clear_sky_radiation_value():
    assert S.clear_sky_radiation(36.16, 10.0, 12.0) == pytest.approx(24.107, abs=1e-3)


def test_clear_sky_radiation_bad_daylight():
    with pytest.raises(OutOfRangeError):
        S.clear_sky_radiation(36.16, 10.0, 0.0)


def test_declination_array():
    out = S.solar_declination(np.array([172, 355]))
    assert np.allclose(out, [23.45, -23.45], atol=0.01)
