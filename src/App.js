import React, { useState, useEffect } from 'react';
import Select from 'react-select';
import Papa from 'papaparse';
import './App.css';

function App() {
  const [options, setOptions] = useState([]);

  const [selectedDegrees, setSelectedDegrees] = useState([]);
  const [comparisonResults, setComparisonResults] = useState([]);

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/api/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          selectedDegrees: selectedDegrees
        }),
      });
      const data = await response.json();
      console.log(data);
      setComparisonResults(data);
    } catch (error) {
      console.error('Error:', error);
    }
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
        <div className="results">
          <h3>Comparison Results:</h3>
          {comparisonResults.length != [] ? (
            <ul>
              {comparisonResults.result.map((result, index) => (
                <li key={index}>
                  {result[0]}: {result[1]} additional classes
                </li>
              ))}
            </ul>
          ) : (
            <p>No comparison results available yet.</p>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
