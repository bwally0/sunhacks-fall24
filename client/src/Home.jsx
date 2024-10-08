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

const Home = () => {
    const [workouts, setWorkouts] = useState([]);
    const [selectedWorkout, setSelectedWorkout] = useState([]);

    const handleWorkoutClick = (workout) => {
        console.log(workout)
        setSelectedWorkout(workout);
    };

    const getFeed = async () => {
        try { 
            const token = localStorage.getItem('jwtToken');
            const config = {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            };

            const response = await axios.get("http://127.0.0.1:8000/api/workout/", config);
            setWorkouts(response.data);
            setSelectedWorkout(response.data[0]);
        } catch (error) {
            console.log(error);
        }
    };

    const handleRequestJoin = async () => {
        try { 
            const token = localStorage.getItem('jwtToken');
            const config = {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            };

            const body = {
                owner_id: selectedWorkout.owner_id,
                workout_id: selectedWorkout.workout_id
            }

            const response = await axios.post("http://127.0.0.1:8000/api/request", body, config);
            console.log(response.data);
        } catch (error) {
            console.log(error);
        }
    }

    useEffect(() => {
        getFeed();
    }, []);

    return (
        <div className="container-fluid h-100">
            <div className="row h-100">
                {/* Workout Feed */}
                <div className="col-4 border d-flex flex-column">
                    <div className="p-3">
                        <h5 className="text-center">Your Feed</h5>
                    </div>
                    <div className="overflow-auto flex-fill" style={{ maxHeight: 'calc(90vh - 70px)', scrollbarWidth: 'none' }}>
                        {workouts.length > 0 ? (
                            workouts.map(workout => (
                                <div key={workout.workout_id} className="mb-1">
                                    <WorkoutCard workout={workout} onClick={handleWorkoutClick}/>
                                </div>
                            ))
                        ) : (
                            <p>No workouts available.</p>
                        )}
                    </div>
                </div>

                {/* Workout Info */}
                <div className="col-8 border d-flex">
                    {selectedWorkout ? ( 
                        <div className="p-3 d-flex flex-column flex-grow-1">
                            <div className="banner mb-2">
                                <img src={bannerImage} alt="Workout Banner" className="img-fluid" />
                            </div>
                            <h2>{selectedWorkout.name}</h2>
                            <div className="mb-2">
                                {selectedWorkout.tag1 && <span className="badge bg-primary me-1">{selectedWorkout.tag1}</span>}
                                {selectedWorkout.tag2 && <span className="badge bg-secondary me-1">{selectedWorkout.tag2}</span>}
                                {selectedWorkout.tag3 && <span className="badge bg-success me-1">{selectedWorkout.tag3}</span>}
                            </div>
                            <h6>{selectedWorkout.date_time}</h6>
                            <h5>{selectedWorkout.location}</h5>
                            <p>{selectedWorkout.description}</p>

                            <div className="mt-auto">
                                <button className="btn btn-primary" onClick={handleRequestJoin}>
                                    Request to Join
                                </button>
                            </div>
                        </div>
                    ) : (
                        <p>Select a workout to see details.</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Home;