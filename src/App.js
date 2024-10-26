import React, { useState } from 'react';
import './App.css';

function App() {
  const [major, setMajor] = useState('');
  const [minor, setMinor] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Major: ${major}\nMinor/Concentration: ${minor || 'None'}`);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Purdue Dual Major Finder</h1>
      </header>
      <main className="App-main">
        <h2>Find what major/minor you could add with the fewest additional classes</h2>
        <form onSubmit={handleSubmit}>
          <h3>Enter your current major (and minor/concentration):</h3>
          <div className="form-group">
            <label htmlFor="major">Major: </label>
            <input
              type="text"
              id="major"
              value={major}
              onChange={(e) => setMajor(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="minor">Minor/Concentration (if any): </label>
            <input
              type="text"
              id="minor"
              value={minor}
              onChange={(e) => setMinor(e.target.value)}
            />
          </div>
          <button type="submit" className="submit-button">Submit</button>
        </form>
      </main>
    </div>
  );
}

export default App;
