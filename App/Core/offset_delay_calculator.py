import numpy as np

class OffsetDelay:

    def __init__(self, received_actual_delays: np.ndarray) -> None:
        self.actual_delays = received_actual_delays

    def calculate_offset_delay(self, sample_rate: int) -> np.ndarray:
        return np.round(self.actual_delays * sample_rate).astype(int)
