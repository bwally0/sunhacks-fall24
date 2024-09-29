const Home = () => {

    const getFeed = async () => {
        try { 
            const token = localStorage.getItem('jwtToken')
            const config = {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }

            const response = await axios.get("http://127.0.0.1:8000/api/auth/protected", config)
            console.log(response.data)
        } catch (error) {
            console.log(error)
        }
    }

    return (
        <div className="container-fluid">
            <div className="row h-100">
                {/* Workout Feed */}
                <div className="col-4 border d-flex justify-content-center align-items-center">
                    <div>
                        <p>Workout feed</p>
                    </div>
                </div>

                {/* Workout Info */}
                <div className="col-8 border d-flex justify-content-center align-items-center">
                    <div>
                        <p>workout info</p>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Home;