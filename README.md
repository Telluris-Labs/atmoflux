# atmoflux
A Python package for atmospheric and surface flux calculation and analysis.

## Overview

**atmoflux** is a Python library for atmospheric and surface flux calculations relevant to climate, micrometeorology, and urban environmental research. The package provides modular tools for radiative, turbulent, hydrological, aerosol, and energy balance calculations, alongside supporting utilities for atmospheric state variables and physical constants.

The **atmoflux** library emphasizes physically explicit formulations and transparent diagnostics, supporting process-based analysis and integration with statistical or machine learning models. All functions accept scalars or NumPy arrays, so calculations vectorize naturally over gridded or time-series data.

**atmoflux** is being developed alongside dissertation research focused on urban microclimates, heat stress, and land–atmosphere interactions, and is intended to evolve as a flexible research framework rather than a fixed operational model.

## Requirements

- Python ≥ 3.9 
- [NumPy](https://numpy.org/) ≥ 1.22 — the only runtime dependency

Keeping the dependency footprint minimal is a deliberate design goal; NumPy is the sole external requirement.

## Installation

### From PyPI (recommended)

```bash
pip install atmoflux
```

### From source

Clone the repository and install from the project root. Use an editable
install if you intend to modify the code:

```bash
git clone https://github.com/TellurisLabs/atmoflux.git
cd atmoflux

pip install .       # regular installation
pip install -e .    # editable (development) installation
```

## Quick Start

```python
import atmoflux as af

# Net all-wave radiation at a surface (W/m²)
rn = af.radiative.net_radiation(
    sw_down=800, lw_down=350, albedo=0.2, temp_surface=295
)

# Turbulent sensible heat flux via the bulk-aerodynamic method
rho = af.turbulent.air_density(temp=22, pressure=101.325)
h = af.turbulent.sensible_heat_flux(
    rho, wind_speed=3.0, temp_air=22, temp_surface=25, transfer_coeff=0.0013
)

# Assemble a surface energy balance with derived diagnostics
eb = af.balance.energy_balance(
    rn, sensible_heat=h, latent_heat=250, ground_heat=60
)
print(eb.residual)       # closure residual (W/m²)
print(eb.bowen_ratio)    # H / LE
```

## Modules

**State variables**

| Module | Description |
| --- | --- |
| `temperature` | Unit conversion, dew point, potential and virtual temperature, lapse rate, surface temperature from longwave |
| `humidity` | Saturation and actual vapor pressure, relative and specific humidity, mixing ratio, vapor pressure deficit, absolute humidity |
| `wind` | Speed unit conversion, vector components, log and power-law profiles, friction velocity, shear |

**Flux / process**

| Module | Description |
| --- | --- |
| `radiative` | Blackbody emission, net shortwave and longwave, net radiation, clear-sky emissivity |
| `turbulent` | Air density, bulk-aerodynamic sensible and latent heat fluxes, transfer coefficients |
| `hydro` | Latent-heat-to-evaporation conversion, Penman, Penman-Monteith, FAO-56 reference ET |
| `aerosols` | Gravitational settling, dry deposition, surface emission flux |
| `balance` | Energy budget residual, Bowen ratio, `EnergyBalance` assembly |

**Support**

| Module | Description |
| --- | --- |
| `constants` | Physical and derived constants with documented units |
| `core` | Shared data structures, including the `EnergyBalance` container |
| `exceptions` | Package exception hierarchy rooted at `AtmofluxError` |

## Testing

The package ships with a `pytest` suite mirroring the module structure, plus doctests in every public function.

```bash
# Unit tests
pytest atmoflux/tests/

# Docstring examples
pytest --doctest-modules atmoflux/
```

## License

Released under the MIT License. See the [`LICENSE`](LICENSE) file for details.