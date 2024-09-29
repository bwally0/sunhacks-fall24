import { useState } from "react"
import axios from 'axios'
import { useNavigate } from "react-router-dom"

const LoginPage = ({ setAuth }) => {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault()
        try {
            const response = await axios.post("http://127.0.0.1:8000/api/auth/login", { username, password })
            
            const token = response.data.access_token
            localStorage.setItem('jwtToken', token)
            console.log(token)

            setAuth(true)
            navigate('/')
        } catch (error) {
            console.log(error)
            setError('Invalid Login')
        }
    }

    return(
        <div>
            <h1>LOGIN FORM</h1>
            <form onSubmit={handleLogin}>
                <input
                type="username"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                />
                <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                />
                <button type="submit">Login</button>
                {error && <p>{error}</p>}
            </form>
        </div>
    )
}

export default LoginPage;