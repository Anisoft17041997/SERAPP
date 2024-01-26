import os
from scipy.stats import mode
import librosa
import numpy as np
from tqdm import tqdm
from audiomentations import Compose, TimeStretch, PitchShift, AddGaussianNoise
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
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
def extract_features(nb_features, data, sample_rate):
    if nb_features == 3: return extract_features_three_features(data, sample_rate)
    if nb_features == 7: return extract_features_seven_features(data, sample_rate)
#
#
#
def extract_features_three_features(normalized_y, sr, max_len=100):
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
def extract_features_seven_features(data, sample_rate):
    '''Fonctions d'extration de 7 features'''

    zcr = np.mean(librosa.feature.zero_crossing_rate(y=data).T, axis=0)
    rms_energy = np.mean((librosa.feature.rms(y=data)).T, axis=0)
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=data, sr=sample_rate).T, axis=0)
    spectral_spread = np.mean(librosa.feature.spectral_bandwidth(y=data, sr=sample_rate).T, axis=0)
    spectral_flux = np.mean(librosa.onset.onset_strength(y=data, sr=sample_rate).T, axis=0)
    mfcc = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate, n_mfcc=13).T, axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(y=data, sr=sample_rate).T, axis=0)

    # Stack all features horizontally
    return zcr, rms_energy, spectral_centroid, spectral_spread, spectral_flux, mfcc, chroma
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
    '''Dans notre contexte, nous avons décidé de nous concentrer 
    sur la prédiction d'une émotion: la colère'''

    return 1 if emotion == "anger" else 0
#
#
#
def predict_emotion_three_features(audio_test_file, model):
    '''Fonction qui permet de predire l'emotion d'un fichier audio
     en prenant l'audion et le model en paramètres'''
    
    normalized_y, sr = process_audio(audio_test_file)
    flat_mfccs, flat_chroma, flat_spectral_contrast = extract_features_three_features(normalized_y, sr)

    flat_features = np.hstack((flat_mfccs, flat_chroma, flat_spectral_contrast))
    flat_features = np.array(flat_features).reshape(1, -1)

    prediction = model.predict(flat_features)

    return audio_test_file, prediction[0]
#
#
#
def predict_emotion_seven_features(audio_test_file, model):
    '''Fonction qui permet de predire l'emotion d'un fichier audio
     en prenant l'audion et le model en paramètres'''
    
    normalized_y, sr = process_audio(audio_test_file)
    flat_zcr, flat_rms_energy, flat_spectral_centroid, flat_spectral_spread, flat_spectral_flux, flat_mfcc, flat_chroma = extract_features_seven_features(normalized_y, sr)

    flat_features = np.hstack((flat_zcr, flat_rms_energy, flat_spectral_centroid, flat_spectral_spread, flat_spectral_flux, flat_mfcc, flat_chroma))
    flat_features = np.array(flat_features).reshape(1, -1)

    prediction = model.predict(flat_features)

    return audio_test_file, prediction[0]
#
#
#
def evaluate_model(model, X_test, y_test):
    '''Cette fonction permet d'évaluer un modèle
    params:
    model: Le modèle à évaluer
    X_test: Les labels des données de test
    y_test: Les targets des données de test
    '''

    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

    y_pred = model.predict(X_test)

    _accuracy = accuracy_score(y_test, y_pred)
    _precision = precision_score(y_test, y_pred, average='weighted')
    _recall = recall_score(y_test, y_pred, average='weighted')
    _f1_score = f1_score(y_test, y_pred, average='weighted')

    print(f"Accuracy: {_accuracy:.4f}")
    print(f"Precision: {_precision:.4f}")
    print(f"Recall: {_recall:.4f}")
    print(f"F1 Score: {_f1_score:.4f}")
#
#
#
def get_true_label(file_path):
    return os.path.basename(file_path).split(".")[0].startswith("a")
#
#
#
def predict_emotions_in_directory(model, directory_path):
    audio_files = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.wav')]
        
    predictions = []
    true_emotions = []

    correct_predictions = 0
    incorrect_predictions = 0
    total_angry_audio = 0

    for audio_file in tqdm(audio_files):
  
        # Make prediction using the provided model
        prediction = predict_emotion_seven_features(audio_file, model)

        # Check if the prediction is correct
        true_label = get_true_label(audio_file)
        total_angry_audio += 1 if true_label else 0

        if prediction and true_label:
            correct_predictions += 1
        else:
            incorrect_predictions += 1

        predictions.append(prediction)
        true_emotions.append(true_label)

    total_predictions = len(audio_files)
    print(f"\nTotal Predictions: {total_predictions}")
    print(f"Correct Predictions: {correct_predictions}/{total_angry_audio} angry files")
    print(f"Incorrect Predictions: {incorrect_predictions}")