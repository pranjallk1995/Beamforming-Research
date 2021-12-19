import os
import logging
import numpy as np
import prettytable as pt

import App.Config.config as cfg

from datetime import date
from App.Interface.dash_visualization import VisualizeDash

class Visualize:

    def __init__(self, sound_length: float, number_of_sample_points: int) -> None:
        self.X = np.linspace(start = 0, stop = sound_length, num = number_of_sample_points)

    def visualize_dash(
        self, 
        sound_array: np.ndarray, 
        number_of_channels: int,
        received_sounds: dict,
        sample_rate: int,
        resultant_sounds: list
        ) -> None:
        VisualizeDash().run(self.X, sound_array, number_of_channels, received_sounds, sample_rate, resultant_sounds)
        logging.info("Visualizations in Dash successful")

    def visualize_offsets(self, actual_offsets: list, calculated_offsets: list) -> None:
        table_offsets = [pt.PrettyTable() for _ in range(cfg.number_of_microphone_arrays)]
        file_path = os.path.join(cfg.output_export_path, "Offsets.txt")
        with open(file_path, "w") as file:
            file.write(str(date.today()))
        for array in range(cfg.number_of_microphone_arrays):
            with open(file_path, "a") as file:
                file.write("\n\n################# Microphone {} ######################\n".format(array + 1))
            table_offsets[array].field_names = ["Sound Pulse", "Actual Offests", "Calculated Offsets"]
            for number in range(cfg.number_of_microphones):
                table_offsets[array].add_row(
                    [
                        "Pulse " + str(number + 1),
                        actual_offsets[array][number],
                        calculated_offsets[array][number]
                    ]
                )
            with open(file_path, "a") as file:
                file.write(str(table_offsets[array]))
        logging.info("Text file for Offsets created in Exports folder")

    def visualize_delays(self, actual_delays: list, calculated_delays: list) -> None:
        table_delays = [pt.PrettyTable() for _ in range(cfg.number_of_microphone_arrays)]
        file_path = os.path.join(cfg.output_export_path, "Delays.txt")
        with open(file_path, "w") as file:
            file.write(str(date.today()))
        for array in range(cfg.number_of_microphone_arrays):
            with open(file_path, "a") as file:
                file.write("\n\n################# Microphone {} ######################\n".format(array + 1))
            table_delays[array].field_names = ["Sound Pulse", "Actual Delays", "Calculated Delays"]
            for index, delay in enumerate(calculated_delays[array]):
                table_delays[array].add_row(
                    [
                        "Pulse " + str(index + 1),
                        str(round(actual_delays[array][index], 5)) + " seconds",
                        str(round(delay, 5)) + " seconds"
                    ]
                )
            with open(file_path, "a") as file:
                file.write(str(table_delays[array]))
        logging.info("Text file for Delays created in Exports folder")
    
    def visualize_thetas(self, calculated_thetas: np.ndarray):
        table_thetas = pt.PrettyTable()
        file_path = os.path.join(cfg.output_export_path, "Thetas.txt")
        with open(file_path, "w") as file:
            file.write(str(date.today()) + "\n\n")
        table_thetas.field_names = ["Angle", "Actual", "Calculated", "Error"]
        for array in range(cfg.number_of_microphone_arrays):
            table_thetas.add_row(
                [
                    "Theta " + str(array + 1),
                    str(cfg.actual_thetas[array]) + " degrees", 
                    str(round(calculated_thetas[array], 2)) + " degrees",
                    str(round(abs(cfg.actual_thetas[array] - calculated_thetas[array]), 2)) + " degrees"
                ]
            )
        with open(file_path, "a") as file:
            file.write(str(table_thetas))
        logging.info("Text file for Thetas created in Exports folder")

    def visualize_location(self, actual_location: list, calculated_location: list):
        table_location = pt.PrettyTable()
        file_path = os.path.join(cfg.output_export_path, "Location.txt")
        with open(file_path, "w") as file:
            file.write(str(date.today()) + "\n\n")
        table_location.field_names = ["Actual Location", "Calculated Location", "Error"]
        dimension_x, dimension_y = cfg.coordinate_system
        table_location.add_row(
            [
                "(" + str(round(actual_location[dimension_x], 2)) + "," + str(round(actual_location[dimension_y], 2)) + ")", 
                "(" + str(round(calculated_location[dimension_x], 2)) + "," + str(round(calculated_location[dimension_y], 2)) + ")",
                str(
                    round(
                        np.sqrt(
                            np.square(actual_location[dimension_x] - calculated_location[dimension_x]) + \
                            np.square(actual_location[dimension_y] - calculated_location[dimension_y])
                        ), 
                    2)
                ) + " meters"
            ]
        )
        with open(file_path, "a") as file:
            file.write(str(table_location))
        logging.info("Text file for Locations created in Exports folder")
