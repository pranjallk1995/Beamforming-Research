import numpy as np
import App.Config.config as cfg

from App.Core.delta_calculator import CalculateDelta
from App.Core.offset_delay_calculator import OffsetDelay
from App.Core.scannig_window_offset_calculator import ScanningWindow

class Shift:

    def __init__(self) -> None:
        self.offsets = np.zeros(cfg.number_of_microphone_arrays).astype(int)

    def trim(self, received_array: np.ndarray, sample_rate: int) -> np.ndarray:
        scanning_window_max_offset = ScanningWindow().calculate_offset(sample_rate)
        return received_array[:scanning_window_max_offset]

    def perform_shifting(self, received_sound_pulse: np.ndarray, sample_rate: int) -> dict:
        pulses = {array: [] for array in range(cfg.number_of_microphone_arrays)}
        actual_delays = CalculateDelta().calculate_delays()
        offset_delay = OffsetDelay(actual_delays).calculate_offset_delay(sample_rate) 
        for array in range(cfg.number_of_microphone_arrays):
            for _ in range(cfg.number_of_microphones):
                pulses[array].append(
                    [
                        self.trim(np.roll(received_sound_pulse, self.offsets[array]), sample_rate), 
                        self.offsets[array]
                    ]
                )
                self.offsets[array] += offset_delay[array]
        return pulses
