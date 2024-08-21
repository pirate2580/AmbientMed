import React, { useState } from 'react';
import logo from '../../assets/ambientmed.png';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleLogin = async () => {
    const response = await fetch('http://localhost:3001/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });
    const data = await response.json();
    if (response.ok) {
      localStorage.setItem('token', data.token);
      setMessage('Login successful');
      // navigate('/upload');
    } else {
      setMessage(`Error: ${data.message}`);
    }
  };

  const handleRegister = async () => {
    const response = await fetch('http://localhost:3001/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });
    const data = await response.json();
    if (response.ok) {
      localStorage.setItem('token', data.token);
      setMessage('Registration successful');
      // navigate('/upload');
    } else {
      setMessage(`Error: ${data.message}`);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-300">
      <div className="bg-white border border-gray-400 p-8 w-full min-h-screen mx-4 rounded-md shadow-md flex flex-col justify-between">
        <div>
          <h2 className="text-center mb-6 text-2xl font-bold">Login</h2>
        
          <div
            className={`transition-opacity duration-1500 ease-in-out h-12 flex items-center justify-center ${
              message ? 'opacity-100' : 'opacity-0'
            }`}
          >
            <p
              className={`px-4 py-2 rounded-md text-center font-bold text-white ${
                message === 'Login successful' || message === 'Registration successful'
                  ? 'bg-green-500'
                  : 'bg-red-500'
              }`}
            >
              {message}
            </p>
          </div>
        
          <input
            type="email"
            className="border border-gray-300 rounded w-full p-3 mb-4 focus:outline-none focus:border-blue-500"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
          />
        
          <input
            type="password"
            className="border border-gray-300 rounded w-full p-3 mb-6 focus:outline-none focus:border-blue-500"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
          />
        
          <div className="flex justify-center mb-6">
            <img
              src={logo}
              alt="Logo"
              className="h-80 w-auto" // Increased the size of the image
            />
          </div>
        </div>

        <div className="mt-auto">
          <button
            onClick={handleLogin}
            className="w-full bg-blue-500 text-white py-3 rounded-md mb-4 hover:bg-blue-600 transition duration-300"
          >
            Login
          </button>
        
          <button
            onClick={handleRegister}
            className="w-full bg-green-500 text-white py-3 rounded-md hover:bg-green-600 transition duration-300"
          >
            Register
          </button>
        </div>
      </div>
    </div>
  );
};

export default Login;
