import React, { useState } from 'react';

const Appointment = ({ appointment }) => {
  const [appointmentName, setAppointmentName] = useState(appointment.appointment_name);
  const [appointmentDate, setAppointmentDate] = useState(appointment.appointment_date);
  const [patientName, setPatientName] = useState(appointment.patientName);

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      // call backend api to update info TODO
      console.log(`Updated: ${appointmentName}, ${appointmentDate}, ${patientName}`);
    }
  };

  return (
    <div
      key={appointment._id}
      className="appointment flex flex-col bg-white p-4 rounded-lg shadow-md transition duration-300 ease-in-out transform hover:scale-105 hover:bg-gray-100"
    >
      <input
        type="text"
        className="border p-2 mb-2"
        value={appointmentName}
        onChange={(e) => setAppointmentName(e.target.value)}
        onKeyPress={(e) => handleKeyPress(e)}
      />
      <input
        type="text"
        className="border p-2 mb-2"
        value={appointmentDate}
        onChange={(e) => setAppointmentDate(e.target.value)}
        onKeyPress={(e) => handleKeyPress(e)}
      />
      <input
        type="text"
        className="border p-2 mb-2"
        value={patientName}
        onChange={(e) => setPatientName(e.target.value)}
        onKeyPress={(e) => handleKeyPress(e)}
      />
    </div>
  );
};

export default Appointment;
