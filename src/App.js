import React, { useState, useEffect } from 'react';
import Select from 'react-select';
import Papa from 'papaparse';
import './App.css';

function App() {
  const [selectedDegrees, setSelectedDegrees] = useState([]);
  console.log(selectedDegrees);
  const [options, setOptions] = useState([]);

  useEffect(() => {
    Papa.parse('/links.csv', {
      download: true,
      header: true,
      complete: (results) => {
        const parsedOptions = results.data
          .filter(row => row.name) // Filter out empty rows
          .map(row => ({
            value: row.name,
            label: row.name
          }));
        setOptions(parsedOptions);
      },
      error: (error) => {
        console.error('Error parsing CSV:', error);
      }
    });
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    const degrees = selectedDegrees.join(', ');
    alert(`Degrees: ${degrees || 'None'}`);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Purdue Dual Major Finder</h1>
      </header>
      <main className="App-main">
        <h2>Find what degrees you could add with the fewest additional classes</h2>
        <form onSubmit={handleSubmit} style={{ width: '80%', maxWidth: '800px' }}>
          <h3>Select your current degree(s):</h3>
          <div className="form-group">
            <label htmlFor="degree">Degree(s): </label>
            <Select
              isMulti
              name="degrees"
              options={options}
              className="basic-multi-select wide-select"
              classNamePrefix="select"
              value={options.filter(option => selectedDegrees.includes(option.value))}
              onChange={(selectedOptions) => setSelectedDegrees(selectedOptions.map(option => option.value))}
            />
          </div>
          <button type="submit" className="submit-button">Submit</button>
        </form>
      </main>
    </div>
  );
}

export default App;
