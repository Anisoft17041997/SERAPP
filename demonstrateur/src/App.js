import React, { useState, useRef } from 'react';
import axios from 'axios';
import './bootstrap/css/bootstrap.min.css';
import Container from 'react-bootstrap/Container';
import { FaMicrophone, FaStop, FaFileImport, FaSearch} from 'react-icons/fa';
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';
import './App.css';

function App() {
  const [audioUrl, setAudioUrl] = useState('');
  const fileInputRef = useRef(null);
  const [audioFile, setAudioFile] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const mediaRecorderRef = useRef(null);
  const [audioBlob, setAudioBlob] = useState(null);
  const [lastAction, setLastAction] = useState(null);

  const openFileSelector = () => {
    fileInputRef.current.click();
  };

  const handleUpload = (event) => {
    const file = event.target.files[0];
    setAudioFile(file);
    setLastAction('upload');
    setAudioUrl(URL.createObjectURL(file));
  };

  const cleanupAudioUrl = () => {
    if (audioUrl) {
      URL.revokeObjectURL(audioUrl);
      setAudioUrl('');
    }
  };

  const cleanup = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.ondataavailable = null;
    }
    setIsRecording(false);
    cleanupAudioUrl();
  };

  const handleSuccess = (response) => {
    setResult(response.data);
    cleanup();
  };

  const handleError = (error) => {
    console.error('Error in submitting file:', error);
    setError('An error occurred while sending the data.');
  };

  const handleRecordingError = (error) => {
    console.error('Error during recording:', error);
    setError('Failed to start recording. Please ensure the microphone is accessible.');
  };

  const startRecording = async () => {
    try {
      setError('');
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      let chunks = [];
      mediaRecorderRef.current.ondataavailable = event => chunks.push(event.data);
      mediaRecorderRef.current.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/wav' });
        setAudioBlob(blob);
        setLastAction('record');
        setAudioUrl(URL.createObjectURL(blob));
        chunks = [];
      };
      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (error) {
      handleRecordingError(error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
    }
    setIsRecording(false);
  };

  const handleSubmit = async () => {
    if (!audioFile) return;
    
    setResult(null);
    setError('');
  
    try {
      const formData = new FormData();
      formData.append('audio_file', audioFile);
      const response = await axios.post('http://127.0.0.1:8000/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Accept': 'application/json',
        },
      });
      setResult(response.data);
      handleSuccess(response);
    } catch (error) {
      handleError(error);
    }
  };

  return (
    <Container className="my-5 text-center">
      <h1 className="mb-3">Speech Emotion Recognition - SERAPP</h1>
      {error && <Alert variant="danger">{error}</Alert>}
      <div className="result-box" style={{ marginBottom: '5vh' }}>
        Analysis result : {result ? (result.prediction === "1" ? "Anger" : "Other emotion") : 'Waiting...'}
      </div>
      <Button variant="primary" onClick={isRecording ? stopRecording : startRecording} className="btn mt-3">
        {isRecording ? <FaStop className="mr-2" /> : <FaMicrophone className="mr-2" />}
        {isRecording ? ' Stop recording' : ' Start recording'}
      </Button>
      <span> </span>
      <Button variant="primary" onClick={openFileSelector} className="btn mt-3 ml-2">
        <FaFileImport className="mr-2" /> Upload audio
      </Button>
      <input type="file" onChange={handleUpload} accept="audio/*" className="d-none" ref={fileInputRef} />
      <Button variant="success" disabled={!audioFile && !audioBlob} onClick={handleSubmit} className="btn d-block mx-auto mt-3">
        <FaSearch className="mr-2" /> Start analysis
      </Button><br/>
      <div className="audio-player-container">
        <audio src={audioUrl} controls />
      </div>
    </Container>
  );
}

export default App;
