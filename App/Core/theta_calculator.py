import logging
import numpy as np
import App.Config.config as cfg

class Theta:

    def find_mean_delay(self, calculated_delays: list) -> float:
        return np.mean(np.diff(np.asarray(calculated_delays)))

    def calculate_thetas(self, calculated_delays: list) -> np.ndarray:
        mean_delay = list()
        for array in range(cfg.number_of_microphone_arrays):
            mean_delay.append(self.find_mean_delay(calculated_delays[array]))
        calculated_deltas = cfg.S * np.asarray(mean_delay)
        calculated_thetas = np.degrees(np.arcsin(calculated_deltas / cfg.d))
        logging.info(
            "Theta values of {} and {} calculated successfully".format(
                round(calculated_thetas[0], 2), 
                round(calculated_thetas[1], 2)
            )
        )
        return calculated_thetas