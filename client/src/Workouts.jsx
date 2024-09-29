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
    const [showModal, setShowModal] = useState(false);

    const [name, setName] = useState('');
    const [date_time, setDate_time] = useState('');
    const [location, setLocation] = useState('');
    const [description, setDescription] = useState('');
    const [tag1, setTag1] = useState('');
    const [tag2, setTag2] = useState('');
    const [tag3, setTag3] = useState('');

    const openModal = () => {
        setShowModal(true);
    }

    const closeModal = () => { 
        setShowModal(false)
    }

    const handleCreateWorkout = async () => {
        try { 
            const token = localStorage.getItem('jwtToken');
            const config = {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            };

            const body = {
                name: name,
                date_time: date_time,
                location: location,
                description: description,
                tag1: tag1,
                tag2: tag2,
                tag3: tag3
            }

            const response = await axios.post("http://127.0.0.1:8000/api/workout/create", body, config);
            console.log(response.data);
            getOwnedWorkouts();
            closeModal();
        } catch (error) {
            console.log(error);
        }
    }

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
                        <button className="btn btn-success me-1" onClick={openModal}>Create</button>
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

                    {showModal && (
                <div className="modal show d-block" tabIndex="-1" role="dialog">
                    <div className="modal-dialog" role="document">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h5 className="modal-title">Create A Workout</h5>
                            </div>
                            <div className="modal-body">
                            <form>
                                    <div className="form-group p-2">
                                        <input type="text" className="form-control" placeholder="Workout Name" value={name} onChange={(e) => setName(e.target.value)} />
                                    </div>
                                    <div className="form-group p-2">
                                        <input type="datetime-local" className="form-control" placeholder="Date & Time" value={date_time} onChange={(e) => setDate_time(e.target.value)} />
                                    </div>
                                    <div className="form-group p-2">
                                        <input type="text" className="form-control" placeholder="Location" value={location} onChange={(e) => setLocation(e.target.value)} />
                                    </div>
                                    <div className="form-group p-2">
                                        <textarea className="form-control" placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)}></textarea>
                                    </div>
                                    <div className="form-group p-2">
                                        <input type="text" className="form-control" placeholder="Tag 1" value={tag1} onChange={(e) => setTag1(e.target.value)} />
                                    </div>
                                    <div className="form-group p-2">
                                        <input type="text" className="form-control" placeholder="Tag 2" value={tag2} onChange={(e) => setTag2(e.target.value)} />
                                    </div>
                                    <div className="form-group p-2">
                                        <input type="text" className="form-control" placeholder="Tag 3" value={tag3} onChange={(e) => setTag3(e.target.value)} />
                                    </div>
                            </form>
                            </div>
                            <div className="modal-footer">
                                <button type="button" className="btn btn-secondary" onClick={closeModal}>
                                    Close
                                </button>
                                <button type="button" className="btn btn-primary" onClick={handleCreateWorkout}>
                                    Add
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
                </div>
            </div>
        </div>
    );
};

export default Workouts