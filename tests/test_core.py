"""Tests for atmoflux.core."""
import numpy as np
import pytest

from atmoflux.core import EnergyBalance, AtmosphericState


def test_residual_closed_budget():
    eb = EnergyBalance(400.0, 150.0, 200.0, 50.0)
    assert eb.residual == pytest.approx(0.0)


def test_bowen_ratio_scalar_is_float():
    eb = EnergyBalance(400.0, 150.0, 200.0, 50.0)
    assert isinstance(eb.bowen_ratio, float)
    assert eb.bowen_ratio == pytest.approx(0.75)


def test_default_ground_heat_zero():
    eb = EnergyBalance(400.0, 150.0, 200.0)
    assert eb.ground_heat == 0.0
    assert eb.residual == pytest.approx(50.0)


def test_to_dict_keys():
    eb = EnergyBalance(400.0, 150.0, 200.0, 50.0)
    d = eb.to_dict()
    assert set(d) == {
        "net_radiation",
        "sensible_heat",
        "latent_heat",
        "ground_heat",
        "residual",
        "bowen_ratio",
    }


def test_array_inputs_broadcast():
    rn = np.array([400.0, 500.0])
    eb = EnergyBalance(rn, np.array([150.0, 200.0]), np.array([200.0, 250.0]), 50.0)
    assert np.allclose(eb.residual, [0.0, 0.0])
    assert eb.bowen_ratio.shape == (2,)


def test_bowen_ratio_zero_latent_is_inf():
    eb = EnergyBalance(100.0, 50.0, 0.0)
    assert np.isinf(eb.bowen_ratio)


def test_repr_runs_for_arrays():
    eb = EnergyBalance(np.array([400.0, 500.0]), 150.0, 200.0)
    assert "array" in repr(eb)


def test_atmospheric_state_fields():
    state = AtmosphericState(20.0, 101.325, 3.0, 55.0)
    assert state.temperature == 20.0
    assert state.pressure == 101.325
    assert state.wind_speed == 3.0
    assert state.relative_humidity == 55.0


def test_atmospheric_state_optional_rh():
    state = AtmosphericState(20.0, 101.325, 3.0)
    assert state.relative_humidity is None
    assert "RH=None" in repr(state)


def test_atmospheric_state_to_dict():
    state = AtmosphericState(20.0, 101.325, 3.0, 55.0)
    d = state.to_dict()
    assert set(d) == {"temperature", "pressure", "wind_speed", "relative_humidity"}
    assert d["pressure"] == 101.325


def test_atmospheric_state_array_repr():
    state = AtmosphericState(np.array([18.0, 22.0]), 101.325, 3.0)
    assert "array" in repr(state)
