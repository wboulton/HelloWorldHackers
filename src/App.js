import React, { useState, useEffect } from 'react';
import Select from 'react-select';
import Papa from 'papaparse';
import './App.css';

function App() {
  const [selectedDegrees, setSelectedDegrees] = useState([]);
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
    const degrees = selectedDegrees.map(option => option.label).join(', ');
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
          <div className="form-group" style={{ width: '100%' }}>
            <label htmlFor="degree">Degree(s): </label>
            <Select
              isMulti
              name="degrees"
              options={options}
              className="basic-multi-select"
              classNamePrefix="select"
              value={selectedDegrees}
              onChange={setSelectedDegrees}
              styles={{
                container: (provided) => ({
                  ...provided,
                  width: '100%',
                }),
                control: (provided) => ({
                  ...provided,
                  width: '100%',
                }),
              }}
            />
          </div>
          <button type="submit" className="submit-button" style={{ width: '100%', marginTop: '20px' }}>Submit</button>
        </form>
      </main>
    </div>
  );
}

export default App;
