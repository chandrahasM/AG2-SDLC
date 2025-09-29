import React, { useState } from 'react';
import WeatherCard from './components/WeatherCard';
import SearchForm from './components/SearchForm';
import './App.css';

function App() {
  const [currentLocation, setCurrentLocation] = useState('London');

  const handleLocationChange = (location: string) => {
    setCurrentLocation(location);
  };

  const handleSearch = (query: string) => {
    setCurrentLocation(query);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Weather App</h1>
        <SearchForm onSearch={handleSearch} placeholder="Enter city name" />
      </header>
      <main className="App-main">
        <WeatherCard 
          location={currentLocation} 
          onLocationChange={handleLocationChange} 
        />
      </main>
    </div>
  );
}

export default App;