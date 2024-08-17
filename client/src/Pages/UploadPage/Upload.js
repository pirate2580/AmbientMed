import React, { useState, useRef } from 'react';
import download from '../../assets/download.png';
import upload from '../../assets/upload.png';
const Upload = () => {
  const [isRecording, setIsRecording] = useState(false);  // for conditional render
  const [videoURL, setVideoURL] = useState(null);
  const videoRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const recordedChunks = useRef([]);

  const sendRecording = async() => {
    if (!videoURL){

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
    <div>
      
      {videoURL && !isRecording? (
        <div>
          <h3>Recorded Video:</h3>
          <video
            key="recordedVideo" // This key helps React uniquely identify the component
            src={videoURL}
            className="w-full h-[85vh] object-cover"
            controls
          />
        </div>
      ): (
        <div>        
          <h3>{isRecording ? 'Recording...' : 'Start Recording Video:'}</h3>
          <video
            key="liveVideo" // This key helps React uniquely identify the component
            ref={videoRef}
            className="w-full h-[85vh] bg-black object-cover"
            autoPlay
            muted
          />
        </div>
      )}
      
      <div className="flex justify-center items-end h-16 w-full mx-auto my-4 px-4">
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

        <div className="flex flex-col items-center cursor-pointer hover:bg-slate-100 rounded-md transition-colors duration-200 p-2" onClick={sendRecording}>
          <img
            src={upload}
            alt="upload"
            className="h-8 w-8"
          />
          <span className="text-black ml-2">Upload</span>

        </div>
      </div>
    </div>
  );
}

export default Upload;