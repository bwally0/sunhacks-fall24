import React, { useState } from 'react';
import './MainPage.css'; // Ensure your CSS file is linked

const workouts = [
    { id: 1, name: 'Chest', description: 'Workout focused on chest muscles.', owner: 'John Doe' },
    { id: 2, name: 'Back', description: 'Workout focused on back muscles.', owner: 'Jane Smith' },
    { id: 3, name: 'Legs', description: 'Workout focused on leg muscles.', owner: 'Alex Johnson' },
    { id: 4, name: 'Shoulders', description: 'Workout focused on shoulder muscles.', owner: 'Emily Davis' },
    { id: 5, name: 'Arms', description: 'Workout focused on arm muscles.', owner: 'Michael Brown' },
    { id: 6, name: 'Cardio', description: 'Workout focused on cardiovascular health.', owner: 'Sarah Wilson' },
    { id: 7, name: 'Shoulders', description: 'Workout focused on shoulder muscles.', owner: 'Emily Davis' },
    { id: 8, name: 'Arms', description: 'Workout focused on arm muscles.', owner: 'Michael Brown' },
    { id: 9, name: 'Cardio', description: 'Workout focused on cardiovascular health.', owner: 'Sarah Wilson' },
  ];
  

const MainPage = () => {
  const [activeWorkout, setActiveWorkout] = useState(null);
  const [showModal, setShowModal] = useState(false); // State for the modal

  const toggleModal = () => setShowModal(!showModal);
  const handleRequest = () => {
    toggleModal(); // Show modal when request button is clicked
  };

  return (
    <div className="mainpage-container">
      <div className="sidebar">
        <h2>Workouts</h2>
        {workouts.map((workout) => (
          <div 
            key={workout.id} 
            className={`workout-container ${activeWorkout === workout.id ? 'active' : ''}`} 
            onClick={() => setActiveWorkout(activeWorkout === workout.id ? null : workout.id)}
          >
            <h3>{workout.name}</h3>
            {activeWorkout === workout.id && (
              <p>{workout.description}</p>
            )}
          </div>
        ))}
      </div>
      <div className="content-area">
        <h1>{activeWorkout ? workouts.find(w => w.id === activeWorkout).name : 'Select a workout'}</h1>
        <p>{activeWorkout ? workouts.find(w => w.id === activeWorkout).description : 'Please select a workout from the sidebar.'}</p>
        
        {/* Request to Join Button */}
        <div className="button-container">
          <button className="request-button" onClick={handleRequest}>Request to Join</button>
        </div>
      </div>
    </div>
  );
};

export default MainPage;
