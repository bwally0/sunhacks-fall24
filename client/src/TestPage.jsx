import { useNavigate } from "react-router-dom"
import axios from 'axios'

const TestPage = ({ setAuth }) => {
    const navigate = useNavigate()

    const handleLogout = () => {
        navigate('/login')
        localStorage.removeItem('jwtToken')
        setAuth(false)
    }

    const testRequest = async () => {
        try { 
            const token = localStorage.getItem('jwtToken')
            const config = {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }

            const response = await axios.get("http://127.0.0.1:8000/api/auth/protected", config)
            console.log(response.data)
        } catch (error) {
            console.log(error)
        }
    }
    
    return (
        <div>
            PISS
            <button onClick={handleLogout}>Logout</button>
            <button onClick={testRequest}>Test</button>
        </div>
    )
}

export default TestPage