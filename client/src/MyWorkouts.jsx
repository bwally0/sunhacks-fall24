import React, { useState } from 'react';
import './MainPage.css'; // Ensure your CSS file is linked

const ownedWorkouts = [
    { id: 1, name: 'Chest', description: 'Workout focused on chest muscles.', owner: 'John Doe' },
    { id: 2, name: 'Back', description: 'Workout focused on back muscles.', owner: 'Jane Smith' },
    { id: 3, name: 'Legs', description: 'Workout focused on leg muscles.', owner: 'Alex Johnson' },
    { id: 4, name: 'Chest', description: 'Workout focused on chest muscles.', owner: 'John Doe' },
    { id: 4, name: 'Back', description: 'Workout focused on back muscles.', owner: 'Jane Smith' },
    { id: 6, name: 'Legs', description: 'Workout focused on leg muscles.', owner: 'Alex Johnson' },
    { id: 7, name: 'Chest', description: 'Workout focused on chest muscles.', owner: 'John Doe' },
    { id: 8, name: 'Back', description: 'Workout focused on back muscles.', owner: 'Jane Smith' },
    { id: 9, name: 'Legs', description: 'Workout focused on leg muscles.', owner: 'Alex Johnson' },
];

const joinedWorkouts = [
    { id: 4, name: 'Shoulders', description: 'Workout focused on shoulder muscles.', owner: 'Emily Davis' },
    { id: 5, name: 'Arms', description: 'Workout focused on arm muscles.', owner: 'Michael Brown' },
    { id: 6, name: 'Cardio', description: 'Workout focused on cardiovascular health.', owner: 'Sarah Wilson' },
    { id: 4, name: 'Chest', description: 'Workout focused on chest muscles.', owner: 'John Doe' },
    { id: 4, name: 'Back', description: 'Workout focused on back muscles.', owner: 'Jane Smith' },
    { id: 6, name: 'Legs', description: 'Workout focused on leg muscles.', owner: 'Alex Johnson' },
    { id: 7, name: 'Chest', description: 'Workout focused on chest muscles.', owner: 'John Doe' },
    { id: 8, name: 'Back', description: 'Workout focused on back muscles.', owner: 'Jane Smith' },
    { id: 9, name: 'Legs', description: 'Workout focused on leg muscles.', owner: 'Alex Johnson' }
];

const MyWorkouts = () => {
  const [activeWorkout, setActiveWorkout] = useState(null);
  const [showModal, setShowModal] = useState(false); // State for the modal

  const toggleModal = () => setShowModal(!showModal);
  const handleRequest = () => {
    toggleModal(); // Show modal when request button is clicked
  };

  return (
    <div className="mainpage-container">
      <div className="sidebar left-sidebar">
        <h2>Owned Workouts</h2>
        {ownedWorkouts.map((workout) => (
          <div 
            key={workout.id} 
            className={`workout-container ${activeWorkout === workout.id ? 'active' : ''}`} 
            onClick={() => setActiveWorkout(activeWorkout === workout.id ? null : workout.id)}
          >
            <h3>{workout.name}</h3>
            {activeWorkout === workout.id && (
              <div>
                <p>{workout.description}</p>
                <p><strong>Owner:</strong> {workout.owner}</p> {/* Display the workout owner's info */}
              </div>
            )}
          </div>
        ))}
      </div>
      
      <div className="sidebar right-sidebar">
        <h2>Joined Workouts</h2>
        {joinedWorkouts.map((workout) => (
          <div 
            key={workout.id} 
            className={`workout-container ${activeWorkout === workout.id ? 'active' : ''}`} 
            onClick={() => setActiveWorkout(activeWorkout === workout.id ? null : workout.id)}
          >
            <h3>{workout.name}</h3>
            {activeWorkout === workout.id && (
              <div>
                <p>{workout.description}</p>
                <p><strong>Owner:</strong> {workout.owner}</p> {/* Display the workout owner's info */}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="content-area">
        <h1>{activeWorkout ? ownedWorkouts.find(w => w.id === activeWorkout)?.name || joinedWorkouts.find(w => w.id === activeWorkout)?.name : 'Select a workout'}</h1>
        <p>{activeWorkout ? ownedWorkouts.find(w => w.id === activeWorkout)?.description || joinedWorkouts.find(w => w.id === activeWorkout)?.description : 'Please select a workout from the sidebar.'}</p>
        
        {/* Request to Join Button */}
        <div className="button-container">
          <button className="request-button" onClick={handleRequest}>Request to Join</button>
        </div>
      </div>

      {/* Modal Popup */}
      {showModal && (
        <div className="modal-overlay" onClick={toggleModal}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <span className="close" onClick={toggleModal}>&times;</span>
            <h2>Request to Join</h2>
            <p>Your request has been sent successfully!</p>
            <button onClick={toggleModal}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default MyWorkouts;
