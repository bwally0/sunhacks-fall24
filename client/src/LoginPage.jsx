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
        <div className="container d-flex justify-content-center align-items-center" style={{ minHeight: "100vh" }}>
            <div className="row">
                <div className="card p-3 mx-auto" style={{ width: "350px" }}>
                    <h2 className="text-center">Login</h2>
                    <form onSubmit={handleLogin}>
                        <div className="form-group p-2">
                            <label>Username</label>
                            <input type="username" className="form-control" placeholder="Enter username" value={username} onChange={(e) => setUsername(e.target.value)} />
                        </div>
                        <div className="form-group p-2">
                            <label>Password</label>
                            <input type="password" className="form-control" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
                        </div>
                        {error && <p className="p-2">{error}</p>}
                        <div className="text-center p-2">
                            <button type="submit" className="btn btn-primary">Login</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
}

export default LoginPage;

{/* <h1>LOGIN FORM</h1>
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
                
            </form> */}