import numpy as np
import App.Config.config as cfg

class CalculateDelta:

    def calculate_deltas(self) -> np.ndarray:
        return np.sin(np.radians(cfg.actual_thetas)) * cfg.d

    def calculate_delays(self) -> np.ndarray:
        return self.calculate_deltas() / cfg.S
        