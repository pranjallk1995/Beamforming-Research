import os
import logging
import App.Config.config as cfg

from App.load import LoadSound
from App.exporter import Export
from App.shifting import Shift
from App.Core.theta_calculator import Theta
from App.Core.location_calculator import Location
from App.Core.delay_calculator import BeamForming
from App.Interface.visualizations import Visualize

def load_sound() -> object:
    sound = LoadSound(cfg.sound_path)
    try:
        sound.load_sound()
        visualize = Visualize(sound.sound_length, sound.number_of_sample_points)
    except:
        logging.error("Could not load the sound")
    return visualize, sound

def receive_sound(visualize: object, sound: object) -> dict:
    try:
        received_sounds = Shift().perform_shifting(sound.get_left_channel(), sound.sample_rate)
    except:
        logging.error("Could not perform shifting")
    return received_sounds

def beam_forming(received_sounds: dict, visualize: object, sound: object):
    beam = BeamForming()
    try:
        resultant_sounds = beam.calculate_offsets(received_sounds, sound.sample_rate)
        beam.calculate_delays(sound.sample_rate)
    except:
        logging.error("Could not perform Beamforming")
    try:
        visualize.visualize_offsets(beam.actual_offsets, beam.calculated_offsets)
    except:
        logging.error("Could not write offset values")
    try:
        visualize.visualize_delays(beam.actual_delays, beam.calculated_delays)
    except:
        logging.error("Could not write delay values")
    try:
        Export().export(resultant_sounds, sound.number_of_channels, sound.sample_rate)
    except:
        logging.error("Could not export resultant sounds")
    return beam, resultant_sounds

def find_sound_source(visualize: object, beam: object) -> list:
    theta = Theta()
    try:
        calculated_thetas = theta.calculate_thetas(beam.calculated_delays)
    except:
        logging.error("Could not calculate thetas")
    try:
        visualize.visualize_thetas(calculated_thetas)
    except:
        logging.error("Could not write theta values")
    try:
        actual_location = Location().calculate_actual_location()
        calculated_location = Location().calculate_location(calculated_thetas)
    except:
        logging.error("Could not calculate location of the source of sound")
    try:
        visualize.visualize_location(actual_location, calculated_location)
    except:
        logging.error("Could not visualize source sound's location")
    return calculated_location

def visualize_diagrams(visualize: object, sound: object, received_sounds: dict, resultant_sounds: list) -> None:
    # try:
    visualize.visualize_dash(
        sound.sound_array,
        sound.number_of_channels,
        received_sounds,
        sound.sample_rate,
        resultant_sounds
    )
    # except:
    #     logging.error("Could not visualize Dash")

def main():
    viz, sound = load_sound()
    received_sounds = receive_sound(viz, sound)
    beam, resultant_sounds = beam_forming(received_sounds, viz, sound)
    source_location = find_sound_source(viz, beam)
    visualize_diagrams(viz, sound, received_sounds, resultant_sounds)
    logging.info(
        "Source location of x = {} and y = {} with respect to the 2nd microphone array was successfully calculated"\
        .format(round(source_location[0], 2), round(source_location[1], 2))
    )

if __name__ == "__main__":
    log_path = os.path.join(os.getcwd(), "Logs", "App_logs.log")
    if os.path.isfile(log_path):
        os.remove(log_path)
    logging.basicConfig(filename = "Logs/App_logs.log", level = logging.INFO)
    main()
