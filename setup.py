from setuptools import find_packages, setup

setup(
    name="atmoflux",
    packages=find_packages(include=["atmoflux"]),
    version="0.0.1",
    description="Atmospheric and energy flux analysis Python library by Telluris Labs",
    author="Telluris Labs",
    license="MIT",
    python_requires='>=3.9',
    install_requires=["numpy>=1.22"],
    test_suite="tests",
)
