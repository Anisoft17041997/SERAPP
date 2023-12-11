import os
import librosa
import numpy as np
import soundfile as sf
from scipy.signal import find_peaks
#
#
#
def normalize(data):
    max_X = np.max(np.abs(data))
    Y = data / max_X

    return Y
#
#
#
def remove_silence(data, factor):
    max_X = np.max(np.abs(data))
    decision_threshold = max_X / factor

    # Find the indices of samples above the decision threshold
    indices_useful_X, _ = find_peaks(np.abs(data), height=decision_threshold)

    # Extract the useful samples
    Y = data[indices_useful_X[0]:indices_useful_X[-1] + 1]

    return Y
#
#
#
def normalise_remove_silence(input_filename, output_directory, factor):
    # Read the input audio file
    x, fs = librosa.load(input_filename, sr=None)

    # Normalize the audio
    y = normalize(x)

    # Remove silence
    z = remove_silence(y, factor)

    # Extract the filename and extension
    filename, extension = os.path.splitext(os.path.basename(input_filename))

    # Create the output filename in the specified directory
    output_filename = os.path.join(output_directory, f"{filename}_N_RS{factor}{extension}")

    # Write the processed audio to the output file
    sf.write(output_filename, z, fs)