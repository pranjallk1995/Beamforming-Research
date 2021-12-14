import os
import logging
import numpy as np
import prettytable as pt
import plotly.graph_objs as go
import App.Config.config as cfg

from datetime import date
from plotly import subplots
from App.shifting import Shift

class Visualize:

    def __init__(self, sound_length: float, number_of_sample_points: int) -> None:
        self.X = np.linspace(start = 0, stop = sound_length, num = number_of_sample_points)

    def visualize_sound(self, sound_array: np.ndarray, number_of_channels: int) -> None:
        trace = list()
        name = ["Left Channel", "Right Channel"]
        colors = ["darkred", "lightblue"]
        for channel in range(number_of_channels):
            trace.append(
                go.Scatter(
                    x = self.X,
                    y = sound_array[:, channel],
                    name = name[channel],
                    legendgroup = channel,
                    marker = dict(
                        color = colors[channel]
                    ),
                    mode = "lines"
                )
            )
        fig_sound = subplots.make_subplots(
            rows = number_of_channels, cols = 1, 
            shared_xaxes = True, 
            vertical_spacing = 0.1
        )
        for channel in range(number_of_channels):
            fig_sound.add_trace(trace[channel], row = channel + 1, col = 1)
            fig_sound.update_yaxes(title_text = "Amplitude", row = channel, col = 1)
        fig_sound.update_xaxes(title_text = "Time", row = number_of_channels, col = 1)
        fig_sound.update_layout(
            title = "Sound Pulse",
            template = "plotly_dark"
        )
        fig_sound.show()
        logging.info("Visualiziation for original sound successful")

    def visualize_received_sound(self, received_sounds: np.ndarray, number_of_microphone_arrays: int, number_of_microphones: int, sample_rate: int) -> None:
        traces = list()
        titles = list()
        rows = number_of_microphones
        columns = number_of_microphone_arrays
        X = Shift().trim(self.X, sample_rate)
        for array in range(number_of_microphone_arrays):
            for number in range(number_of_microphones):
                traces.append(
                    go.Scatter(
                        x = X,
                        y = received_sounds[array][number][0],
                        mode = "lines"
                    )
                )
        for number in range(number_of_microphones):
            for array in range(number_of_microphone_arrays):
                titles.append("Microphone array " + str(array + 1) + ": Pulse " + str(number + 1))
        fig_received_sounds = subplots.make_subplots(
            rows = rows, cols = columns, 
            shared_xaxes = True,
            shared_yaxes = True,
            horizontal_spacing = 0.1,
            vertical_spacing = 0.2,
            subplot_titles = titles
        )
        for index, trace in enumerate(traces):
            fig_received_sounds.add_trace(trace, row = (index % 3) + 1, col = (index // 3) + 1)
        for value in range(rows):
            fig_received_sounds.update_yaxes(title_text = "Amplitude", row = value + 1, col = 1)
        for value in range(columns):
            fig_received_sounds.update_xaxes(title_text = "Time", row = 3, col = value + 1)
        fig_received_sounds.update_layout(
                colorway = [
                        "floralwhite", 
                        "plum", 
                        "coral"
            ],
            showlegend = False,
            title = "Sound Pulses",
            template = "plotly_dark",
            height = 700
        )
        fig_received_sounds.show()
        logging.info("Visualization for received sounds on all microphones successful")

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
    
    def visualize_resultant_sounds(self, resultant_sounds: list, sample_rate: int) -> None:
        trace = list()
        colors = ["orange", "purple"]
        X = Shift().trim(self.X, sample_rate)
        for array in range(cfg.number_of_microphone_arrays):
            trace.append(
                go.Scatter(
                    x = X,
                    y = resultant_sounds[array],
                    marker = dict(
                        color = colors[array]
                    ),
                    mode = "lines"
                )
            )
        titles = list()
        for array in range(cfg.number_of_microphone_arrays):
            titles.append("Microphone " + str(array + 1))
        fig_resultant = subplots.make_subplots(
            rows = cfg.number_of_microphone_arrays, cols = 1, 
            shared_xaxes = True,
            vertical_spacing = 0.2,
            subplot_titles = titles
        )
        for array in range(cfg.number_of_microphone_arrays):
            fig_resultant.add_trace(trace[array], row = array + 1, col = 1)
            fig_resultant.update_yaxes(title_text = "Amplitude", row = array + 1, col = 1)
        fig_resultant.update_xaxes(title_text = "Time", row = array + 1, col = 1)
        fig_resultant.update_layout(
            title = "Resultant Pulses",
            showlegend = False,
            template = "plotly_dark"
        )
        fig_resultant.show()
        logging.info("Visualization for resultant sounds from microphone arrays successful")
    
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