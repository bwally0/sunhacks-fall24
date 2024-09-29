import { useEffect, useState } from "react";
import axios from 'axios';
import bannerImage from './assets/banner.jpg'; 
import './App.css'; // Ensure to import your CSS file

const WorkoutCard = ({ workout, onClick }) => {
    return (
        <div className="card p-1 workout-card" onClick={() => onClick(workout)}>
            <div className="card-body">
                <h5 className="card-title">{workout.name}</h5>
                <div className="mb-2">
                    {workout.tag1 && <span className="badge bg-primary me-1">{workout.tag1}</span>}
                    {workout.tag2 && <span className="badge bg-secondary me-1">{workout.tag2}</span>}
                    {workout.tag3 && <span className="badge bg-success me-1">{workout.tag3}</span>}
                </div>
                <p className="card-text">{workout.date_time}</p>
            </div>
        </div>
    );
};

const Workouts = () => {
    const [ownedWorkouts, setOwnedWorkouts] = useState([]);
    const [selectedWorkout, setSelectedWorkout] = useState([]);
    const [joinedWorkouts, setJoinedWorkouts] = useState([]);
    const [ownerInfo, setOwnerInfo] = useState([]);

    const handleWorkoutClick = async (workout) => {
        setSelectedWorkout(workout);
        const token = localStorage.getItem('jwtToken');
        const config = {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        };
        try {
            const owner_id = workout.owner_id
            const userResponse = await axios.get(`http://127.0.0.1:8000/api/user/${owner_id}`, config);
            setOwnerInfo(userResponse.data);
        } catch (error) {
            console.log(error);
        }       
    };

    const getOwnedWorkouts = async () => {
        try { 
            const token = localStorage.getItem('jwtToken');
            const config = {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            };

            const response = await axios.get("http://127.0.0.1:8000/api/workout/owned", config);
            console.log(response.data);
            setOwnedWorkouts(response.data);
            handleWorkoutClick(response.data[0]);
        } catch (error) {
            console.log(error);
        }
    };

    const getJoinedWorkouts = async () => {
        try { 
            const token = localStorage.getItem('jwtToken');
            const config = {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            };

            const response = await axios.get("http://127.0.0.1:8000/api/workout/joined", config);
            console.log(response.data);
            setJoinedWorkouts(response.data);
        } catch (error) {
            console.log(error);
        }
    }

    useEffect(() => {
        getOwnedWorkouts();
        getJoinedWorkouts();
    }, []);

    return (
        <div className="container-fluid h-100">
            <div className="row h-100">
                {/* Owned Workouts */}
                <div className="col-4 border d-flex flex-column">
                    <div className="p-3">
                        <h5 className="text-center">Your Workouts</h5>
                    </div>
                    <div className="overflow-auto flex-fill" style={{ maxHeight: 'calc(90vh - 70px)', scrollbarWidth: 'none' }}>
                        {ownedWorkouts.length > 0 ? (
                            ownedWorkouts.map(workout => (
                                <div key={workout.workout_id} className="mb-1">
                                    <WorkoutCard workout={workout} onClick={handleWorkoutClick}/>
                                </div>
                            ))
                        ) : (
                            <p>No workouts available.</p>
                        )}
                    </div>
                    <div className="d-flex p-3 mt-auto">
                        <button className="btn btn-success me-1">Create</button>
                        <button className="btn btn-warning">Edit</button>
                    </div>
                </div>
                

                {/* Joined Workouts */}
                <div className="col-4 border d-flex flex-column">
                    <div className="p-3">
                        <h5 className="text-center">Joined Workouts</h5>
                    </div>
                    <div className="overflow-auto flex-fill" style={{ maxHeight: 'calc(90vh - 70px)', scrollbarWidth: 'none' }}>
                        {joinedWorkouts.length > 0 ? (
                            joinedWorkouts.map(workout => (
                                <div key={workout.workout_id} className="mb-1">
                                    <WorkoutCard workout={workout} onClick={handleWorkoutClick}/>
                                </div>
                            ))
                        ) : (
                            <p>No workouts available.</p>
                        )}
                    </div>
                    
                </div>

                
                <div className="col-4 border d-flex">
                    {selectedWorkout ? ( 
                        <div className="p-3 d-flex flex-column flex-grow-1">
                            <h2>{selectedWorkout.name}</h2>
                            <div className="mb-2">
                                {selectedWorkout.tag1 && <span className="badge bg-primary me-1">{selectedWorkout.tag1}</span>}
                                {selectedWorkout.tag2 && <span className="badge bg-secondary me-1">{selectedWorkout.tag2}</span>}
                                {selectedWorkout.tag3 && <span className="badge bg-success me-1">{selectedWorkout.tag3}</span>}
                            </div>
                            <h6>{selectedWorkout.date_time}</h6>
                            <h5>{selectedWorkout.location}</h5>
                            <p>{selectedWorkout.description}</p>

                            <h5>Host Info</h5>
                            <p>{ownerInfo.first_name} {ownerInfo.last_name}: {ownerInfo.phone}</p>
                        </div>
                    ) : (
                        <p>Select a workout to see details.</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Workouts