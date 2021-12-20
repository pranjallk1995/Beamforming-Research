import numpy as np
import App.Config.config as cfg

class Location:

    def __init__(self, received_thetas: list) -> None:
        self.thetas = received_thetas
        
    def calculate_location(self, thetas: list) -> list:
        theta_1, theta_2 = thetas
        p_x = (2 * cfg.d + cfg.Delta) / (np.tan(np.radians(theta_2)) - np.tan(np.radians(theta_1)))
        p_y = np.tan(np.radians(theta_2)) * p_x
        return [p_x, p_y]

    def calculate_actual_location(self) -> list:
        return self.calculate_location(self.thetas)
