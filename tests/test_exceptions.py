"""Tests for atmoflux.exceptions."""
import pytest

from atmoflux.exceptions import (
    AtmofluxError,
    InvalidUnitError,
    OutOfRangeError,
    ValidationError,
)


@pytest.mark.parametrize(
    "exc", [InvalidUnitError, OutOfRangeError, ValidationError]
)
def test_subclasses_inherit_base(exc):
    assert issubclass(exc, AtmofluxError)


@pytest.mark.parametrize(
    "exc", [InvalidUnitError, OutOfRangeError, ValidationError]
)
def test_caught_as_base(exc):
    with pytest.raises(AtmofluxError):
        raise exc("boom")


def test_base_is_exception():
    assert issubclass(AtmofluxError, Exception)
