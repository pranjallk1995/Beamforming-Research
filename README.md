# Modules
![numpy](https://img.shields.io/badge/numpy-v1.21.4-information)
![numpy (latest)](https://img.shields.io/pypi/v/numpy?label=lateset)
![scipy](https://img.shields.io/badge/scipy-v1.7.3-information)
![scipy (latest)](https://img.shields.io/pypi/v/scipy?label=lateset)
![plotly](https://img.shields.io/badge/plotly-v5.4.0-information)
![plotly (latest)](https://img.shields.io/pypi/v/plotly?label=lateset)
![prettytable](https://img.shields.io/badge/prettytable-v2.4.0-information)
![prettytable (latest)](https://img.shields.io/pypi/v/prettytable?label=lateset)


# Introduction
This Repository is a compilation of Cosine-Beamforming implementation in python as a part of our research.


### Owners
Pranjall Kumar, Jr. Data Scientist @ Siemens Gamesa (DVL)

Sureshkumar Natarajan, Research Scholar @ Universiti Putra Malaysia

<sub>(In alphabetical order)</sub>


# Aim
To find the exact position of the source of sound with the help of two microphone arrays in a 2D plane.


### Experimental Setup
![Experimental_setup](/Images/Experimental_setup.jpg "Experimantal Setup")


### Calculation of $\theta$
![Theta](/Images/Angular_location.jpg "Calculation of Theta")


### Calculation of source location ($p$)
![D](/Images/Actual_location.jpg "Calculation of source location")


# Assumptions
1. There are 3 omnidirectional microphones in a linear array which are d distance apart.
1. There are 2 linear microphone arrays which are &Delta; distance apart.
1. All microphones are at a common fixed distance away from each other.
1. The position of the source of sound is unknown in a 2D plane.
1. There is only a single source of sound.
1. The souce of sound is to left of the normal to microphone array (minor change in code will fix this).
1. The source of sound is a point source.
1. The source of sound is sufficiently far away from the microphone array.
1. The source of sound is in a fixed position with respect to all the microphones.
1. The source of sound produces some sound for a very breif amount of time (max 0.2 seconds).
1. The source of sound is stationary.
1. There is minimal noise (max 0.5 units).
1. There is no echo.
1. There is minimal distortion.
1. The sound medium is dry air at 20 <sup>o</sup>C.
1. Microphones are of good quality.


# Formulas
![\Large speed=\frac{distance}{time}](https://latex.codecogs.com/svg.latex?\Large&space;speed=\frac{distance}{time})

![\Large sin(\theta)=\frac{opposite-side}{hypotenus}](https://latex.codecogs.com/svg.latex?\Large&space;sin(\theta)=\frac{opposite-side}{hypotenus})

![\Large similarity(A,B)=\frac{A.B}{||A||*||B||}](https://latex.codecogs.com/svg.latex?\Large&space;similarity(A,B)=\frac{A.B}{||A||*||B||})

![\Large \delta_{i}^{j}=S*delay_{i}](https://latex.codecogs.com/svg.latex?\Large&space;\delta_{i}^{j}=S*delay_{i})

![\Large \theta_{j}^{i}=sin^{-1}(\frac{\delta^{j}_{i}}{d})](https://latex.codecogs.com/svg.latex?\Large&space;\theta_{j}^{i}=sin^{-1}(\frac{\delta^{j}_{i}}{d}))

![\Large \theta_{j}=\frac{1}{n}*\sum_{i=1}^{n}\theta_{j}^{i+1}](https://latex.codecogs.com/svg.latex?\Large&space;\theta_{j}=\frac{1}{n}*\sum_{i=1}^{n}\theta_{j}^{i+1})

![\Large p_{x}=\frac{2d+\Delta}{tan(\theta_{2})-tan(\theta_{1})}](https://latex.codecogs.com/svg.latex?\Large&space;p_{x}=\frac{2d+\Delta}{tan(\theta_{2})-tan(\theta_{1})})

![\Large p_{y}=tan(\theta_{2})*p_{x}](https://latex.codecogs.com/svg.latex?\Large&space;p_{y}=tan(\theta_{2})*p_{x})


# Units
| Metrics | Units |
|---------|-------|
| Distance | meters |
| Sampling | samples/seconds |
| Time | seconds |
| Angle | degrees |
| Speed | meters/second |
| Temperature | Celsius |


# Parameter List
| Parameter | Value | Descripttion |
|-----------|-------|--------------|
| Number of microphones (n+1)| 3 | Represents the number of microphones in the microphone array. |
| Number of microphone arrays | 2 | Represents the number of microphone arrays being used. |
| Reference Pulse | NA | The first sound pulse received by any microphone. |
| Resultant Pulse | NA | The final amplified sound pulse. |
| D | Unknown | Longitudinal distance of the source of sound from the microphone array. |
| &theta;<sub>j</sub> | Unknown | Angle made by the source of sound from the normal to the j<sup>th</sup> microphone array. |
| d | 0.1 meters | Distance between each microphone. |
| &delta; | Variable | Distance of the incident wavefront from the previous/subsequent incident microphone. | 
| &Delta; | 0.5 meters | Distance between the microphone arrays. |
| delay<sub>i</sub> | Variable | Delay in time for sound wavefront to reach the i<sup>th</sup> microphone. |
| m<sub>i</sub><sup>j</sup> | NA | i<sup>th</sup> microphone of j<sup>th</sup> microphone array. |
| p<sub>x</sub> | Unknown | x-coordinate of the source of sound in meters with respect to microphone 2. |
| p<sub>y</sub> | Unknown | y-coordinate of the source of sound in meters with respect to microphone 2. |
| S | 343 meters/second | Speed of sound in dry air at 20 <sup>o</sup>C.
| delay | Variable | Time taken by the incident wavefront to reach the previous/subsequent incident microphone. |
| Sampling Rate | 44100 samples/second | The number of samples taken from a continuous signal to make a digital signal. |
| Scanning Window | 0.2 seconds | The duration of signal considered for finding the source. |
| Shift | Variable | Represents the shift of signal in time from source to the closest microphone. |
| Offset | Variable | Represents the shift of signal in time from microphone to microphone (depends on d and &theta;). |
| Step | 1 | Represents the increments of shift in time for a signal. |


# Caution
* Verify the right value of d.
* Verify the right value of &Delta;.