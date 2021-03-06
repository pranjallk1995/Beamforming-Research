import os

# fundamental
coordinate_system = [0, 1]
number_of_microphones = 3
number_of_microphone_arrays = 2
d = 0.1
S = 343
scanning_window = 0.2
actual_thetas = [20, 40]
Delta = 0.5
step = 1

# paths
sound_path = os.path.join(os.getcwd(), "Audio", "Imports", "Pulse_001.wav")
output_sound_path = os.path.join(os.getcwd(), "Audio", "Exports")
output_export_path = os.path.join(os.getcwd(), "Exports")
output_numpy_path = os.path.join(os.getcwd(), "Exports")

# flags
suppress_plots = False
calculate_errors = False

# plotting
threshold = 0.3
number_x = 0.01
number_y = 0.08
normal_x = 0.05