"""
atmoflux: Atmospheric / Energy Flux Library from Telluris Labs
top-level package
"""

# Package metadata
__version__ = "0.0.1"
__author__ = "Telluris Labs"
__email__ = "info@tellurislabs.io"
__license__ = "MIT"
__description__ = "Custom tools for climate data processing and analysis"

# Import modules
from . import temperature
from . import humidity
from . import pressure
from . import solar
from . import longwave
from . import wind

__all__ = [
    'temperature',
    'humidity', 
    'pressure',
    'solar',
    'longwave',
    'wind',
]