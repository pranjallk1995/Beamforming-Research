import os
import warnings
import numpy as np
import App.Config.config as cfg

from tqdm import tqdm
from App.shifting import Shift
from App.Core.theta_calculator import Theta
from App.Core.location_calculator import Location
from App.Core.beam_delay_calculator import BeamForming

class CalculateError:

    def __init__(self):
        self.X = list()
        self.Y = list()
        self.errors = list()
        self.actual_locations = list()
        self.calculated_locations = list()

    def calculate_errors(self, sound_array: np.ndarray, sample_rate: int) -> None:
        warnings.filterwarnings("ignore")
        thetas = np.arange(start = -90, stop = 90, step = cfg.step)
        print("\nCalculating Errors:\n")
        for theta_x in tqdm(thetas, position = 0, bar_format = "{l_bar}{bar: 50}{r_bar}"):
            for theta_y in tqdm(thetas, position = 1, leave = False, bar_format = "{l_bar}{bar: 50}{r_bar}"):
                try:
                    sounds = Shift().perform_shifting(sound_array, sample_rate, [theta_x, theta_y])
                    beam = BeamForming()
                    results = beam.calculate_offsets(sounds, sample_rate)
                    beam.calculate_delays(sample_rate)
                    calculated_thetas = Theta().calculate_thetas(beam.calculated_delays)
                    location = Location([theta_x, theta_y])
                    actual_location = location.calculate_actual_location()
                    calculated_location = location.calculate_location(calculated_thetas)
                    self.X.append(theta_x)
                    self.Y.append(theta_y)
                    self.errors.append(
                        np.sqrt(
                            np.square(actual_location[0] - calculated_location[0]) + \
                            np.square(actual_location[1] - calculated_location[1])
                        )
                    )
                    self.actual_locations.append(actual_location)
                    self.calculated_locations.append(calculated_location)
                except:
                    pass
        print("\nDone!")
        with open(os.path.join(cfg.output_numpy_path, "Error_values.npy"), "wb") as file:
            np.save(file, np.array(self.X))
            np.save(file, np.array(self.Y))
            np.save(file, np.array(self.errors))
            np.save(file, np.array(self.actual_locations))
            np.save(file, np.array(self.calculated_locations))
