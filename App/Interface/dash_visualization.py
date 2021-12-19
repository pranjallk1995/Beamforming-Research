import dash
import numpy as np
import plotly.graph_objs as go
import App.Config.config as cfg

from dash import dcc
from dash import html
from plotly import subplots
from App.shifting import Shift

class VisualizeDash:
    def visualize_source_sound(self, X: np.ndarray, sound_array: np.ndarray, number_of_channels: int) -> go.Figure:
        trace = list()
        name = ["Left Channel", "Right Channel"]
        colors = ["darkred", "lightblue"]
        for channel in range(number_of_channels):
            trace.append(
                go.Scatter(
                    x = X,
                    y = sound_array[:, channel],
                    name = name[channel],
                    legendgroup = channel,
                    marker = dict(
                        color = colors[channel]
                    ),
                    mode = "lines"
                )
            )
        fig_source_sound = subplots.make_subplots(
            rows = number_of_channels, cols = 1, 
            shared_xaxes = True, 
            vertical_spacing = 0.1
        )
        for channel in range(number_of_channels):
            fig_source_sound.add_trace(trace[channel], row = channel + 1, col = 1)
            fig_source_sound.update_yaxes(title_text = "Amplitude", row = channel, col = 1)
        fig_source_sound.update_xaxes(title_text = "Time", row = number_of_channels, col = 1)
        fig_source_sound.update_layout(
            title = "Original Sound",
            template = "plotly_dark"
        )
        return fig_source_sound

    def visualize_received_sound(self, X: np.ndarray, received_sounds: np.ndarray, sample_rate: int) -> go.Figure:
        traces = list()
        titles = list()
        rows = cfg.number_of_microphones
        columns = cfg.number_of_microphone_arrays
        X = Shift().trim(X, sample_rate)
        for array in range(cfg.number_of_microphone_arrays):
            for number in range(cfg.number_of_microphones):
                traces.append(
                    go.Scatter(
                        x = X,
                        y = received_sounds[array][number][0],
                        mode = "lines"
                    )
                )
        for number in range(cfg.number_of_microphones):
            for array in range(cfg.number_of_microphone_arrays):
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
            title = "Received Sounds",
            template = "plotly_dark",
            height = 700
        )
        return fig_received_sounds

    def visualize_resultant_sounds(self, X: np.ndarray, resultant_sounds: list, sample_rate: int) -> go.Figure:
        trace = list()
        colors = ["orange", "purple"]
        X = Shift().trim(X, sample_rate)
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
            titles.append("Microphone array " + str(array + 1))
        fig_resultant_sounds = subplots.make_subplots(
            rows = cfg.number_of_microphone_arrays, cols = 1, 
            shared_xaxes = True,
            vertical_spacing = 0.2,
            subplot_titles = titles
        )
        for array in range(cfg.number_of_microphone_arrays):
            fig_resultant_sounds.add_trace(trace[array], row = array + 1, col = 1)
            fig_resultant_sounds.update_yaxes(title_text = "Amplitude", row = array + 1, col = 1)
        fig_resultant_sounds.update_xaxes(title_text = "Time", row = array + 1, col = 1)
        fig_resultant_sounds.update_layout(
            title = "Resultant Sounds",
            showlegend = False,
            template = "plotly_dark"
        )
        return fig_resultant_sounds

    def run(
        self, 
        X: np.ndarray, 
        sound_array: np.ndarray, 
        number_of_channels: int, 
        received_sounds: dict, 
        sample_rate: int, 
        resultant_sounds: list
        ) -> None:
        app = dash.Dash(__name__)
        fig_original_sound = self.visualize_source_sound(X, sound_array,  number_of_channels)
        fig_received_sounds = self.visualize_received_sound(X, received_sounds, sample_rate)
        fig_resultant_sounds = self.visualize_resultant_sounds(X, resultant_sounds, sample_rate)
        app.layout = html.Div(
            style = {"backgroundColor": "black"}, 
            children = [
                html.H1(
                    children = "Visualizations",
                    style = {
                        "textAlign": "center",
                        "color": "white"
                    }
                ),
                dcc.Graph(
                    id = "Sound source",
                    figure = fig_original_sound
                ),
                dcc.Graph(
                    id = "Received sound",
                    figure = fig_received_sounds
                ),
                dcc.Graph(
                    id = "Resultant sound",
                    figure = fig_resultant_sounds
                )
            ]
        )
        app.run_server(debug=True)