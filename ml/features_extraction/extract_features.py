from scipy.stats import mode
import librosa
import numpy as np
from audiomentations import Compose, TimeStretch, PitchShift, AddGaussianNoise
#
#
#
def process_audio(file_path):
    '''Fonction de precession du fichier en vue de le normaliser'''
    y, sr = librosa.load(file_path)
    y, _ = librosa.effects.trim(y)

    normalized_y = librosa.util.normalize(y)

    return normalized_y, sr
#
#
#
def extract_features(normalized_y, sr, max_len=100):
    '''Fonctions de traitement des fichiers audios'''
    mfccs = librosa.feature.mfcc(y=normalized_y, sr=sr, n_mfcc=13)
    chroma = librosa.feature.chroma_stft(y=normalized_y, sr=sr)
    spectral_contrast = librosa.feature.spectral_contrast(y=normalized_y, sr=sr)

    mfccs = librosa.util.fix_length(mfccs, size = max_len, axis=1)
    chroma = librosa.util.fix_length(chroma, size = max_len, axis=1)
    spectral_contrast = librosa.util.fix_length(spectral_contrast, size = max_len, axis=1)

    flat_mfccs = np.ravel(mfccs)
    flat_chroma = np.ravel(chroma)
    flat_spectral_contrast = np.ravel(spectral_contrast)

    return flat_mfccs, flat_chroma, flat_spectral_contrast
#
#
#
def augment_audio(y, sr):
    '''Fonction d'augmentation des fichiers audios'''
    augment = Compose([
        TimeStretch(min_rate=0.8, max_rate=1.2),
        PitchShift(min_semitones=-2, max_semitones=2),
        AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015)
    ])

    augmented_y = augment(samples=y, sample_rate=sr)

    return augmented_y
#
#
#
def is_anger(emotion):
    '''Dans notre contexte, nous avons décidé de nous concentrer sur la prédiction d'une émotion: la colère'''
    return 1 if emotion == "anger" else 0
#
#
#
def predict_emotion(audio_test_file, model):
    '''Fonction qui permet de predire l'emotion d'un fichier audio
     en prenant l'audion et le model en paramètres'''
    normalized_y, sr = process_audio(audio_test_file)
    flat_mfccs, flat_chroma, flat_spectral_contrast = extract_features(normalized_y, sr)

    flat_mfccs = np.array(flat_mfccs).reshape(1, -1)
    flat_chroma = np.array(flat_chroma).reshape(1, -1)
    flat_spectral_contrast = np.array(flat_spectral_contrast).reshape(1, -1)

    flat_features = np.concatenate((flat_mfccs, flat_chroma, flat_spectral_contrast), axis=1)

    prediction = model.predict(flat_features)

    print("Audio File is anger: ", audio_test_file)
    print("Prediction: ", prediction == 1)

    return is_anger(prediction)