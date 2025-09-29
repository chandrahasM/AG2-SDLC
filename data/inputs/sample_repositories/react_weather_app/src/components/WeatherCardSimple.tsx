import React, { useState, useEffect } from 'react';

interface WeatherCardProps {
  location: string;
  onLocationChange: (location: string) => void;
}

const WeatherCardSimple: React.FC<WeatherCardProps> = ({ location, onLocationChange }) => {
  const [weatherData, setWeatherData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (location) {
      fetchWeatherData(location);
    }
  }, [location]);

  const fetchWeatherData = async (location: string) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log('Fetching weather for:', location);
      
      // Test API call
      const response = await fetch(
        `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(location)}&count=1&language=en&format=json`
      );
      
      console.log('Geocoding response status:', response.status);
      
      if (!response.ok) {
        throw new Error('Failed to find location');
      }
      
      const data = await response.json();
      console.log('Geocoding data:', data);
      
      if (!data.results || data.results.length === 0) {
        throw new Error('Location not found');
      }
      
      const { latitude, longitude, name, country } = data.results[0];
      
      // Get weather data
      const weatherResponse = await fetch(
        `https://api.open-meteo.com/v1/current?latitude=${latitude}&longitude=${longitude}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m&timezone=auto`
      );
      
      console.log('Weather response status:', weatherResponse.status);
      
      if (!weatherResponse.ok) {
        throw new Error('Failed to fetch weather data');
      }
      
      const weatherApiData = await weatherResponse.json();
      console.log('Weather data:', weatherApiData);
      
      setWeatherData({
        location: `${name}, ${country}`,
        temperature: Math.round(weatherApiData.current.temperature_2m),
        description: 'Weather data loaded successfully',
        humidity: weatherApiData.current.relative_humidity_2m,
        windSpeed: Math.round(weatherApiData.current.wind_speed_10m),
        feelsLike: Math.round(weatherApiData.current.apparent_temperature)
      });
      
    } catch (err) {
      console.error('Error fetching weather:', err);
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={{ padding: '20px', textAlign: 'center', background: '#f0f0f0', borderRadius: '10px' }}>
        <div>Loading weather data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '20px', textAlign: 'center', background: '#ffebee', borderRadius: '10px', color: 'red' }}>
        <div>Error: {error}</div>
        <button onClick={() => fetchWeatherData(location)} style={{ marginTop: '10px', padding: '10px' }}>
          Retry
        </button>
      </div>
    );
  }

  return (
    <div style={{ padding: '20px', background: '#e3f2fd', borderRadius: '10px', margin: '20px' }}>
      <h2>{weatherData?.location || location}</h2>
      {weatherData && (
        <div>
          <div style={{ fontSize: '24px', fontWeight: 'bold' }}>
            {weatherData.temperature}°C
          </div>
          <div>{weatherData.description}</div>
          <div>Feels like: {weatherData.feelsLike}°C</div>
          <div>Humidity: {weatherData.humidity}%</div>
          <div>Wind: {weatherData.windSpeed} km/h</div>
        </div>
      )}
    </div>
  );
};

export default WeatherCardSimple;
