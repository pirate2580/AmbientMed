import React, { useState, useEffect } from 'react';
import Sidebar from './SidebarComponent';
import Header from './HeaderComponent'
import Appointment from './Appointment';

const Main = () => {
  const [appointments, setAppointments] = useState([]);

  useEffect(() => {
    const fetchAppointments = async () => {
      try {
        const response = await fetch('http://localhost:3001/appointments/all', {
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          console.log('Error getting data');
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const appointmentData = await response.json();
        console.log('Fetched Appointments:', appointmentData); // Log the fetched data
        setAppointments(appointmentData);

      } catch (error) {
        console.error("Error occurred:", error); // Log any errors
      }
    };
    fetchAppointments();
  }, []);

  return (
    <div className="main flex h-screen overflow-hidden">
      <Sidebar />
      <div className="content flex-1 flex flex-col">
        <Header />
        {/* <AppointmentList appointments={appointments} /> */}
        <div className="appointments grid grid-cols-1 gap-4 p-4 overflow-y-auto">
          {appointments.map((appointment) => (
            <Appointment appointment={appointment}/>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Main;