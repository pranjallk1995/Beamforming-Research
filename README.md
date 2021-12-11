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
![jupyterlab](https://img.shields.io/badge/jupyterlab-v3.2.4-information)
![jupyterlab (latest)](https://img.shields.io/pypi/v/jupyterlab?label=lateset)

# Introduction
This Repository is a compilation of Cosine-Beamforming implementation in python as a part of our research.


### Owners:
Pranjall Kumar, Jr. Data Scientist @ Siemens Gamesa (DVL)

Sureshkumar Natrajan, Research scholar @ Universiti Putra Malaysia

<sub>(In alphabetical order)</sub>

# Aim
To find the angular position of the source of sound with the help of a microphone array in a 2D plane.

![2D scenario](/Images/2D_Scenario.jpg "Experimantal Setup")

# Assumptions
1. There are 6 omnidirectional microphones in a linear array.
1. All microphones are at a common fixed distance away from each other.
1. The position of the source of sound is unknown in a 2D plane.
1. The souce of sound is to left of the normal to microphone array (minor change in code will fix this).
1. The source of sound is a point source.
1. The source of sound is sufficiently far away from the microphone array.
1. The source of sound is in a fixed position with respect to all the microphones.
1. The source of sound produces some sound for a very breif amount of time (max 0.2 seconds).
1. The source of sound is stationary.
1. There is minimal noise (max 0.5 units).
1. There is no echo.
1. There is minimal distortion.
1. Microphones are of good quality.

# Units
| Metrics | Units |
|---------|-------|
| Distance | meters |
| Sampling | samples/seconds |
| Time | seconds |
| Angle | degrees |

# Parameter List
| Parameter | Value | Descripttion |
|-----------|-------|--------------|
| $D$ | Unknown | Longitudinal distance of the source of sound from the microphone array. |
| $\theta$ | Unknown | Angle made by the source of sound from the normal to the microphone array. |
| $d$ | To be decided | Distance between each microphone. |
| Sampling Rate | 44100 samples/second | The number of samples taken from a continuous signal to make a digital signal. |
| Scanning Window | 1.08 seconds | The duration of signal considered for finding the source. |
| shift | 2000 | Represents the shift of signal in time from source to the closest microphone (not necessary in experiments) |
| offset | variable | Represents the shift of signal in time from microphone to microphone (depends on $d$ and $\theta$). |
| number_of_microphones | 6 | Represents the number of microphones in the microphone array. |
| step | 100 | Represents the increments of shift in time for a signal. |
| reference_pulse | NA | The first sound pulse received by any microphone. |
| resultant_pulse | NA | The final amplified sound pulse. |
