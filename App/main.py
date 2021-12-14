import os
import logging
import numpy as np
import App.Config.config as cfg

from App.load import LoadSound
from App.exporter import Export
from App.shifting import Shift
from App.Core.theta_calculator import Theta
from App.Core.delay_calculator import BeamForming
from App.Interface.visualizations import Visualize

def load_sound() -> object:
    sound = LoadSound(cfg.sound_path)
    try:
        sound.load_sound()
    except:
        logging.error("Could not load the sound")
    try:
        vizualize = Visualize(sound.sound_length, sound.number_of_sample_points)
        vizualize.visualize_sound(sound.sound_array, sound.number_of_channels)
    except:
        logging.error("Could not visualize the sound")
    return vizualize, sound

def receive_sound(vizualize: object, sound: object) -> dict:
    try:
        received_sounds = Shift().perform_shifting(sound.get_left_channel(), sound.sample_rate)
    except:
        logging.error("Could not perform shifting")
    try:
        vizualize.visualize_received_sound(received_sounds, cfg.number_of_microphone_arrays, cfg.number_of_microphones, sound.sample_rate)
    except:
        logging.error("Could not visualize received sounds")
    return received_sounds

def beam_forming(received_sounds: dict, vizualize: object, sound: object):
    beam = BeamForming()
    try:
        resultant_sounds = beam.calculate_offsets(received_sounds, sound.sample_rate)
        beam.calculate_delays(sound.sample_rate)
    except:
        logging.error("Could not perform Beamforming")
    try:
        vizualize.visualize_offsets(beam.actual_offsets, beam.calculated_offsets)
    except:
        logging.error("Could not write offset values")
    try:
        vizualize.visualize_delays(beam.actual_delays, beam.calculated_delays)
    except:
        logging.error("Could not write delay values")
    try:
        vizualize.visualize_resultant_sounds(resultant_sounds, sound.sample_rate)
    except:
        logging.error("Could not visualize resultant sounds")
    try:
        Export().export(resultant_sounds, sound.number_of_channels, sound.sample_rate)
    except:
        logging.error("Could not export resultant sounds")
    return beam

def find_sound_source(vizualize: object, beam: object) -> list:
    theta = Theta()
    try:
        calculated_thetas = theta.calculate_thetas(beam.calculated_delays)
    except:
        logging.error("Could not calculate thetas")
    try:
        vizualize.visualize_thetas(calculated_thetas)
    except:
        logging.error("Could not write theta values")

def main():
    viz, sound = load_sound()
    received_sounds = receive_sound(viz, sound)
    beam = beam_forming(received_sounds, viz, sound)
    source_location = find_sound_source(viz, beam)

if __name__ == "__main__":
    log_path = os.path.join(os.getcwd(), "Logs", "App_logs.log")
    if os.path.isfile(log_path):
        os.remove(log_path)
    logging.basicConfig(filename = "Logs/App_logs.log", level = logging.INFO)
    main()
    
    
