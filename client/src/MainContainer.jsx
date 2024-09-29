import { useState } from "react";
import { useNavigate } from "react-router-dom"
import axios from 'axios'

const Home = () => <div><h2>Home Component</h2><p>Welcome to the Home page!</p></div>;
const Workouts = () => <div><h2>Workouts Component</h2><p>Here are your workouts!</p></div>;
const Requests = () => <div><h2>Requests Component</h2><p>These are your requests!</p></div>;
const Profile = () => <div><h2>Profile Component</h2><p>This is your profile.</p></div>;

const MainContainer = ({ setAuth }) => {
    const navigate = useNavigate()
    const [activeComponent, setActiveComponent] = useState('home');

    const handleLogout = () => {
        navigate('/login')
        localStorage.removeItem('jwtToken')
        setAuth(false)
    }

    const renderComponent = () => {
        switch (activeComponent) {
            case 'home':
                return <Home />;
            case 'workouts':
                return <Workouts />;
            case 'requests':
                return <Requests />;
            case 'profile':
                return <Profile />;
            default:
                return <Home />;
        }
    };

    return (
        <div>
            <nav className="navbar navbar-expand-lg navbar-light bg-light">
                <div className="container">
                    <a className="navbar-brand">GymGoat</a>
                    <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="collapse navbar-collapse" id="navbarNav">
                        <ul className="navbar-nav">
                            <li className="nav-item">
                                <button className="nav-link btn btn-link" onClick={() => setActiveComponent('home')} >Home</button>
                            </li>
                            <li className="nav-item">
                                <button className="nav-link btn btn-link " onClick={() => setActiveComponent('workouts')}>Workouts</button>
                            </li>
                            <li className="nav-item">
                                <button className="nav-link btn btn-link" onClick={() => setActiveComponent('requests')}>Requests</button>
                            </li>
                        </ul>
                        <ul className="navbar-nav ms-auto">
                            <li className="nav-item">
                                <button className="btn btn-outline-primary" onClick={() => setActiveComponent('profile')}>Profile</button>
                            </li>
                            <li className="nav-item">
                                <button className="btn btn-outline-danger ms-2" onClick={handleLogout}>Log Out</button>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>

            <div className="container mt-4">
                {renderComponent()}
            </div>
        </div>
    )
}

export default MainContainer

// const testRequest = async () => {
//     try { 
//         const token = localStorage.getItem('jwtToken')
//         const config = {
//             headers: {
//                 'Authorization': `Bearer ${token}`
//             }
//         }

//         const response = await axios.get("http://127.0.0.1:8000/api/auth/protected", config)
//         console.log(response.data)
//     } catch (error) {
//         console.log(error)
//     }
// }

{/* <div>
            PISS
            <button onClick={handleLogout}>Logout</button>
            <button onClick={testRequest}>Test</button>
        </div> */}