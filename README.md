# Modules
![numpy](https://img.shields.io/badge/numpy-v1.21.4-information)
![numpy (latest)](https://img.shields.io/pypi/v/numpy?label=lateset)
![scipy](https://img.shields.io/badge/scipy-v1.7.3-information)
![scipy (latest)](https://img.shields.io/pypi/v/scipy?label=lateset)
![plotly](https://img.shields.io/badge/plotly-v5.4.0-information)
![plotly (latest)](https://img.shields.io/pypi/v/plotly?label=lateset)
![nbformat](https://img.shields.io/badge/nbformat-v5.1.3-information)
![nbformat (latest)](https://img.shields.io/pypi/v/nbformat?label=lateset)
![chart-studio](https://img.shields.io/badge/chart--studio-v1.1.0-information)
![chart-studio (latest)](https://img.shields.io/pypi/v/chart-studio?label=lateset)
![tqdm](https://img.shields.io/badge/tqdm-v4.62.3-information)
![tqdm (latest)](https://img.shields.io/pypi/v/tqdm?label=lateset)
![prettytable](https://img.shields.io/badge/prettytable-v2.4.0-information)
![prettytable (latest)](https://img.shields.io/pypi/v/prettytable?label=lateset)
![ipywidgets](https://img.shields.io/badge/ipywidgets-v7.6.5-information)
![ipywidgets (latest)](https://img.shields.io/pypi/v/ipywidgets?label=lateset)

# Introduction
This Repository is a compilation of Beamforming experiments in python as a part of our research.

# Aim
To find the angular position of the source of sound with the help of a microphone array in a 2D plane.

# Assumptions
1. There are 6 microphones in a linear array.
1. All microphones are at a common fixed distance away from each other.
1. The position of the source of sound is unknown in a 2D plane.
1. The source of sound is in a fixed position with respect to all the microphones.
1. The source of sound produces some sound for a very breif amount of time (max 0.2 seconds).
1. There is minimal noise (max 0.5 ?).
1. There is no echo.
1. There is minimal distortion.
1. Microphones are of good quality.

# Units
| Metrics | Units |
|---------|-------|
| Amplitude | ? |
| Sampling | samples/seconds |
| Time | seconds |
