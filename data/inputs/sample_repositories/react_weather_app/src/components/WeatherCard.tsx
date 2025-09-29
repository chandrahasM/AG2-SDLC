import React, { useState, useEffect } from 'react';
import './WeatherCard.css';
import { WeatherData, OpenMeteoCurrentResponse } from '../types/weather';

interface WeatherCardProps {
  location: string;
}

const WeatherCard: React.FC<WeatherCardProps> = ({ location }) => {
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
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
      console.log('Fetching weather data for:', location);
      
      // First, get coordinates for the location using Open-Meteo Geocoding API
      const geocodingUrl = `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(location)}&count=1&language=en&format=json`;
      console.log('Geocoding URL:', geocodingUrl);
      
      const geocodingResponse = await fetch(geocodingUrl);
      console.log('Geocoding response status:', geocodingResponse.status);
      
      if (!geocodingResponse.ok) {
        throw new Error(`Failed to find location: ${geocodingResponse.status} ${geocodingResponse.statusText}`);
      }
      
      const geocodingData = await geocodingResponse.json();
      console.log('Geocoding data:', geocodingData);
      
      if (!geocodingData.results || geocodingData.results.length === 0) {
        throw new Error('Location not found');
      }
      
      const { latitude, longitude, name, country } = geocodingData.results[0];
      console.log('Coordinates:', { latitude, longitude, name, country });
      
      // Then, get weather data using Open-Meteo Weather API
      const weatherUrl = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,wind_direction_10m,surface_pressure,cloud_cover&timezone=auto`;
      console.log('Weather URL:', weatherUrl);
      
      const weatherResponse = await fetch(weatherUrl);
      console.log('Weather response status:', weatherResponse.status);
      
      if (!weatherResponse.ok) {
        throw new Error(`Failed to fetch weather data: ${weatherResponse.status} ${weatherResponse.statusText}`);
      }
      
      const weatherApiData: OpenMeteoCurrentResponse = await weatherResponse.json();
      console.log('Weather data:', weatherApiData);
      
      // Transform Open-Meteo data to our WeatherData format
      const transformedData: WeatherData = {
        location: `${name}, ${country}`,
        temperature: Math.round(weatherApiData.current.temperature_2m),
        description: getWeatherDescription(weatherApiData.current.weather_code),
        humidity: weatherApiData.current.relative_humidity_2m,
        windSpeed: Math.round(weatherApiData.current.wind_speed_10m),
        feelsLike: Math.round(weatherApiData.current.apparent_temperature),
        icon: getWeatherIcon(weatherApiData.current.weather_code),
        pressure: Math.round(weatherApiData.current.surface_pressure),
        visibility: 10, // Open-Meteo doesn't provide visibility in current API
        uvIndex: undefined // Not available in current API
      };
      
      setWeatherData(transformedData);
    } catch (err) {
      console.error('Error fetching weather data:', err);
      const errorMessage = err instanceof Error ? err.message : 'An error occurred';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // Helper function to convert weather code to description
  const getWeatherDescription = (code: number): string => {
    const weatherCodes: { [key: number]: string } = {
      0: 'Clear sky',
      1: 'Mainly clear',
      2: 'Partly cloudy',
      3: 'Overcast',
      45: 'Fog',
      48: 'Depositing rime fog',
      51: 'Light drizzle',
      53: 'Moderate drizzle',
      55: 'Dense drizzle',
      61: 'Slight rain',
      63: 'Moderate rain',
      65: 'Heavy rain',
      71: 'Slight snow fall',
      73: 'Moderate snow fall',
      75: 'Heavy snow fall',
      77: 'Snow grains',
      80: 'Slight rain showers',
      81: 'Moderate rain showers',
      82: 'Violent rain showers',
      85: 'Slight snow showers',
      86: 'Heavy snow showers',
      95: 'Thunderstorm',
      96: 'Thunderstorm with slight hail',
      99: 'Thunderstorm with heavy hail'
    };
    return weatherCodes[code] || 'Unknown';
  };

  // Helper function to get weather icon (you can replace with actual icons)
  const getWeatherIcon = (code: number): string => {
    if (code === 0 || code === 1) return '☀️';
    if (code === 2 || code === 3) return '☁️';
    if (code >= 45 && code <= 48) return '🌫️';
    if (code >= 51 && code <= 67) return '🌧️';
    if (code >= 71 && code <= 77) return '❄️';
    if (code >= 80 && code <= 86) return '🌦️';
    if (code >= 95 && code <= 99) return '⛈️';
    return '🌤️';
  };


  if (loading) {
    return (
      <div className="weather-card">
        <div className="loading">Loading weather data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="weather-card">
        <div className="error">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="weather-card">
      {weatherData && (
        <div className="weather-content">
          <h2 className="location">{weatherData.location}</h2>
          <div className="weather-main">
            <div className="temperature">{weatherData.temperature}°C</div>
            <div className="weather-icon">{weatherData.icon}</div>
          </div>
          <div className="condition">{weatherData.description}</div>
          <div className="feels-like">Feels like {weatherData.feelsLike}°C</div>
          <div className="details">
            <div className="detail-item">
              <span className="label">Humidity:</span>
              <span className="value">{weatherData.humidity}%</span>
            </div>
            <div className="detail-item">
              <span className="label">Wind Speed:</span>
              <span className="value">{weatherData.windSpeed} km/h</span>
            </div>
            <div className="detail-item">
              <span className="label">Pressure:</span>
              <span className="value">{weatherData.pressure} hPa</span>
            </div>
            {weatherData.visibility && (
              <div className="detail-item">
                <span className="label">Visibility:</span>
                <span className="value">{weatherData.visibility} km</span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default WeatherCard;