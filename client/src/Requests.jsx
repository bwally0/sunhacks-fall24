import { useEffect, useState } from "react";
import axios from 'axios';
import bannerImage from './assets/banner.jpg'; 
import './App.css'; // Ensure to import your CSS file

const JoinRequestCard = ({ joinRequest, onApprove, onReject }) => {
    return (
        <div className="card p-1 workout-card">
            <div className="card-body">
                <h5 className="card-title">{joinRequest.user.first_name} {joinRequest.user.last_name}</h5>
                <p className="card-text">{joinRequest.workout.name}</p>
                <div className="d-flex">
                    {/* Approve Button */}
                    <button 
                        className="btn btn-success me-1" 
                        onClick={() => onApprove(joinRequest)}
                    >
                        Approve
                    </button>

                    {/* Reject Button */}
                    <button 
                        className="btn btn-danger" 
                        onClick={() => onReject(joinRequest)}
                    >
                        Reject
                    </button>
                </div>
            </div>
        </div>
    );
};

const YourRequestCard = ({ yourRequest }) => {
    return (
        <div className="card p-1 workout-card">
            <div className="card-body">
                <h5 className="card-title">{yourRequest.workout.name}</h5>
                <p className="card-text">{yourRequest.workout.location}</p>
                <p className="card-text">{yourRequest.workout.date_time}</p>
                <p className="card-text">Pending ...</p>
            </div>
        </div>
    );
}

const Requests = () => {
    const [joinRequests, setJoinRequests] = useState([]);
    const [yourRequests, setYourRequests] = useState([]);

    const approveRequest = async (request) => {
        try { 
            const token = localStorage.getItem('jwtToken');
            const config = {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            };

            const response = await axios.post(`http://127.0.0.1:8000/api/request/accept/${request.request_id}`, {}, config);
            rejectRequest(request)
        } catch (error) {
            console.log(error);
        }
    };

    // Function to handle Reject action
    const rejectRequest = async (request) => {
        try { 
            const token = localStorage.getItem('jwtToken');
            const config = {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            };

            const response = await axios.put(`http://127.0.0.1:8000/api/request/delete/${request.request_id}`, {}, config);
            getJoinRequests()
        } catch (error) {
            console.log(error);
        }
    };

    const getJoinRequests = async () => {
        try { 
            const token = localStorage.getItem('jwtToken');
            const config = {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            };

            let joinRequests = []

            const response = await axios.get("http://127.0.0.1:8000/api/request/owner", config);
            for (const request of response.data) {
                const user_id = request.participant_id
                const workout_id = request.workout_id
                const userResponse = await axios.get(`http://127.0.0.1:8000/api/user/${user_id}`, config);
                const workoutResponse = await axios.get(`http://127.0.0.1:8000/api/workout/${workout_id}`, config);
                request["user"] = userResponse.data
                request["workout"] = workoutResponse.data
                joinRequests.push(request)
            }
            
            setJoinRequests(response.data);
        } catch (error) {
            console.log(error);
        }
    };

    const getYourRequests = async () => {
        try { 
            const token = localStorage.getItem('jwtToken');
            const config = {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            };

            const response = await axios.get("http://127.0.0.1:8000/api/request/user", config);
            
            let yourRequests = []
            
            console.log(response.data);
            for (const request of response.data) {
                const workout_id = request.workout_id
                const workoutResponse = await axios.get(`http://127.0.0.1:8000/api/workout/${workout_id}`, config);
                request["workout"] = workoutResponse.data
                yourRequests.push(request)
            }

            setYourRequests(response.data);
        } catch (error) {
            console.log(error);
        }
    }

    useEffect(() => {
        getJoinRequests()
        getYourRequests()
    }, []);

    return (
        <div className="container-fluid h-100">
            <div className="row justify-content-center h-100">
                {/* Owned Workouts */}
                <div className="col-4 border d-flex flex-column">
                    <div className="p-3">
                        <h5 className="text-center">Join Requests</h5>
                    </div>
                    <div className="overflow-auto flex-fill" style={{ maxHeight: 'calc(90vh - 70px)', scrollbarWidth: 'none' }}>
                        {joinRequests.length > 0 ? (
                            joinRequests.map(request => (
                                <div key={request.request_id} className="mb-1">
                                    <JoinRequestCard joinRequest={request} onApprove={approveRequest} onReject={rejectRequest}/>
                                </div>
                            ))
                        ) : (
                            <p>No requests available.</p>
                        )}
                    </div>
                </div>
                

                {/* Joined Workouts */}
                <div className="col-4 border d-flex flex-column">
                    <div className="p-3">
                        <h5 className="text-center">Your Requests</h5>
                    </div>
                    <div className="overflow-auto flex-fill" style={{ maxHeight: 'calc(90vh - 70px)', scrollbarWidth: 'none' }}>
                        {yourRequests.length > 0 ? (
                            yourRequests.map(request => (
                                <div key={request.request_id} className="mb-1">
                                    <YourRequestCard yourRequest={request} />
                                </div>
                            ))
                        ) : (
                            <p>No requests available.</p>
                        )}
                    </div>
                    
                </div>
            </div>
        </div>
    );
};

export default Requests