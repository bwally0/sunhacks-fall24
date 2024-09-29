import React, {useState, useEffect} from 'react'
import { BrowserRouter, Route, Router, Routes } from 'react-router-dom'
import LoginPage from './LoginPage'
import PrivateRoute from './PrivateRoute'
import MainContainer from './MainContainer'

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
              <MainContainer setAuth={setAuth}/>
            </PrivateRoute>
          }
        />
      </Routes>  
    </BrowserRouter>
  )
}

export default App
