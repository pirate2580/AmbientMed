import React, { useState, useEffect } from 'react';
import Sidebar from './SidebarComponent';
import Header from './HeaderComponent'
import Appointment from './AppointmentComponent';

const Main = () => {
  const [appointments, setAppointments] = useState([]);
  const [triggerFetch, setTriggerFetch] = useState(false);

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
        const sortedAppointments = appointmentData.sort((a, b) => new Date(b.appointment_date) - new Date(a.appointment_date));
        setAppointments(sortedAppointments);

      } catch (error) {
        console.error("Error occurred:", error); // Log any errors
      }
    };
    fetchAppointments();
  }, [triggerFetch]);

  return (
    <div className="main flex h-screen overflow-hidden">
      <Sidebar />
      <div className="content flex-1 flex flex-col">
        <Header />
        {/* <AppointmentList appointments={appointments} /> */}
        <div className="appointments grid grid-cols-1 gap-4 p-4 overflow-y-auto">
          {appointments.map((appointment) => (
            <Appointment 
            key={appointment._id}
            appointment={appointment}
            onDelete={() => setTriggerFetch(!triggerFetch)}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Main;