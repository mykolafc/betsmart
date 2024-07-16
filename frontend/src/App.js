import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Replace with your API URL
    fetch('http://localhost:5000/data')
      .then(response => {
        if (!response.ok) {
          // If the response status is not OK, throw an error
          throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
      })
      .then(data => setData(data))
      .catch(error => {
        // Catch any error and set the error state
        setError(error);
        console.error('There was a problem with the fetch operation:', error);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        {error ? (
          // Display error message if there is an error
          <div className="error">
            <p>Error: {error.message}</p>
          </div>
        ) : (
          // Display table if data is successfully fetched
          <table>
            <thead>
              <tr>
                {/* Replace with your column names */}
                <th>ID</th>
                <th>Name</th>
                <th>Age</th>
              </tr>
            </thead>
            <tbody>
              {data.map((row, index) => (
                <tr key={index}>
                  {/* Replace with your column names */}
                  <td>{row.Key}</td>
                  <td>{row.Name}</td>
                  <td>{row.Points}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </header>
    </div>
  );
}

export default App;
