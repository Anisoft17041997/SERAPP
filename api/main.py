from flask import Flask, request, jsonify
import joblib
import librosa
import numpy as np
from flask_cors import CORS
#
#
app = Flask(__name__)
CORS(app)
#
# Load the machine learning model
model = joblib.load('model.pkl')
#
#
def extract_features(normalized_y, sr, max_len=100):
    mfccs = librosa.feature.mfcc(y=normalized_y, sr=sr, n_mfcc=13)
    chroma = librosa.feature.chroma_stft(y=normalized_y, sr=sr)
    spectral_contrast = librosa.feature.spectral_contrast(y=normalized_y, sr=sr)

    mfccs = librosa.util.fix_length(mfccs, size = max_len, axis=1)
    chroma = librosa.util.fix_length(chroma, size = max_len, axis=1)
    spectral_contrast = librosa.util.fix_length(spectral_contrast, size = max_len, axis=1)

    flat_mfccs = np.ravel(mfccs)
    flat_chroma = np.ravel(chroma)
    flat_spectral_contrast = np.ravel(spectral_contrast)
    
    # print(np.array(flat_mfccs).reshape(1, -1), np.array(flat_chroma).reshape(1, -1), np.array(flat_spectral_contrast).reshape(1, -1))

    return np.array(flat_mfccs).reshape(1, -1), np.array(flat_chroma).reshape(1, -1), np.array(flat_spectral_contrast).reshape(1, -1)
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

            # Load the audio file using librosa
            audio, sr = librosa.load('./audio.wav', sr=None)
            audio, _ = librosa.effects.trim(audio)
            normalized_y = librosa.util.normalize(audio)

            # Extract features from the audio
            flat_mfccs, flat_chroma, flat_spectral_contrast = extract_features(normalized_y, sr)
            features = np.concatenate((flat_mfccs, flat_chroma, flat_spectral_contrast), axis=1)
            
            # Make a prediction using the loaded model
            prediction = model.predict(features)[0]
            print(prediction)

            # Return the prediction as a JSON response
            return jsonify({'prediction': str(prediction)})
    except Exception as e:
        return jsonify({'error': str(e)})
   
if __name__ == '__main__':
    app.run(port=8000, debug=True)