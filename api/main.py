import joblib
import librosa
from flask import Flask, request, jsonify
from ml.features_extraction.extract_features import extract_features
#
app = Flask(__name__)
#
# Load the machine learning model
model = joblib.load('../ml/models/model.pkl')
#
@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'Aucun fichier audio trouvé'})
        else:
            # Get the input audio file from the request and save
            audio_file = request.file('audio_file')
            audio_file.save('audio.wav')
            # Load the audio file using librosa
            audio, sr = librosa.load('audio.wav', sr=None)
            # Extract features from the audio
            features = extract_features(audio, sr)
            # Make a prediction using the loaded model
            prediction = model.predict(features.reshape(1, -1))[0]
            # Return the prediction as a JSON response
            return jsonify({prediction})
    except Exception as e:
        return jsonify({'error': str(e)})
   
if __name__ == '__main__':
    app.run(port=8000, debug=True)