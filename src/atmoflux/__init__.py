"""
atmoflux: tools for computing atmospheric and surface fluxes.

This package provides state-variable helpers (temperature, humidity, wind),
physical constants, and process-based flux calculations for radiative,
turbulent, hydrological, aerosol, and energy balance applications.

"""

# Package metadata
__version__ = "0.1.0"
__author__ = "Telluris Labs"
__email__ = "info@tellurislabs.io"
__license__ = "MIT"
__description__ = "Custom tools for climate data processing and analysis"

# State and constants
from . import temperature
from . import humidity
from . import wind
from . import constants

# Flux / process modules
from . import radiative
from . import turbulent
from . import hydro
from . import aerosols
from . import balance

# Shared core abstractions
from . import core
from . import exceptions

__all__ = [
    "temperature",
    "humidity",
    "wind",
    "constants",
    "radiative",
    "turbulent",
    "hydro",
    "aerosols",
    "balance",
    "core",
    "exceptions",
]