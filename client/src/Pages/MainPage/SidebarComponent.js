import React from 'react';
import logo from '../../assets/ambientmed.png';
import { useNavigate } from 'react-router';
const Sidebar = () => {
  const navigate = useNavigate();

  return (
    <div className="sidebar bg-gray-200 p-4 w-1/6 h-screen flex flex-col justify-between">
      <div className="profile-pic mb-4">
        <img
          src={logo}
          alt="Profile"
          className="rounded-full w-25 h-24 mx-auto"
        />
        <p className="text-center mt-2">Dr. Jackson</p>
      </div>

      <div className="mt-auto">
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition duration-300 w-full"
          onClick={() => {navigate('/upload')}}
        >
          Record New Appointment
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
