import React from 'react'
import { Navigate } from 'react-router-dom'

const PrivateRoute = ({ children }) => {
    const token = localStorage.getItem('jwtToken')

    if (!token) {
        return <Navigate to="/login"/>
    }

    return children
}

export default PrivateRoute