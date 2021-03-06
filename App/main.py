import os
import logging
import App.Config.config as cfg

from App.load import LoadSound
from App.exporter import Export
from App.shifting import Shift
from App.Core.theta_calculator import Theta
from App.Core.location_calculator import Location
from App.Interface.visualizations import Visualize
from App.Core.error_calculator import CalculateError
from App.Core.beam_delay_calculator import BeamForming

def load_sound() -> object:
    sound = LoadSound(cfg.sound_path)
    try:
        sound.load_sound()
        visualize = Visualize(sound.sound_length, sound.number_of_sample_points)
    except:
        logging.error("Could not load the sound")
    return [visualize, sound]

def receive_sound(visualize: object, sound: object) -> dict:
    try:
        received_sounds = Shift().perform_shifting(sound.get_left_channel(), sound.sample_rate, cfg.actual_thetas)
    except:
        logging.error("Could not perform shifting")
    return received_sounds

def beam_forming(received_sounds: dict, visualize: object, sound: object):
    beam = BeamForming()
    try:
        resultant_sounds = beam.calculate_offsets(received_sounds, sound.sample_rate, "main")
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
    return [beam, resultant_sounds]

def find_sound_source(visualize: object, beam: object) -> list:
    try:
        calculated_thetas = Theta().calculate_thetas(beam.calculated_delays)
    except:
        logging.error("Could not calculate thetas")
    try:
        visualize.visualize_thetas(calculated_thetas)
    except:
        logging.error("Could not write theta values")
    try:
        location = Location(cfg.actual_thetas)
        actual_location = location.calculate_actual_location()
        calculated_location = location.calculate_location(calculated_thetas)
    except:
        logging.error("Could not calculate location of the source of sound")
    try:
        visualize.visualize_location(actual_location, calculated_location)
    except:
        logging.error("Could not visualize source sound's location")
    return [actual_location, calculated_location]

def visualize_diagrams(
    visualize: object, sound: object, 
    received_sounds: dict, resultant_sounds: list, 
    actual_location: list, calculated_location: list
    ) -> None:
    try:
        visualize.visualize_dash(
            sound.sound_array,
            sound.number_of_channels,
            received_sounds,
            sound.sample_rate,
            resultant_sounds,
            actual_location,
            calculated_location
        )
    except:
        logging.error("Could not visualize Dash")

def main():
    viz, sound = load_sound()
    received_sounds = receive_sound(viz, sound)
    beam, resultant_sounds = beam_forming(received_sounds, viz, sound)
    actual_location, calculated_location = find_sound_source(viz, beam)
    logging.info(
        "Source location of x = {} and y = {} with respect to the 2nd microphone array was successfully calculated"\
        .format(round(calculated_location[0], 2), round(calculated_location[1], 2))
    )
    if cfg.calculate_errors:
        CalculateError().calculate_errors(sound.sound_array[:, 0], sound.sample_rate)
    if not cfg.suppress_plots:
        visualize_diagrams(viz, sound, received_sounds, resultant_sounds, actual_location, calculated_location)

if __name__ == "__main__":
    logging_path = os.path.join(os.getcwd(), "Logs", "App_logs.log")
    if os.path.isfile(logging_path):
        os.remove(logging_path)
    logging.basicConfig(filename = "Logs/App_logs.log", level = logging.INFO)
    main()
