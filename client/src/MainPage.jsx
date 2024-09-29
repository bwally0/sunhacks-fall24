import React, {useState, useEffect} from 'react'

const Home = () => <div><h1>Home</h1><p>Welcome to the home page!</p></div>;
const MyWorkouts = () => <div><h1>My Workouts</h1><p>Here are your workouts.</p></div>;
const Requests = () => <div><h1>Requests</h1><p>You have no new requests.</p></div>;

const MainPage = () => {
  const [activePage, setActivePage] = useState("home");

  const renderPage = () => {
    switch (activePage) {
      case "home":
        return <Home />;
      case "myworkouts":
        return <MyWorkouts />;
      case "requests":
        return <Requests />;
      default:
        return <Home />;
    }
  };

  return (
    <div>
      <nav>
        <ul>
          <li onClick={() => setActivePage("home")}>Home</li>
          <li onClick={() => setActivePage("myworkouts")}>My Workouts</li>
          <li onClick={() => setActivePage("requests")}>Requests</li>
        </ul>
      </nav>
      <div>{renderPage()}</div>
    </div>
  );
}

export default MainPage