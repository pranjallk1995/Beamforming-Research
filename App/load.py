import os
import logging
import numpy as np

from scipy.io import wavfile

class LoadSound:

    def __init__(self, received_path: str) -> None:
        self.sound_path = received_path
        self.sound_array = None
        self.sample_rate = None
        self.number_of_sample_points = None
        self.number_of_channels = None
        self.sound_length = None

    def get_sound(self) -> bool:
        try:
            os.path.isfile(self.sound_path)
            return True
        except:
            logging.error("Sound not found.")
            return False

    def get_length(self, sound_length: int, sample_rate: int) -> float:
        length = sound_length / sample_rate
        return round(length, 2)

    def get_left_channel(self):
        return self.sound_array[:, 0]
    
    def load_sound(self) -> None:
        if self.get_sound():
            self.sample_rate, self.sound_array = wavfile.read(self.sound_path)
            self.sound_length = self.get_length(self.sound_array.shape[0], self.sample_rate)
            logging.info("Sampling rate: {} samples/seconds".format(self.sample_rate))
            logging.info("Number of sample points: {}".format(self.sound_array.shape[0]))
            logging.info("Number of channels: {}".format(self.sound_array.shape[1]))
            logging.info("Length of sound: {} seconds".format(self.sound_length))
            self.number_of_sample_points = self.sound_array.shape[0]
            self.number_of_channels = self.sound_array.shape[1]
