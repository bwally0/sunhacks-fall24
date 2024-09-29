import { useState, useEffect } from "react";
import axios from "axios";

const Profile = () => {
    const [userData, setUserData] = useState(null);  // Start as null to check if data is fetched
    const [loading, setLoading] = useState(true);    // Track loading state

    const getUserData = async () => {
        try { 
            const token = localStorage.getItem('jwtToken');
            const config = {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            };

            const response = await axios.get("http://127.0.0.1:8000/api/user", config);
            console.log(response.data);
            setUserData(response.data);  // Set the data once it is fetched
        } catch (error) {
            console.log(error);
        } finally {
            setLoading(false);  // Stop loading once the request is done
        }
    }

    useEffect(() => {
        getUserData();
    }, []);

    // If loading is true, show a loading message
    if (loading) {
        return <div>Loading...</div>;
    }

    // If userData is null or undefined, handle error case
    if (!userData) {
        return <div>Error loading user data.</div>;
    }

    return (
        <div>
            <h1>Profile</h1>
            <p>Name: {userData.first_name} {userData.last_name}</p>
            <p>Location: {userData.location}</p>
            <p>Gender: {userData.gender}</p>
            <p>Gender: {userData.phone}</p>
        </div>
    );
};

export default Profile;
