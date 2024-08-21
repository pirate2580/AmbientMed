import './App.css';
import React from 'react';
import { RouterProvider } from 'react-router';
import { createBrowserRouter } from "react-router-dom";
import Upload from './Pages/UploadPage/Upload'
import Main from './Pages/MainPage/Main';
import Login from './Pages/LoginPage/Login';

const router = createBrowserRouter([
  {
    path: "/asdf", 
    element: <Login/>
  },
  {
    path: '/upload',
    element: <Upload/>
  },
  {
    path: "/",
    element: <Main/>
  },
  {
    path: '*',
    element: <h1>404 error</h1>
  }
])

function App() {
  return (
    <div className="App w-full h-full overflow-x-hidden overflow-y-auto">
      {/* <Upload/> */}
      <RouterProvider router={router}/>
    </div>
  );
}

export default App;
