import numpy as np
import App.Config.config as cfg

class CalculateDelta:

    def __init__(self, received_thetas: list) -> None:
        self.thetas = received_thetas

    def calculate_deltas(self) -> np.ndarray:
        return np.sin(np.radians(self.thetas)) * cfg.d

    def calculate_delays(self) -> np.ndarray:
        return self.calculate_deltas() / cfg.S
        