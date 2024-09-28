import React, {useState, useEffect} from 'react'
import axios from 'axios'

function App() {
  const [message, setMessage] = useState([])

  useEffect(() => {
    axios.get('http://127.0.0.1:8000')
      .then(response => {
        setMessage(response.data)
      })
      .catch(error => {
        console.error(error)
      })
  }, [])

  return (
    <>
      <div className="card">
        <div className="card-body">{message.message}</div>
      </div>
    </>
  )
}

export default App
