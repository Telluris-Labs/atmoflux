"""Tests for atmoflux.humidity."""
import numpy as np
import pytest

from atmoflux import humidity as H
from atmoflux.exceptions import OutOfRangeError


def test_saturation_vp_value():
    assert H.saturation_vp(20) == pytest.approx(2.3382, abs=1e-4)


def test_saturation_vp_array():
    out = H.saturation_vp(np.array([0.0, 20.0]))
    assert np.allclose(out, [0.61078, 2.3382], atol=1e-4)


def test_actual_vp_value():
    assert H.actual_vp(10) == pytest.approx(1.2279, abs=1e-4)


def test_saturation_vp_slope_value():
    assert H.saturation_vp_slope(20) == pytest.approx(0.1447, abs=1e-4)


def test_relative_humidity_value():
    assert H.relative_humidity(20, 10) == pytest.approx(52.5, abs=0.1)


def test_relative_humidity_saturated():
    # Dew point equal to temperature implies 100% RH.
    assert H.relative_humidity(15, 15) == pytest.approx(100.0)


def test_specific_humidity_value():
    assert H.specific_humidity(1.2279, 101.325) == pytest.approx(0.00757, abs=1e-5)


def test_specific_humidity_bad_pressure():
    with pytest.raises(OutOfRangeError):
        H.specific_humidity(2.0, 1.0)


def test_mixing_ratio_value():
    assert H.mixing_ratio(1.2279, 101.325) == pytest.approx(0.00763, abs=1e-5)


def test_mixing_ratio_exceeds_specific_humidity():
    e, p = 1.5, 101.325
    assert H.mixing_ratio(e, p) > H.specific_humidity(e, p)


def test_vapor_pressure_deficit_value():
    assert H.vapor_pressure_deficit(25, 60) == pytest.approx(1.2671, abs=1e-4)


def test_vapor_pressure_deficit_bad_rh():
    with pytest.raises(OutOfRangeError):
        H.vapor_pressure_deficit(25, 150)


def test_absolute_humidity_value():
    assert H.absolute_humidity(1.2279, 20) == pytest.approx(0.00908, abs=1e-5)


def test_saturation_vp_ice_value():
    assert H.saturation_vp_ice(-10) == pytest.approx(0.2595, abs=1e-4)


def test_saturation_vp_ice_below_water():
    # Over ice, saturation vapor pressure is below that over supercooled water.
    assert H.saturation_vp_ice(-10) < H.saturation_vp(-10)


def test_specific_humidity_from_dewpoint_value():
    assert H.specific_humidity_from_dewpoint(10, 101.325) == pytest.approx(
        0.00757, abs=1e-5
    )


def test_specific_humidity_from_dewpoint_bad_pressure():
    with pytest.raises(OutOfRangeError):
        H.specific_humidity_from_dewpoint(10, 0.5)


def test_rh_from_specific_humidity_value():
    assert H.relative_humidity_from_specific_humidity(
        0.00757, 20, 101.325
    ) == pytest.approx(52.5, abs=0.1)


def test_rh_from_specific_humidity_roundtrip():
    # q -> RH should invert RH -> q (via dewpoint) to within tolerance.
    q = H.specific_humidity_from_dewpoint(10, 101.325)
    rh = H.relative_humidity_from_specific_humidity(q, 20, 101.325)
    assert rh == pytest.approx(H.relative_humidity(20, 10), abs=0.5)


def test_rh_from_specific_humidity_bad_pressure():
    with pytest.raises(OutOfRangeError):
        H.relative_humidity_from_specific_humidity(0.005, 20, -1.0)


def test_precipitable_water_value():
    assert H.precipitable_water(0.01, 101.325) == pytest.approx(103.32, abs=1e-2)


def test_precipitable_water_bad_humidity():
    with pytest.raises(OutOfRangeError):
        H.precipitable_water(-0.001, 101.325)
