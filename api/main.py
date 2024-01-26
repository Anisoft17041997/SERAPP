from flask import Flask, request, jsonify
import joblib
import librosa
import random as r
import numpy as np
from flask_cors import CORS
from main_telegram_notif import notify
#
#
app = Flask(__name__)
CORS(app)
#
# Load the machine learning model
model = joblib.load('dtc_model.pkl')
#
#
def process_audio(file_path):
    y, sr = librosa.load(file_path)
    y, _ = librosa.effects.trim(y)
    normalized_y = librosa.util.normalize(y)

    return normalized_y, sr
#
#
def extract_features_seven_features(data, sample_rate):
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
@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'audio_file' not in request.files:
            return jsonify({'error': 'Aucun fichier audio trouvé'})
        else:
            # Get the input audio file from the request and save
            audio_file = request.files['audio_file']
            audio_file.save('./audio.wav')

            # Process the audio
            normalized_y, sr = process_audio('./audio.wav')

            # Extract features from the audio
            features = np.hstack((extract_features_seven_features(normalized_y, sr)))
            features = features.reshape(1, -1)
            
            # Make a prediction using the loaded model
            prediction = model.predict(features)[0]

            # Notify the angry prediction
            notify(f'DET{int(r.uniform(100, 999))}') if prediction == 1 else None

            # Return the prediction as a JSON response
            return jsonify({'prediction': str(prediction)})
    except Exception as e:
        return jsonify({'error': str(e)})
#
#
if __name__ == '__main__':
    app.run(port=8000, debug=True)