"""
atmoflux.exceptions
=================
Defines the exception hierarchy for the atmoflux package.

Errors raised by atmoflux derive from :class:`AtmofluxError`, allowing
callers to catch any package-specific failure with a single ``except`` clause.
Specific subclasses cover unit, range, and validation failures.
"""
# Standard imports

# Outside imports

# imports from within atmoflux


class AtmofluxError(Exception):
    """
    Base exception for errors raised by atmoflux.

    Catching this exception will catch every package-specific error. Library
    code should never raise :class:`AtmofluxError` directly; it should raise one
    of the more specific subclasses instead.

    Examples
    --------
    >>> try:
    ...     raise InvalidUnitError("bad unit")
    ... except AtmofluxError as exc:
    ...     print(type(exc).__name__)
    InvalidUnitError
    """


class InvalidUnitError(AtmofluxError):
    """
    Raised when an unrecognized or unsupported unit string is supplied.

    Examples
    --------
    >>> raise InvalidUnitError("Temp unit must be one of {'C', 'F', 'K'}")
    Traceback (most recent call last):
        ...
    atmoflux.exceptions.InvalidUnitError: Temp unit must be one of {'C', 'F', 'K'}
    """


class OutOfRangeError(AtmofluxError):
    """
    Raised when a value falls outside its physically valid range.

    Used for inputs that are the correct type but physically impossible or
    outside the validated domain of a formula (e.g. a negative wind speed or a
    relative humidity above 100%).
    """


class ValidationError(AtmofluxError):
    """
    Raised when an input fails type or value validation.

    Used for inputs of the wrong type (e.g. a non-numeric temperature) or
    structurally invalid arguments that are not specifically unit- or
    range-related.
    """
