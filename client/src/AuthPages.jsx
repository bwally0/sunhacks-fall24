import React, { useState } from 'react';
import MainPage from './MainPage';
import Requests from './Requests';
import MyWorkouts from './MyWorkouts';
import SignOut from './SignOut';
import Navbar from './NavBar';

const AuthPages = () => {
  const [activePage, setActivePage] = useState("mainpage");

  // Function to render the active container based on the state
  const renderPage = () => {
    switch (activePage) {
      case "mainpage":
        return <MainPage />;
      case "myworkouts":
        return <MyWorkouts />;
      case "requests":
        return <Requests />;
      case "signout":
        return <SignOut />;
      default:
        return <MainPage />;
    }
  };

  return (
    <div>
      {/* Render the Navbar */}
      <Navbar setActivePage={setActivePage} />

      {/* Container that will change based on the active page */}
      <div> 
        {renderPage()}
        </div>
    </div>
  );
};

export default AuthPages;
