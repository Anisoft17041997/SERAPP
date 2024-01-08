import React, { useState, useRef } from 'react';
import axios from 'axios';
import './bootstrap/css/bootstrap.min.css';
import Container from 'react-bootstrap/Container';
import {FaMicrophone, FaStop, FaFileImport } from 'react-icons/fa';
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

  const [audioBlob, setAudioBlob] = useState(null);
  const [lastAction, setLastAction] = useState(null);


  const cleanup = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.ondataavailable = null;
    }
    setIsRecording(false);
  };

  const handleRecordingError = (error) => {
    console.error('Error during recording:', error);
    setError('Failed to start recording. Please ensure the microphone is accessible.');
  };

  const handleError = (error) => {
    console.error('Error in submitting file:', error);
    setError('An error occurred while sending the data.');
  };

  const startRecording = async () => {
    try {
      setError('');
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      mediaRecorderRef.current.ondataavailable = (event) => {
        //setAudioFile(event.data);


        setAudioBlob(event.data);
        setLastAction('record'); // Mise à jour de l'action


        audioUrlRef.current = URL.createObjectURL(event.data);
      };
      mediaRecorderRef.current.onerror = handleRecordingError;
      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (error) {
      handleRecordingError(error);
    }
  };

  const stopRecording = () => {
    cleanup();
  };

  const handleUpload = (event) => {
    setAudioFile(event.target.files[0]);

    setLastAction('upload'); // Mise à jour de l'action

  };

  const handleSubmit = async () => {
    //if (!audioFile) return;

    if (lastAction === 'record' && !audioBlob) return;
    if (lastAction === 'upload' && !audioFile) return;


    setResult(null);
    setError('');
  
    setTimeout(async () => {
        try {
          const formData = new FormData();
          //formData.append('audio_file', audioFile);

          if (lastAction === 'upload') {

            console.log('Uploading file:', audioFile);

            formData.append('audio_file', audioFile);
          } else if (lastAction === 'record') {

            console.log('Uploading blob:', audioBlob);

            formData.append('audio_file', new File([audioBlob], 'recording.wav', { type: 'audio/wav' }));
          }

          const response = await axios.post('http://127.0.0.1:8000/predict', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
              'Accept': 'application/json',
            },
          });

          console.log('Response:', response);

          
          setResult(response.data);

        } catch (error) {
          //handleError(error);
          console.error('Error in submitting file:', error);
          setError('An error occurred while sending the data.');

        }
      }, 500); // Attendre 500ms avant d'envoyer
    };

  return (
    <Container className="my-5 text-center">
      <h1 className="mb-3">Analyse des Émotions par la Voix - SERAPP</h1>
      {error && <Alert variant="danger">{error}</Alert>}

      <div className="result-box" style={{ marginBottom: '5vh' }}>Résultat de l'analyse : {result ? (result.prediction === "1" ? "Colère" : "Autre émotion") : 'En attente...'}</div>

      <Button variant="primary" onClick={isRecording ? stopRecording : startRecording} className="mt-3">
        {isRecording ? <FaStop className="mr-2" /> : <FaMicrophone className="mr-2" />}
        {isRecording ? ' Arrêter l\'enregistrement' : ' Démarrer l\'enregistrement'}
      </Button>
      <span> </span>
      <Button variant="secondary" onClick={openFileSelector} className="mt-3 ml-2">
        <FaFileImport className="mr-2" /> Importer un fichier
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
