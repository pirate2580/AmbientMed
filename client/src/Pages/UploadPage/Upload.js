import React, { useState, useEffect, useRef } from 'react';
import download from '../../assets/record.svg';
import upload from '../../assets/upload.png';
const Upload = () => {
  const [isRecording, setIsRecording] = useState(false);  // for conditional render
  const [videoURL, setVideoURL] = useState(null);
  const videoRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const recordedChunks = useRef([]);

  useEffect(() => {
    const savedVideoURL = localStorage.getItem('videoURL');
    if (savedVideoURL) {
      setVideoURL(savedVideoURL);
    }
  }, []);

  const sendRecording = async() => {
    if (!videoURL){
      return;
    }
    const blob = await fetch(videoURL).then(r => r.blob());
    const formData = new FormData();
    formData.append("video", blob, 'recording.webm');
    
    try{
      const response = await fetch('http://localhost:3001/appointments/', {
        method: 'POST',
        body: formData,
      });
      if (response.ok) {
        const data = await response.json();
        console.log("Video uploaded successfully!", data);
      } else {
        console.error("Failed to upload video.");
      }
    }
    catch (error) {
      console.error("Error uploading video:", error)
    }
  }

  const startRecording = async () => {
    setIsRecording(true);
    recordedChunks.current = [];

    // request camera access
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    if (videoRef.current) {
      videoRef.current.srcObject = stream;
      videoRef.current.play();
    }

    // Set up MediaRecorder
    const mediaRecorder = new MediaRecorder(stream, {
      mimeType: 'video/webm',
    });

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        recordedChunks.current.push(event.data);
      }
    };

    mediaRecorder.onstop = () => {
      const blob = new Blob(recordedChunks.current, {
        type: 'video/webm',
      });
      const url = URL.createObjectURL(blob);
      setVideoURL(url);
      localStorage.setItem('videoURL', url); 
    };

    mediaRecorder.start();
    mediaRecorderRef.current = mediaRecorder;
  }

  const stopRecording = () => {
    setIsRecording(false);
    if (mediaRecorderRef.current){
      mediaRecorderRef.current.stop();
      // Stop all video streams
      const stream = videoRef.current.srcObject;
      if (stream){
        const tracks = stream.getTracks();
        tracks.forEach((track) => track.stop());
      }
    }
  };
  // There is only a URL if a video has been recorded already
  // if a video is recorded and a new one isn't being recorded, show the video for playback
  return (
    <div className="flex flex-col h-screen">
      
      
      {videoURL && !isRecording? (
        <div className="flex items-center flex-col justify-center bg-black flex-grow">
          <h3 className=" w-full bg-white font-bold">Recorded Video</h3>
          <video
            key="recordedVideo" // This key helps React uniquely identify the component
            src={videoURL}
            className="w-[90vw] h-[80vh] min-h-[400px] object-cover"
            controls
          />
        </div>
      ): (
        <div className="flex items-center flex-col justify-center bg-black flex-grow">        
          <h3 className="w-full bg-white font-bold">{isRecording ? 'Recording...' : 'Start Recording Your Appointment'}</h3>
          <video
            key="liveVideo" // This key helps React uniquely identify the component
            ref={videoRef}
            className="w-[90vw] h-[80vh] min-h-[400px] object-cover bg-black"
            autoPlay
            muted
          />
        </div>
      )}
      
      <div className="bg-slate-300 w-full h-[15vh] flex justify-center items-end mx-auto px-4">
        {isRecording ? (
          <div className="flex flex-col items-center cursor-pointer hover:bg-slate-50 rounded-md transition-colors duration-300 p-2" onClick={stopRecording}>
            <img 
              src={download} 
              alt="Stop Recording" 
              className="h-8 w-8"
            />
            <span className="text-black ml-2">Stop Recording</span>
        </div>
        ) : (
          <div className="flex flex-col items-center cursor-pointer hover:bg-slate-100 rounded-md transition-colors duration-200 p-2" onClick={startRecording}>
            <img 
              src={download} 
              alt="Start Recording" 
              className="h-8 w-8"
            />
            <span className="text-black ml-2">Start Recording</span>
        </div>
        )}
        {videoURL ? (
          <div className="flex flex-col items-center cursor-pointer hover:bg-slate-100 rounded-md transition-colors duration-200 p-2" onClick={sendRecording}>
            <img
              src={upload}
              alt="upload"
              className="h-8 w-8"
            />
            <span className="text-black ml-1 mt-1">Upload</span>
        </div>
        ): (
          <div className="flex flex-col items-center cursor-pointer hover:bg-slate-100 rounded-md transition-colors duration-200 p-2" onClick={sendRecording}>
            <img
              src={upload}
              alt="upload"
              className="h-8 w-8"
            />
            <span className="text-red-500 ml-1 mt-1">Upload</span>
          </div>
        )}
      </div>
    </div>
  );
}

export default Upload;