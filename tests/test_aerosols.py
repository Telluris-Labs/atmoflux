"""Tests for atmoflux.aerosols."""
import pytest

from atmoflux import aerosols as A
from atmoflux.exceptions import OutOfRangeError


def test_settling_velocity_submicron():
    assert A.settling_velocity(1e-6, 1000.0) * 1e6 == pytest.approx(35.095, abs=1e-2)


def test_settling_velocity_ten_micron():
    assert A.settling_velocity(10e-6, 1000.0) * 1e3 == pytest.approx(3.06, abs=1e-2)


def test_settling_velocity_increases_with_size():
    small = A.settling_velocity(1e-6, 1000.0)
    large = A.settling_velocity(10e-6, 1000.0)
    assert large > small


def test_settling_velocity_bad_diameter():
    with pytest.raises(OutOfRangeError):
        A.settling_velocity(0.0, 1000.0)


def test_settling_velocity_bad_density():
    with pytest.raises(OutOfRangeError):
        A.settling_velocity(1e-6, -10.0)


def test_dry_deposition_velocity_value():
    vs = A.settling_velocity(10e-6, 1000.0)
    assert A.dry_deposition_velocity(vs, 50.0, 20.0) * 1000 == pytest.approx(
        16.747, abs=1e-2
    )


def test_dry_deposition_exceeds_settling():
    vs = A.settling_velocity(10e-6, 1000.0)
    assert A.dry_deposition_velocity(vs, 50.0, 20.0) > vs


def test_dry_deposition_bad_resistance():
    with pytest.raises(OutOfRangeError):
        A.dry_deposition_velocity(0.003, 0.0, 20.0)


def test_emission_flux_value():
    assert A.emission_flux(2e-6, 0.01) == pytest.approx(2e-8)


def test_emission_flux_negative():
    with pytest.raises(OutOfRangeError):
        A.emission_flux(-1.0, 0.01)
