"""Tests for atmoflux.stability."""
import numpy as np
import pytest

from atmoflux import stability as St
from atmoflux.exceptions import OutOfRangeError


def test_bulk_richardson_unstable_sign():
    # Temperature decreasing with height -> unstable -> negative Rb.
    assert St.bulk_richardson_number(15, 14, 5.0, 2.0, 10.0) < 0


def test_bulk_richardson_value():
    assert St.bulk_richardson_number(15, 14, 5.0, 2.0, 10.0) == pytest.approx(
        -0.01091, abs=1e-5
    )


def test_bulk_richardson_stable_sign():
    # Temperature increasing with height -> stable -> positive Rb.
    assert St.bulk_richardson_number(14, 15, 5.0, 2.0, 10.0) > 0


def test_bulk_richardson_equal_heights():
    with pytest.raises(OutOfRangeError):
        St.bulk_richardson_number(15, 14, 5.0, 10.0, 10.0)


def test_bulk_richardson_zero_wind():
    with pytest.raises(OutOfRangeError):
        St.bulk_richardson_number(15, 14, 0.0, 2.0, 10.0)


def test_obukhov_length_value():
    assert St.obukhov_length(0.3, 20, 100.0, 1.2) == pytest.approx(-24.334, abs=1e-3)


def test_obukhov_length_unstable_negative():
    # Positive (upward) sensible heat flux -> unstable -> negative L.
    assert St.obukhov_length(0.3, 20, 100.0, 1.2) < 0


def test_obukhov_length_bad_friction_velocity():
    with pytest.raises(OutOfRangeError):
        St.obukhov_length(0.0, 20, 100.0, 1.2)


def test_obukhov_length_zero_flux():
    with pytest.raises(OutOfRangeError):
        St.obukhov_length(0.3, 20, 0.0, 1.2)


def test_stability_parameter_value():
    assert St.stability_parameter(10.0, -50.0) == pytest.approx(-0.2)


def test_stability_parameter_zero_length():
    with pytest.raises(OutOfRangeError):
        St.stability_parameter(10.0, 0.0)


def test_psi_momentum_stable():
    assert St.psi_momentum(0.1) == pytest.approx(-0.5)


def test_psi_momentum_unstable_value():
    assert St.psi_momentum(-0.1) == pytest.approx(0.2836, abs=1e-4)


def test_psi_momentum_neutral_zero():
    assert St.psi_momentum(0.0) == pytest.approx(0.0)


def test_psi_heat_stable():
    assert St.psi_heat(0.1) == pytest.approx(-0.5)


def test_psi_heat_unstable_value():
    assert St.psi_heat(-0.1) == pytest.approx(0.5343, abs=1e-4)


@pytest.mark.parametrize(
    "rb, expected",
    [(-0.5, "unstable"), (0.0, "neutral"), (0.005, "neutral"), (0.5, "stable")],
)
def test_stability_class(rb, expected):
    assert St.stability_class(rb) == expected


def test_psi_momentum_array():
    out = St.psi_momentum(np.array([0.1, -0.1]))
    assert out[0] == pytest.approx(-0.5)
    assert out[1] == pytest.approx(0.2836, abs=1e-4)
