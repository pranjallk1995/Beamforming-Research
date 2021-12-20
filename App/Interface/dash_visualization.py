import os
import dash
import logging
import numpy as np
import plotly.graph_objs as go
import App.Config.config as cfg

from dash import dcc
from dash import html
from plotly import subplots
from App.shifting import Shift
from dash.dependencies import Input, Output

class VisualizeDash:

    def setup_figure(self, actual_location: list, calculated_location: list) -> go.Figure:
        trace0 = go.Scatter(
            x = np.asarray(actual_location[0]),
            y = np.asarray(actual_location[1]),
            mode = "markers",
            name = "Actual Location",
            legendgroup = "1",
            marker = dict(color = "green")
        )
        trace1 = go.Scatter(
            x = np.asarray(calculated_location[0]),
            y = np.asarray(calculated_location[1]),
            mode = "markers",
            name = "Calculated Location",
            legendgroup = "2",
            marker = dict(color = "red")
        )
        trace2 = go.Scatter(
            x = np.zeros(cfg.number_of_microphones),
            y = np.arange(cfg.d+cfg.Delta, 2*cfg.d+cfg.Delta+1, cfg.d),
            mode = "markers",
            marker = dict(color = "yellow"),
            showlegend = False
        )
        trace3 = go.Scatter(
            x = np.zeros(cfg.number_of_microphones),
            y = np.arange(-cfg.d, cfg.d+1, cfg.d),
            mode = "markers",
            marker = dict(color = "yellow"),
            showlegend = False
        )
        trace4 = go.Scatter(
            x = [-cfg.number_x, cfg.number_x, cfg.number_x, -cfg.number_x, -cfg.number_x],
            y = [cfg.d+cfg.Delta-cfg.number_y, cfg.d+cfg.Delta-cfg.number_y, 3*cfg.d+cfg.Delta+cfg.number_y, 3*cfg.d+cfg.Delta+cfg.number_y, cfg.d+cfg.Delta-cfg.number_y],
            mode = "lines",
            fill = "toself",
            marker = dict(color = "orange"),
            showlegend = False
        )
        trace5 = go.Scatter(
            x = [-cfg.number_x, cfg.number_x, cfg.number_x, -cfg.number_x, -cfg.number_x],
            y = [-cfg.d-cfg.number_y, -cfg.d-cfg.number_y, cfg.d+cfg.number_y, cfg.d+cfg.number_y, -cfg.d-cfg.number_y],
            mode = "lines",
            fill = "toself",
            marker = dict(color = "orange"),
            showlegend = False
        )
        trace6 = go.Scatter(
            x = [0, actual_location[0], 0],
            y = [2*cfg.d+cfg.Delta, actual_location[1], 0],
            mode = "lines",
            line = dict(dash = "dash"),
            marker = dict(color = "rgba(0, 255, 0, 0.5)"),
            showlegend = False
        )
        trace7 = go.Scatter(
            x = [0, calculated_location[0], 0],
            y = [2*cfg.d+cfg.Delta, calculated_location[1], 0],
            mode = "lines",
            line = dict(dash = "dash"),
            marker = dict(color = "rgba(255, 0, 0, 0.5)"),
            showlegend = False
        )
        trace8 = go.Scatter(
            x = [-cfg.normal_x, cfg.normal_x, None, -cfg.normal_x, cfg.normal_x],
            y = [2*cfg.d+cfg.Delta, 2*cfg.d+cfg.Delta, None, 0, 0],
            mode = "lines",
            marker = dict(color = "white"),
            showlegend = False
        )
        data = [trace0, trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8]
        fig = go.Figure(data)
        fig.add_annotation(
            x = 0,
            y = 0.3,
            text = "Microphone Array 2",
            font = dict(color = "white"),
            showarrow = False
        )
        fig.add_annotation(
            x = 0,
            y = 1,
            text = "Microphone Array 1",
            font = dict(color = "white"),
            showarrow = False
        )
        fig.update_layout(
            title = "Experimental Setup",
            xaxis_title = "x-axis", yaxis_title = "y-axis",
            template = "plotly_dark",
            height = 575
        )
        fig.update_xaxes(
            range = (-0.2, 2)
        )
        fig.update_yaxes(
            range = (-0.3, 2)
        )
        return fig

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
            template = "plotly_dark",
            height = 575
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
            height = 575
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
            template = "plotly_dark",
            height = 575
        )
        return fig_resultant_sounds

    def visualize_error(self, X: np.ndarray, Y: np.ndarray, errors: np.ndarray) -> go.Figure:
        trace = go.Scatter3d(
            x = X, y = Y, z = errors, mode = "markers", 
            marker = dict(size = 2, color = errors, colorscale = "OrRd")
        )
        fig_error = go.Figure([trace])
        fig_error.update_layout(
            title = "Error Plot",
            scene = dict(xaxis_title = "Theta 1", yaxis_title = "Theta 2", zaxis_title = "Error"),
            template = "plotly_dark",
            margin = dict(l = 65, r = 50, b = 65, t = 90),
            height = 1000
        )
        return fig_error
    
    def visualize_range(self, actual_locations: np.ndarray) -> go.Figure:
        trace = list()
        for location in actual_locations:
            trace.append(
                go.Scatter(
                    x = [location[0]],
                    y = [location[1]],
                    mode = "markers",
                    marker = dict(size = 2, color = "green"),
                    showlegend = False
                )
            )
        trace.append(
                go.Scatter(
                x = np.zeros(cfg.number_of_microphones),
                y = np.arange(cfg.d+cfg.Delta, 2*cfg.d+cfg.Delta+1, cfg.d),
                mode = "markers",
                marker = dict(color = "yellow"),
                showlegend = False
            )
        )
        trace.append(
            go.Scatter(
                x = np.zeros(cfg.number_of_microphones),
                y = np.arange(-cfg.d, cfg.d+1, cfg.d),
                mode = "markers",
                marker = dict(color = "yellow"),
                showlegend = False
            )
        )
        trace.append(
            go.Scatter(
                x = [-cfg.number_x, cfg.number_x, cfg.number_x, -cfg.number_x, -cfg.number_x],
                y = [cfg.d+cfg.Delta-cfg.number_y, cfg.d+cfg.Delta-cfg.number_y, 3*cfg.d+cfg.Delta+cfg.number_y, 3*cfg.d+cfg.Delta+cfg.number_y, cfg.d+cfg.Delta-cfg.number_y],
                mode = "lines",
                fill = "toself",
                marker = dict(color = "orange"),
                showlegend = False
            )
        )
        trace.append( 
            go.Scatter(
                x = [-cfg.number_x, cfg.number_x, cfg.number_x, -cfg.number_x, -cfg.number_x],
                y = [-cfg.d-cfg.number_y, -cfg.d-cfg.number_y, cfg.d+cfg.number_y, cfg.d+cfg.number_y, -cfg.d-cfg.number_y],
                mode = "lines",
                fill = "toself",
                marker = dict(color = "orange"),
                showlegend = False
            )
        )
        data = trace
        fig_range = go.Figure(data)
        fig_range.add_annotation(
            x = 0,
            y = 0.3,
            text = "Microphone Array 2",
            font = dict(color = "white"),
            showarrow = False
        )
        fig_range.add_annotation(
            x = 0,
            y = 1,
            text = "Microphone Array 1",
            font = dict(color = "white"),
            showarrow = False
        )
        fig_range.update_layout(
            title = "Experimental Setup",
            xaxis_title = "x-axis", yaxis_title = "y-axis",
            template = "plotly_dark",
            height = 575
        )
        fig_range.update_xaxes(
            range = (-0.2, 5)
        )
        fig_range.update_yaxes(
            range = (-0.3, 4)
        )
        return fig_range

    def run(
        self, 
        X: np.ndarray, 
        sound_array: np.ndarray, 
        number_of_channels: int, 
        received_sounds: dict, 
        sample_rate: int, 
        resultant_sounds: list,
        actual_location: list,
        calculated_location: list
        ) -> None:
        app = dash.Dash(__name__)
        colors = {
            "background": "#111111",
            "text": "white"
        }
        app.layout = html.Div(
            style = {"backgroundColor": colors["background"]}, 
            children = [
                html.Br(),
                html.H1(
                    children = "Visualizations",
                    style = {
                        "textAlign": "center",
                        "color": colors["text"]
                    }
                ),
                html.Div(
                    style = {
                        "width": "50%", "align": "center",
                        "margin-left": "auto", "margin-right": "auto"
                    },
                    children = [
                        dcc.Dropdown(
                            id = "selection",
                            options = [
                                {"label": "Experimental Setup", "value": "SET"},
                                {"label": "Original Sound", "value": "ORG"},
                                {"label": "Received Sounds", "value": "RVD"},
                                {"label": "Resultant Sounds", "value": "RST"},
                                {"label": "Error Plot", "value": "ERR"},
                                {"label": "Range Plot", "value": "RNG"}
                            ],
                            value = "SET",
                            style = {"cursor": "pointer"}
                        ),
                        html.Br()
                    ]
                ),
                html.Div(
                    children = [
                        dcc.Loading(id = "loading_plot"),
                        dcc.Graph(id = "selected_plot")
                    ]
                )
            ]
        )
        @app.callback(
            Output(component_id = "loading_plot", component_property = "children"),
            Output(component_id = "selected_plot", component_property = "figure"),
            Input(component_id = "selection", component_property = "value")
        )
        def update_plot(selection_value: str):
            if selection_value == "SET":
                return selection_value, self.setup_figure(actual_location, calculated_location)
            if selection_value == "ORG":
                return selection_value, self.visualize_source_sound(X, sound_array,  number_of_channels)
            if selection_value == "RVD":
                return selection_value, self.visualize_received_sound(X, received_sounds, sample_rate)
            if selection_value == "RST":
                return selection_value, self.visualize_resultant_sounds(X, resultant_sounds, sample_rate)
            if selection_value == "ERR":
                with open(os.path.join(cfg.output_numpy_path, "Error_values.npy"), "rb") as file:
                    X_errors = np.load(file)
                    Y_errors = np.load(file)
                    errors = np.load(file)
                    actual_locations = np.load(file)
                    calculated_locations = np.load(file)
                return selection_value, self.visualize_error(X_errors, Y_errors, errors)
            if selection_value == "RNG":
                with open(os.path.join(cfg.output_numpy_path, "Error_values.npy"), "rb") as file:
                    X_errors = np.load(file)
                    Y_errors = np.load(file)
                    errors = np.load(file)
                    actual_locations = np.load(file)
                    calculated_locations = np.load(file)
                return selection_value, self.visualize_range(actual_locations)
        app.run_server(debug = True)