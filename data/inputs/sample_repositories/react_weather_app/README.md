# React Weather App with Open-Meteo API

A beautiful React weather application that displays current weather conditions using the free Open-Meteo API.

## Features

- 🌤️ **Real-time Weather Data**: Get current weather conditions for any location
- 🔍 **Location Search**: Search for weather by city name
- 📱 **Responsive Design**: Works perfectly on desktop and mobile devices
- 🎨 **Beautiful UI**: Modern gradient design with smooth animations
- 🌍 **Global Coverage**: Supports weather data for locations worldwide
- 🆓 **Free API**: Uses Open-Meteo API (no API key required)

## Weather Information Displayed

- Temperature (current and "feels like")
- Weather condition with emoji icons
- Humidity percentage
- Wind speed
- Atmospheric pressure
- Weather description

## Technologies Used

- **React 18** with TypeScript
- **Open-Meteo API** for weather data
- **CSS3** with modern styling
- **Fetch API** for HTTP requests

## Quick Start

```bash
# Install dependencies
npm install

# Start the development server
npm start

# Open http://localhost:3000 in your browser
```

That's it! The app will work out of the box with no additional configuration needed.

## Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- npm or yarn

### Installation

1. Navigate to the project directory:
   ```bash
   cd data/inputs/sample_repositories/react_weather_app
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open your browser and go to `http://localhost:3000`

## How to Use

1. **Default Location**: The app loads with London weather by default
2. **Search for Weather**: 
   - Type a city name in the search box at the top
   - Click "Search" or press Enter
   - The weather card will update with the new location's data

## API Integration

This app uses the **Open-Meteo API**, which provides:

- **Geocoding API**: Converts city names to coordinates
- **Weather API**: Provides current weather data
- **No API Key Required**: Completely free to use
- **High Accuracy**: Professional-grade weather data

### API Endpoints Used

- **Geocoding**: `https://geocoding-api.open-meteo.com/v1/search`
- **Current Weather**: `https://api.open-meteo.com/v1/forecast` (with current parameters)

## Project Structure

```
react_weather_app/
├── public/
│   └── index.html           # HTML template (Create React App)
├── src/
│   ├── components/
│   │   ├── WeatherCard.tsx  # Main weather display component
│   │   ├── WeatherCard.css  # Weather card styling
│   │   ├── SearchForm.tsx   # Search input component
│   │   └── SearchForm.css   # Search form styling
│   ├── services/
│   │   └── weatherService.ts # API service layer
│   ├── types/
│   │   └── weather.ts       # TypeScript type definitions
│   ├── App.tsx              # Main app component
│   ├── App.css              # App styling
│   └── index.tsx            # App entry point (Create React App)
├── package.json             # Dependencies and scripts
└── README.md               # This file
```

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm build` - Builds the app for production
- `npm test` - Launches the test runner
- `npm eject` - Ejects from Create React App (one-way operation)

## Error Handling

The app includes comprehensive error handling for:
- Invalid location names
- Network connectivity issues
- API service unavailability
- Malformed API responses

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.