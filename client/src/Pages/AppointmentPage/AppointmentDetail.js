import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
const AppointmentDetail = () => {
  const { id } = useParams();  // Extract the appointment ID from the URL
  const [appointment, setAppointment] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  // const handleReturn = () => {
  //   na
  // }

  useEffect(() => {
    const fetchAppointment = async () => {
      try {
        const response = await fetch(`http://localhost:3001/appointments/${id}`);
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        if (!data || Object.keys(data).length === 0) {
          throw new Error('Received empty response from the server');
        }

        setAppointment(data);
      } catch (error) {
        setError(error.message);
      }
    };

    fetchAppointment();
  }, [id]);

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!appointment) {
    return <div>Loading...</div>;
  }

  return (
    <div className=" grid grid-cols-2 gap-4 h-screen">
      <div className="col-span-1 bg-slate-200 overflow-y-scroll h-full">
        <h2 className="text-lg font-bold mb-2">SOAP Notes</h2>

        <div className="mb-4 bg-slate-100 m-8 p-4">
          <h3 className="font-bold">Subjective:</h3>
          <p>{appointment.subjective}</p>
        </div>

        <div className="mb-4 bg-slate-100 m-8 p-4">
          <h3 className="font-bold">Objective:</h3>
          <p>{appointment.objective}</p>
        </div>

        <div className="mb-4 bg-slate-100 m-8 p-4">
          <h3 className="font-bold">Assessment:</h3>
          <p>{appointment.assessment}</p>
        </div>

        <div className="mb-4 bg-slate-100 m-8 p-4">
          <h3 className="font-bold">Plan:</h3>
          <p>{appointment.plan}</p>
        </div>
      </div>
      
      <div className="col-span-1 overflow-y-scroll h-full">
        <button className='p-2 rounded-sm bg-green-200 hover:bg-green-300 transition duration-300' onClick={() => {navigate('/')}}>Return</button>
        <h2 className="text-lg font-bold mb-2">Transcription</h2>
        {appointment.transcription.map((segment, index) => (
          <div key={index} className="mb-2 flex flex-col justify-start text-left">
            <p><strong>{segment.speaker}:</strong> {segment.segment_transcription}</p>
            <p className="text-sm text-gray-500">({segment.segment_start.toFixed(2)}s - {segment.segment_end.toFixed(2)}s)</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AppointmentDetail;
