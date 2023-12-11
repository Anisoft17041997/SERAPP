import librosa
import numpy as np
from scipy.stats import mode
#
#
#
def global_feature_computation(feature_matrix, computations):
    computed_features = []
    for computation in computations:
        if computation == "mean":
            computed_features.append(np.mean(feature_matrix, axis=1))
        elif computation == "min":
            computed_features.append(np.min(feature_matrix, axis=1))
        elif computation == "max":
            computed_features.append(np.max(feature_matrix, axis=1))
        elif computation == "std":
            computed_features.append(np.std(feature_matrix, axis=1))
        elif computation == "range":
            computed_features.append(np.ptp(feature_matrix, axis=1))
        elif computation == "mode":
            mode_result = mode(feature_matrix, axis=1)
            computed_features.append(mode_result.mode.flatten())
        elif computation == "median":
            computed_features.append(np.median(feature_matrix, axis=1))
        elif computation == "1st_quartile":
            computed_features.append(np.percentile(feature_matrix, 25, axis=1))
        elif computation == "3rd_quartile":
            computed_features.append(np.percentile(feature_matrix, 75, axis=1))

    return np.concatenate(computed_features)
#
#
#
def extract_features(audio_path, features, global_computation):
    # Load the normalized and silence-removed audio
    audio, sr = librosa.load(audio_path)

    lst_spectral_flatness = []
    lst_spectral_centroid = []
    lst_mfcc = []
    lst_melspectrogram = []
    lst_chroma_stft = []
    lst_rms = []

    feature_list = []

    # Extract selected features
    for feature_name in features:
        if feature_name == "spectral_flatness":
            spectral_flatness = librosa.feature.spectral_flatness(y=audio)
            lst_spectral_flatness.append(global_feature_computation(spectral_flatness, global_computation))
        elif feature_name == "spectral_centroid":
            spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr = sr)
            lst_spectral_centroid.append(global_feature_computation(spectral_centroid, global_computation))
        elif feature_name == "mfcc":
            mfcc = librosa.feature.mfcc(y=audio, sr = sr)
            lst_mfcc.append(global_feature_computation(mfcc, global_computation))
        elif feature_name == "melspectrogram":
            mel_spectrum = librosa.feature.melspectrogram(y=audio, sr = sr)
            lst_melspectrogram.append(global_feature_computation(mel_spectrum, global_computation))
        elif feature_name == "chroma_stft":
            chroma_stft = librosa.feature.chroma_stft(y=audio, sr = sr)
            lst_chroma_stft.append(global_feature_computation(chroma_stft, global_computation))
        elif feature_name == "rms":
            rms = librosa.feature.rms(y=audio)
            lst_rms.append(global_feature_computation(rms, global_computation))

    feature_list.append(lst_spectral_flatness[0])
    feature_list.append(lst_spectral_centroid[0])
    feature_list.append(lst_mfcc[0])
    feature_list.append(lst_melspectrogram[0])
    feature_list.append(lst_chroma_stft[0])
    feature_list.append(lst_rms[0])


    # Combine the extracted features into a single feature vector
    feature_vector = np.concatenate(feature_list)

    return feature_vector
#
#
#
def extract_features(audio, sr):
    pass