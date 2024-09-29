import React, {useState, useEffect} from 'react'
import axios from 'axios'
import { BrowserRouter, Route, Router, Routes } from 'react-router-dom'
import LoginPage from './LoginPage'
import PrivateRoute from './PrivateRoute'
import TestPage from './TestPage'

function App() {
  const [auth, setAuth] = useState(false)

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage setAuth={setAuth}/>}/>
        <Route
          path="/"
          element={
            <PrivateRoute>
              <TestPage/>
            </PrivateRoute>
          }
        />
      </Routes>  
    </BrowserRouter>
  )
}

export default App
