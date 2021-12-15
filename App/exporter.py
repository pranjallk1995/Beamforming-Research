import os
import logging
import numpy as np
import App.Config.config as cfg

from scipy.io import wavfile

class Export:

    def export(self, resultant_sounds: np.ndarray, number_of_channels: int, sample_rate: int) -> None:
        for array in range(cfg.number_of_microphone_arrays):
            wavfile.write(
                os.path.join(
                    cfg.output_sound_path,
                    "Resultant_from_microphone_{}.wav".format(array + 1)
                ),
                sample_rate, 
                np.repeat(resultant_sounds[array][:, np.newaxis], number_of_channels, axis = 1)
            )
        logging.info("Resultant sounds exported successfully")
