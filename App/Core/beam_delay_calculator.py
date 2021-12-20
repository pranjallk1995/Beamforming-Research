import time
import logging
import numpy as np
import prettytable as pt
import App.Config.config as cfg

from App.Core.scannig_window_offset_calculator import ScanningWindow

class BeamForming:

    def __init__(self) -> None:
        self.actual_offsets = [list() for _ in range(cfg.number_of_microphone_arrays)]
        self.calculated_offsets = [list() for _ in range(cfg.number_of_microphone_arrays)]
        self.actual_delays = [list() for _ in range(cfg.number_of_microphone_arrays)]
        self.calculated_delays = [list() for _ in range(cfg.number_of_microphone_arrays)]

    def calculate_delays(self, sample_rate: int) -> None:
        for array in range(cfg.number_of_microphone_arrays):
            for actual_offset, calculated_offset in zip(self.actual_offsets[array], self.calculated_offsets[array]):
                self.actual_delays[array].append(
                    actual_offset / sample_rate
                )
                self.calculated_delays[array].append(
                    calculated_offset / sample_rate
                )

    def normalize(self, sound: np.ndarray) -> np.ndarray:
        return sound/np.linalg.norm(sound)

    def find_similarity_score(self, reference_sound: np.ndarray, secondary_sound: np.ndarray) -> float:
        reference_sound_norm = np.linalg.norm(reference_sound)
        secondary_sound_norm = np.linalg.norm(secondary_sound)
        return np.dot(reference_sound, secondary_sound)/ (reference_sound_norm * secondary_sound_norm)

    def find_offset(self, reference_sound: np.ndarray, secondary_sound: np.ndarray, possible_offsets: list) -> float:
        similarity_scores = dict()
        normalized_reference_sound = self.normalize(reference_sound)
        normalized_secondary_sound = self.normalize(secondary_sound)
        for offset in possible_offsets:
            similarity_scores[offset] = self.find_similarity_score(
                np.roll(normalized_reference_sound, offset),
                normalized_secondary_sound
            )
        return max(similarity_scores, key = similarity_scores.get)

    def sum_sounds(self, reference_sound: np.ndarray, secondary_sound: np.ndarray, offset: int) -> np.ndarray:
        return np.add(reference_sound, np.roll(secondary_sound, -offset))

    def calculate_offsets(self, received_sounds: dict, sample_rate: int, caller: str = None) -> list: 
        reference_sound = None
        scanning_window_max_offset = ScanningWindow().calculate_offset(sample_rate)
        resultant_sounds = [np.zeros(scanning_window_max_offset) for _ in range(cfg.number_of_microphone_arrays)]
        possible_offsets = np.arange(start = 0, stop = scanning_window_max_offset, step = cfg.step)
        start = time.time()
        for array in range(cfg.number_of_microphone_arrays):
            for number in range(cfg.number_of_microphones):
                if not len(self.calculated_offsets[array]):
                    reference_sound = received_sounds[array][number][0]
                    self.calculated_offsets[array].append(0)
                    self.actual_offsets[array].append(0)
                else:
                    secondary_sound = received_sounds[array][number][0]
                    self.actual_offsets[array].append(received_sounds[array][number][1])
                    self.calculated_offsets[array].append(
                        self.find_offset(
                            reference_sound, 
                            secondary_sound, 
                            possible_offsets
                        )
                    )
                    resultant_sounds[array] = np.add(
                        resultant_sounds[array],
                        self.sum_sounds(
                            reference_sound, 
                            secondary_sound, 
                            self.calculated_offsets[array][number]
                        )
                    )
        if caller == "main":
            logging.info("Beamforming successful in {} seconds".format(round(time.time() - start, 2)))
        return resultant_sounds