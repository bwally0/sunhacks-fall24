import { useNavigate } from "react-router-dom"

const TestPage = ({ setAuth }) => {
    const navigate = useNavigate()

    const handleLogout = () => {
        navigate('/login')
        localStorage.removeItem('jwtToken')
        setAuth(false)
    }
    
    return (
        <div>
            PISS
            <button onClick={handleLogout}>Logout</button>
        </div>
    )
}

export default TestPage