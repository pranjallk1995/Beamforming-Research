import numpy as np
import App.Config.config as cfg

class ScanningWindow:

    def calculate_offset(self, sample_rate: int) -> int:
        return np.floor(cfg.scanning_window * sample_rate).astype(int)
