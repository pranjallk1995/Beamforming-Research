import os

# basic
renderer = "vscode"
username = "Pranjall"
api_key = "oxp7TxZd22G3qte3rWoc"

# fundamental
number_of_microphones = 3
number_of_microphone_arrays = 2
d = 0.1
S = 343
scanning_window = 0.2
actual_thetas = [25, 45]
Delta = 0.5
step = 1

# paths
sound_path = os.path.join(os.getcwd(), "Audio", "Imports", "Pulse_001.wav")
output_sound_path = os.path.join(os.getcwd(), "Audio", "Exports")
output_export_path = os.path.join(os.getcwd(), "Exports")