import React, { useState, useRef } from 'react';
import axios from 'axios';
import './bootstrap/css/bootstrap.min.css';
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';
import './App.css';

function App() {
  
  const fileInputRef = useRef(null);
  const openFileSelector = () => {
    fileInputRef.current.click();
  };
  const [audioFile, setAudioFile] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const mediaRecorderRef = useRef(null);
  const audioUrlRef = useRef(null);

  const startRecording = async () => {
    try {
      setError('');
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      mediaRecorderRef.current.ondataavailable = (event) => {
        setAudioFile(event.data);
        audioUrlRef.current = URL.createObjectURL(event.data);
      };
      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error starting recording:', error);
      setError('Failed to start recording. Please ensure the microphone is accessible.');
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current.stop();
    setIsRecording(false);
  };

  const handleUpload = (event) => {
    setAudioFile(event.target.files[0]);
  };

  const handleSubmit = async () => {
    if (!audioFile) return;
    setResult(null);
    setError('');
    const formData = new FormData();
    formData.append('voice', audioFile);

    try {
      const response = await axios.post('YOUR_API_ENDPOINT', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data);
    } catch (error) {
      console.error('Error in submitting file:', error);
      setError('An error occurred while sending the data.');
    }
  };

  return (
    <Container className="my-5 text-center">
      <h1 className="mb-4">Analyse des Émotions Vocales</h1>
      {error && <Alert variant="danger">{error}</Alert>}
      <div className="result-box">Résultat de l'analyse : {result ? result : 'En attente...'}</div>
      <Button variant="primary" onClick={isRecording ? stopRecording : startRecording} className="mt-3">
        {isRecording ? 'Arrêter l\'enregistrement' : 'Démarrer l\'enregistrement'}
      </Button>
      <Button variant="secondary" onClick={openFileSelector} className="mt-3 ml-2">
        Importer un fichier
      </Button>
      <input 
        type="file" 
        onChange={handleUpload} 
        accept="audio/*" 
        className="d-none" 
        ref={fileInputRef} 
      />
      <Button variant="success" onClick={handleSubmit} className="d-block mx-auto mt-3">
        Lancer l'analyse
      </Button>
      <audio src={audioUrlRef.current} controls className="my-3" />
    </Container>
  );
}

export default App;
