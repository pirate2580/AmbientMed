import React, { useState, useRef } from 'react';
import image from '../../assets/download.png'
const Upload = () => {
  const [isRecording, setIsRecording] = useState(false);  // for conditional render
  const [videoURL, setVideoURL] = useState(null);
  const videoRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const recordedChunks = useRef([]);

  const startRecording = async () => {
    setIsRecording(true);
    recordedChunks.current = [];

    // request camera access
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    // videoRef.current.srcObject = stream;
    // videoRef.current.play();
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
      <div className="flex flex-col justify-center items-center h-16 w-16 mx-auto my-4">
        {isRecording ? (
          <div className="flex flex-col items-center cursor-pointer" onClick={stopRecording}>
            <img 
              src={image} 
              alt="Stop Recording" 
              className="h-8 w-8"
            />
            <span className="text-black ml-2">Stop Recording</span>
        </div>
        ) : (
          <div className="flex flex-col items-center cursor-pointer" onClick={startRecording}>
            <img 
              src={image} 
              alt="Start Recording" 
              className="h-8 w-8"
            />
            <span className="text-black ml-2">Start Recording</span>
        </div>
        )}
      </div>
    </div>
  );
}

export default Upload;