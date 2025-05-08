import React, { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/suggestion")
      .then(response => response.json())
      .then(json => {
        setData(json);
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching suggestion:", error);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading weather suggestion...</p>;
  if (!data) return <p>No suggestion available.</p>;

  return (
    <div>
      <h1>Weather Suggestion</h1>
      <p><strong>Temperature:</strong> {data.temperature}</p>
      <p><strong>Suggestion:</strong> {data.suggestion}</p>
    </div>
  );
}

export default App;

