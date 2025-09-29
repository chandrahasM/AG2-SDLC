import { WeatherData, OpenMeteoCurrentResponse, GeocodingResponse } from '../types/weather';

export interface ForecastData {
  date: string;
  temperature: number;
  condition: string;
  humidity: number;
  windSpeed: number;
}

class WeatherService {
  private geocodingBaseURL: string = 'https://geocoding-api.open-meteo.com/v1';
  private weatherBaseURL: string = 'https://api.open-meteo.com/v1';

  // Helper function to convert weather code to description
  private getWeatherDescription(code: number): string {
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
  }

  // Helper function to get weather icon
  private getWeatherIcon(code: number): string {
    if (code === 0 || code === 1) return '☀️';
    if (code === 2 || code === 3) return '☁️';
    if (code >= 45 && code <= 48) return '🌫️';
    if (code >= 51 && code <= 67) return '🌧️';
    if (code >= 71 && code <= 77) return '❄️';
    if (code >= 80 && code <= 86) return '🌦️';
    if (code >= 95 && code <= 99) return '⛈️';
    return '🌤️';
  }

  async getCurrentWeather(location: string): Promise<WeatherData> {
    try {
      // First, get coordinates for the location
      const geocodingResponse = await fetch(
        `${this.geocodingBaseURL}/search?name=${encodeURIComponent(location)}&count=1&language=en&format=json`
      );
      
      if (!geocodingResponse.ok) {
        throw new Error('Failed to find location');
      }
      
      const geocodingData: { results: GeocodingResponse[] } = await geocodingResponse.json();
      
      if (!geocodingData.results || geocodingData.results.length === 0) {
        throw new Error('Location not found');
      }
      
      const { latitude, longitude, name, country } = geocodingData.results[0];
      
      // Then, get weather data
      const weatherResponse = await fetch(
        `${this.weatherBaseURL}/current?latitude=${latitude}&longitude=${longitude}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,wind_direction_10m,surface_pressure,cloud_cover&timezone=auto`
      );
      
      if (!weatherResponse.ok) {
        throw new Error('Failed to fetch weather data');
      }
      
      const weatherApiData: OpenMeteoCurrentResponse = await weatherResponse.json();
      
      // Transform Open-Meteo data to our WeatherData format
      return {
        location: `${name}, ${country}`,
        temperature: Math.round(weatherApiData.current.temperature_2m),
        description: this.getWeatherDescription(weatherApiData.current.weather_code),
        humidity: weatherApiData.current.relative_humidity_2m,
        windSpeed: Math.round(weatherApiData.current.wind_speed_10m),
        feelsLike: Math.round(weatherApiData.current.apparent_temperature),
        icon: this.getWeatherIcon(weatherApiData.current.weather_code),
        pressure: Math.round(weatherApiData.current.surface_pressure),
        visibility: 10, // Default value
        uvIndex: undefined
      };
    } catch (error) {
      console.error('Error fetching current weather:', error);
      throw new Error('Failed to fetch current weather data');
    }
  }

  async getForecast(location: string, days: number = 7): Promise<ForecastData[]> {
    try {
      // First, get coordinates for the location
      const geocodingResponse = await fetch(
        `${this.geocodingBaseURL}/search?name=${encodeURIComponent(location)}&count=1&language=en&format=json`
      );
      
      if (!geocodingResponse.ok) {
        throw new Error('Failed to find location');
      }
      
      const geocodingData: { results: GeocodingResponse[] } = await geocodingResponse.json();
      
      if (!geocodingData.results || geocodingData.results.length === 0) {
        throw new Error('Location not found');
      }
      
      const { latitude, longitude } = geocodingData.results[0];
      
      // Get forecast data
      const forecastResponse = await fetch(
        `${this.weatherBaseURL}/forecast?latitude=${latitude}&longitude=${longitude}&daily=temperature_2m_max,temperature_2m_min,weather_code,relative_humidity_2m,wind_speed_10m_max&timezone=auto&forecast_days=${days}`
      );
      
      if (!forecastResponse.ok) {
        throw new Error('Failed to fetch forecast data');
      }
      
      const forecastApiData = await forecastResponse.json();
      
      // Transform forecast data
      const forecast: ForecastData[] = [];
      for (let i = 0; i < days; i++) {
        forecast.push({
          date: forecastApiData.daily.time[i],
          temperature: Math.round((forecastApiData.daily.temperature_2m_max[i] + forecastApiData.daily.temperature_2m_min[i]) / 2),
          condition: this.getWeatherDescription(forecastApiData.daily.weather_code[i]),
          humidity: forecastApiData.daily.relative_humidity_2m[i],
          windSpeed: Math.round(forecastApiData.daily.wind_speed_10m_max[i])
        });
      }
      
      return forecast;
    } catch (error) {
      console.error('Error fetching forecast:', error);
      throw new Error('Failed to fetch forecast data');
    }
  }

  async searchLocations(query: string): Promise<string[]> {
    try {
      const response = await fetch(
        `${this.geocodingBaseURL}/search?name=${encodeURIComponent(query)}&count=10&language=en&format=json`
      );
      
      if (!response.ok) {
        throw new Error('Failed to search locations');
      }
      
      const data: { results: GeocodingResponse[] } = await response.json();
      
      if (!data.results) {
        return [];
      }
      
      return data.results.map(result => `${result.name}, ${result.country}`);
    } catch (error) {
      console.error('Error searching locations:', error);
      throw new Error('Failed to search locations');
    }
  }
}

export const weatherService = new WeatherService();
export default weatherService;