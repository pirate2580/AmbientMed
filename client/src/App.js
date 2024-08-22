import './App.css';
import React from 'react';
import { RouterProvider } from 'react-router';
import { createBrowserRouter } from "react-router-dom";
import Upload from './Pages/UploadPage/Upload'
import Main from './Pages/MainPage/Main';
import Login from './Pages/LoginPage/Login';
import ProtectedRoute from './Pages/ProtectedRoute/ProtectedRoute'
import AppointmentDetail from './Pages/AppointmentPage/AppointmentDetail';


const router = createBrowserRouter([
  {
    path: "/login", 
    element: <Login/>
  },
  {
    path: '/upload',
    element: <ProtectedRoute element={<Upload />} />  // Protect this route
  },
  {
    path: "/",
    element: <ProtectedRoute element={<Main />} />  // Protect this route
  },
  {
    path: "/appointment/:id",
    element: <ProtectedRoute element={<AppointmentDetail />} />  // Protect this route
  },
  {
    path: '*',
    element: <h1>404 error</h1>
  }
]);

function App() {
  return (
    <div className="App w-full h-full overflow-x-hidden overflow-y-auto">
      {/* <Upload/> */}
      <RouterProvider router={router}/>
    </div>
  );
}

export default App;
