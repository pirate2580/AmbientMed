import React, { useState } from 'react';
import { useNavigate } from 'react-router';

const Appointment = ({ appointment, onDelete }) => {
  const [appointmentName, setAppointmentName] = useState(appointment.appointment_name);
  const [appointmentDate, setAppointmentDate] = useState(new Date(appointment.appointment_date));
  const [patientName, setPatientName] = useState(appointment.patient_name);
  const navigate = useNavigate();

  const handleDateChange = (field, value) => {
    const updatedDate = new Date(appointmentDate);
    
    switch (field) {
      case 'day':
        updatedDate.setDate(value);
        break;
      case 'month':
        updatedDate.setMonth(value);
        break;
      case 'year':
        updatedDate.setFullYear(value);
        break;
      case 'hour':
        updatedDate.setHours(value);
        break;
      case 'minute':
        updatedDate.setMinutes(value);
        break;
      default:
        break;
    }

    console.log(`Updated: ${appointmentName}, ${appointmentDate.toLocaleString()}, ${patientName}`);
    setAppointmentDate(updatedDate);
  };

  const handleKeyPress = async (e) => {
    if (e.key === 'Enter') {
      console.log(`Updated: ${appointmentName}, ${appointmentDate.toLocaleString()}, ${patientName}`);
      try {
        const response = await fetch(`http://localhost:3001/appointments/${appointment._id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            'appointment_name': appointmentName,
            'appointment_date': appointmentDate,
            'patient_name': patientName,
          }),
        });

        if (!response.ok) {
          console.log('Error updating data');
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const appointmentData = await response.json();
        console.log('Updated Appointment:', appointmentData);

      } catch (error) {
        console.error("Error occurred:", error);
      }
    }
  };

  const handleDelete = async (e) => {
    // Your delete logic will go here
    // console.log(`Delete appointment with ID: ${appointment._id}`);
    e.stopPropagation();
    try {
      const response = await fetch(`http://localhost:3001/appointments/${appointment._id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        console.log('Error updating data');
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const appointmentData = await response.json();
      console.log('Deleted Appointment:', appointmentData);
      onDelete();
    } catch (error) {
      console.error("Error occurred:", error);
    }
  };
  const handleCardClick = () => {
    navigate(`/appointment/${appointment._id}`);  // Navigate to the detailed view of the appointment
  };

  return (
    <div
      className="appointment flex flex-col bg-white p-4 rounded-lg shadow-md transition duration-300 ease-in-out transform hover:scale-105 hover:bg-gray-100 relative pb-10"
      onClick={handleCardClick}
    >
      {/* appointment name */}
      <input
        type="text"
        className="border p-2 mb-2"
        value={appointmentName}
        onChange={(e) => setAppointmentName(e.target.value)}
        onKeyPress={handleKeyPress}
      />

      {/* appointment date */}
      <div className="flex mb-2 items-center space-x-2">
        <label className="text-sm">Day:</label>
        <select
          value={appointmentDate.getDate()}
          onChange={(e) => handleDateChange('day', parseInt(e.target.value))}
          className="border p-2 rounded"
        >
          {[...Array(31).keys()].map(day => (
            <option key={day + 1} value={day + 1}>{day + 1}</option>
          ))}
        </select>

        <label className="text-sm">Month:</label>
        <select
          value={appointmentDate.getMonth()}
          onChange={(e) => handleDateChange('month', parseInt(e.target.value))}
          className="border p-2 rounded"
        >
          {Array.from({ length: 12 }, (_, month) => (
            <option key={month} value={month}>{new Date(0, month).toLocaleString('en', { month: 'long' })}</option>
          ))}
        </select>

        <label className="text-sm">Year:</label>
        <select
          value={appointmentDate.getFullYear()}
          onChange={(e) => handleDateChange('year', parseInt(e.target.value))}
          className="border p-2 rounded"
        >
          {Array.from({ length: 50 }, (_, i) => (
            <option key={i} value={2020 + i}>{2020 + i}</option>
          ))}
        </select>

        <label className="text-sm">Hour:</label>
        <select
          value={appointmentDate.getHours()}
          onChange={(e) => handleDateChange('hour', parseInt(e.target.value))}
          className="border p-2 rounded"
        >
          {Array.from({ length: 24 }, (_, hour) => (
            <option key={hour} value={hour}>{hour.toString().padStart(2, '0')}</option>
          ))}
        </select>

        <label className="text-sm">Minute:</label>
        <select
          value={appointmentDate.getMinutes()}
          onChange={(e) => handleDateChange('minute', parseInt(e.target.value))}
          className="border p-2 rounded"
        >
          {Array.from({ length: 60 }, (_, minute) => (
            <option key={minute} value={minute}>{minute.toString().padStart(2, '0')}</option>
          ))}
        </select>
      </div>

      {/* patient name */}
      <input
        type="text"
        className="border p-2 mb-2"
        value={patientName}
        onChange={(e) => setPatientName(e.target.value)}
        onKeyPress={handleKeyPress}
      />

      {/* delete button */}
      <button
        onClick={handleDelete}
        className="absolute bottom-2 right-2 bg-red-500 text-white py-1 px-2 rounded text-sm hover:bg-red-600 transition duration-300"
      >
        Delete
      </button>
    </div>
  );
};

export default Appointment;
