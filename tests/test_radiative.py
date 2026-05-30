"""Tests for atmoflux.radiative."""
import numpy as np
import pytest

from atmoflux import radiative as R
from atmoflux.exceptions import OutOfRangeError


def test_blackbody_radiation_value():
    assert R.blackbody_radiation(288.0) == pytest.approx(390.11, abs=1e-2)


def test_blackbody_radiation_emissivity_scaling():
    full = R.blackbody_radiation(300.0)
    grey = R.blackbody_radiation(300.0, emissivity=0.5)
    assert grey == pytest.approx(0.5 * full)


def test_blackbody_radiation_bad_emissivity():
    with pytest.raises(OutOfRangeError):
        R.blackbody_radiation(300.0, emissivity=0.0)


def test_net_shortwave_value():
    assert R.net_shortwave(800.0, 0.2) == pytest.approx(640.0)


def test_net_shortwave_bad_albedo():
    with pytest.raises(OutOfRangeError):
        R.net_shortwave(800.0, 1.5)


def test_net_longwave_value():
    assert R.net_longwave(350.0, 288.0) == pytest.approx(-40.11, abs=1e-2)


def test_net_radiation_value():
    assert R.net_radiation(800.0, 350.0, 0.2, 288.0) == pytest.approx(599.89, abs=1e-2)


def test_net_radiation_is_sum_of_components():
    sw = R.net_shortwave(800.0, 0.2)
    lw = R.net_longwave(350.0, 288.0)
    assert R.net_radiation(800.0, 350.0, 0.2, 288.0) == pytest.approx(sw + lw)


def test_clear_sky_emissivity_value():
    assert R.clear_sky_emissivity(20, 1.5) == pytest.approx(0.8109, abs=1e-4)


def test_clear_sky_emissivity_bad_vapor_pressure():
    with pytest.raises(OutOfRangeError):
        R.clear_sky_emissivity(20, 0.0)


def test_net_shortwave_array():
    out = R.net_shortwave(np.array([800.0, 400.0]), 0.25)
    assert np.allclose(out, [600.0, 300.0])
