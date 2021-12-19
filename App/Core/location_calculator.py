import numpy as np
import App.Config.config as cfg

class Location:
        
    def calculate_location(self, thetas: np.ndarray) -> list:
        theta_1, theta_2 = thetas
        p_x = (2 * cfg.d + cfg.Delta) / (np.tan(np.radians(theta_2)) - np.tan(np.radians(theta_1)))
        p_y = np.tan(np.radians(theta_2)) * p_x
        return [p_x, p_y]

    def calculate_actual_location(self) -> list:
        return self.calculate_location(np.asarray(cfg.actual_thetas))
