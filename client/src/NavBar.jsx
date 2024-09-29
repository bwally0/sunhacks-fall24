import React, { useState } from 'react';
import './Navbar.css';

const Navbar = ({ setActivePage }) => {
  const [activeTab, setActiveTab] = useState("mainpage");

  const handleTabClick = (page) => {
    setActivePage(page);
    setActiveTab(page);
  };

  return (
    <div className="tabs">
      <nav>
        <a
          href="#mainpage"
          className={activeTab === "mainpage" ? "active" : ""}
          onClick={() => handleTabClick("mainpage")}
        >
          Main Page
        </a>
        <a
          href="#myworkouts"
          className={activeTab === "myworkouts" ? "active" : ""}
          onClick={() => handleTabClick("myworkouts")}
        >
          My Workouts
        </a>
        <a
          href="#requests"
          className={activeTab === "requests" ? "active" : ""}
          onClick={() => handleTabClick("requests")}
        >
          Requests
        </a>
        <a
          href="#signout"
          className={activeTab === "signout" ? "active" : ""}
          onClick={() => handleTabClick("signout")}
        >
          Sign Out
        </a>
      </nav>
    </div>
  );
};

export default Navbar;
