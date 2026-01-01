# AI Travel Planner 🌍

A powerful travel planning application with **natural language AI interface** that aggregates data from multiple sources to provide comprehensive travel information including weather forecasts, attractions, and travel insights.

## ✨ New Features (v2.0)

- 🤖 **AI Natural Language Interface**: Chat with GPT-4 powered assistant in plain English
- ⚛️ **Modern React UI**: Beautiful, responsive TypeScript frontend
- 💬 **Conversational Queries**: "Plan a 3-day trip to Paris" instead of structured API calls
- 🎨 **Professional Design**: Dark theme with smooth animations
- 📱 **Mobile Responsive**: Works seamlessly on all devices

## Features

- **AI-Powered Chat**: Natural language understanding with GPT-4
- **Multi-Source Data Integration**: Combines data from OpenWeatherMap, OpenStreetMap/Nominatim, and Foursquare
- **Parallel API Calls**: Efficient async requests to multiple APIs simultaneously
- **Smart Caching**: Redis-based city-level caching with configurable TTL
- **Error Handling**: Robust timeout and fallback mechanisms
- **Response Normalization**: Clean, consistent API responses
- **Distance Clustering**: Attractions grouped by distance for easy trip planning

## Tech Stack

### Backend
- **Python 3.9+**
- **FastAPI**: Modern, fast web framework
- **OpenAI GPT-4**: Natural language processing
- **Redis**: In-memory caching layer
- **httpx**: Async HTTP client
- **Pydantic**: Data validation and settings management

### Frontend
- **React 18**: UI framework
- **TypeScript**: Type-safe development
- **Vite**: Lightning-fast build tool
- **Modern CSS**: Component-scoped styling

## Quick Start

### Automated Setup (Recommended)

```bash
# Run the setup script
chmod +x setup.sh
./setup.sh

# Start the application
python main.py

# Open your browser
# Visit: http://localhost:8000/ui
```

### Manual Setup

See [Installation & Setup](#installation--setup) below for detailed instructions.

## Using the AI Chat Interface

Simply open `http://localhost:8000/ui` and start chatting!

**Example queries:**
- "Plan a 3-day trip to Paris"
- "What's the weather like in Tokyo?"
- "Tell me about attractions in Rome"
- "I want to visit Barcelona for 5 days"

The AI understands your intent and provides personalized, conversational responses with all the data you need!

## API Endpoints

### `POST /chat` (New!)

Natural language interface for travel planning.

**Request:**
```json
{
  "query": "Plan a 3-day trip to Paris"
}
```

**Response:**
```json
{
  "query": "Plan a 3-day trip to Paris",
  "response": "I'd be happy to help you plan...",
  "trip_data": { /* full trip details */ }
}
```

### `GET /trip`

Get a comprehensive travel plan for a city (structured API).

**Query Parameters:**
- `city` (required): City name (e.g., "Rome", "Paris", "Tokyo")
- `days` (optional): Number of days for forecast (1-5, default: 3)

**Example Request:**
```bash
curl "http://localhost:8000/trip?city=Rome&days=3"
```

**Response Structure:**
```json
{
  "city": "Rome",
  "country": "Italy",
  "coordinates": {
    "lat": 41.9028,
    "lon": 12.4964
  },
  "days": 3,
  "weather_forecast": [
    {
      "date": "2024-01-15",
      "temp_avg": 15.5,
      "temp_min": 12.0,
      "temp_max": 18.0,
      "description": "clear sky",
      "humidity": 65,
      "wind_speed": 3.5
    }
  ],
  "top_attractions": [
    {
      "name": "Colosseum",
      "category": "Landmark",
      "distance": 0.5,
      "address": "Piazza del Colosseo, Rome",
      "rating": null
    }
  ],
  "travel_notes": {
    "distance_clusters": [
      {
        "cluster_name": "Within 2km (Walking distance)",
        "count": 8,
        "attractions": ["Colosseum", "Roman Forum", "..."]
      }
    ],
    "total_attractions": 20
  },
  "cached": false
}
```

## Installation & Setup

### Prerequisites

1. **Python 3.9 or higher**
2. **Redis server** running locally or remotely
3. **API Keys** for:
   - OpenWeatherMap: [Get free key](https://openweathermap.org/api)
   - Foursquare: [Get API key](https://foursquare.com/developers/apps)

### Step 1: Clone and Install Dependencies

```bash
# Navigate to project directory
cd TravelPlanner

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

Copy the example environment file and add your API keys:

```bash
cp example.env .env
```

Edit `.env` file:

```env
# API Keys (Required)
OPENAI_API_KEY=your_openai_api_key_here
OPENWEATHER_API_KEY=your_actual_openweather_key
FOURSQUARE_API_KEY=your_actual_foursquare_key

# Redis Configuration (adjust if needed)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# Cache TTL (in seconds)
CACHE_TTL=3600

# API Timeouts (in seconds)
API_TIMEOUT=10
```

**Get your API keys:**
- OpenAI: https://platform.openai.com/api-keys
- OpenWeatherMap: https://openweathermap.org/api
- Foursquare: https://foursquare.com/developers/apps

### Step 3: Start Redis

**On macOS (with Homebrew):**
```bash
brew install redis
brew services start redis
```

**On Linux:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

**Using Docker:**
```bash
docker run -d -p 6379:6379 redis:alpine
```

### Step 4: Setup Frontend

```bash
cd frontend
npm install
npm run build
cd ..
```

### Step 5: Run the Application

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 6: Access the Application

- **Web UI**: http://localhost:8000/ui (Main interface)
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc (Alternative docs)

## Development Mode

For frontend development with hot module replacement:

```bash
# Terminal 1: Backend
python main.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

Then open `http://localhost:5173` for the frontend with HMR.

See [REACT_UI_SETUP.md](REACT_UI_SETUP.md) for detailed frontend development guide.

## Project Structure

```
TravelPlanner/
├── frontend/                  # React + TypeScript UI
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── types.ts         # TypeScript types
│   │   ├── api.ts           # API service
│   │   └── App.tsx          # Main app
│   ├── package.json
│   ├── vite.config.ts
│   └── README.md
├── static/                   # Built frontend (generated)
├── api_clients/
│   ├── nominatim.py         # Geocoding client
│   ├── openweather.py       # Weather API client
│   ├── foursquare.py        # Attractions API client
│   └── openai_client.py     # OpenAI GPT-4 client
├── main.py                   # FastAPI application & endpoints
├── config.py                 # Configuration management
├── models.py                 # Pydantic models for responses
├── cache.py                  # Redis caching layer
├── requirements.txt          # Python dependencies
├── setup.sh                  # Automated setup script
├── example.env               # Environment variables template
├── README.md                 # This file
├── REACT_UI_SETUP.md        # Frontend development guide
└── UI_GUIDE.md              # UI usage guide
```

## Skills Showcased

### 1. Parallel API Calls
The application uses `asyncio.gather()` to fetch weather and attractions data simultaneously:

```python
weather_task = weather_client.get_forecast(lat, lon, days)
attractions_task = foursquare_client.get_attractions(lat, lon)

weather_data, attractions_data = await asyncio.gather(
    weather_task,
    attractions_task,
    return_exceptions=True
)
```

### 2. API Response Normalization
Each API client normalizes its specific response format into a common structure:
- Weather: Daily aggregates from 3-hour forecasts
- Attractions: Unified format with calculated distances
- Geocoding: Standardized coordinate format

### 3. Timeout + Fallback Handling
- Configurable timeouts for all API calls
- Graceful degradation with fallback data
- Exception handling at multiple levels
- Redis connection failures don't break the app

### 4. Caching (City-Level)
- Redis-based caching with city+days as key
- Configurable TTL (default: 1 hour)
- Cache-aware responses (includes `cached` flag)
- Graceful operation when Redis is unavailable

## Testing the API

### Basic Test
```bash
curl "http://localhost:8000/trip?city=Paris&days=2"
```

### Test Caching
```bash
# First request (slow, fetches from APIs)
time curl "http://localhost:8000/trip?city=London&days=3"

# Second request (fast, from cache)
time curl "http://localhost:8000/trip?city=London&days=3"
```

### Test Error Handling
```bash
# Invalid city name
curl "http://localhost:8000/trip?city=InvalidCityXYZ&days=3"

# Out of range days
curl "http://localhost:8000/trip?city=Rome&days=10"
```

## Configuration Options

All configuration is managed through environment variables (see `.env.example`):

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | (required) |
| `FOURSQUARE_API_KEY` | Foursquare API key | (required) |
| `REDIS_HOST` | Redis server hostname | localhost |
| `REDIS_PORT` | Redis server port | 6379 |
| `REDIS_DB` | Redis database number | 0 |
| `REDIS_PASSWORD` | Redis password (if any) | None |
| `CACHE_TTL` | Cache time-to-live in seconds | 3600 |
| `API_TIMEOUT` | API request timeout in seconds | 10 |

## Troubleshooting

### Redis Connection Errors
If Redis is not available, the app will log a warning and continue without caching:
```
WARNING - Redis connection failed. Caching disabled.
```

### API Key Issues
- Ensure your API keys are valid and have sufficient quota
- OpenWeatherMap free tier allows 60 calls/minute
- Foursquare has daily limits depending on your plan

### Geocoding Failures
If a city is not found, try:
- Using the full city name (e.g., "New York" instead of "NY")
- Including country (e.g., "Paris, France")
- Checking spelling

## Documentation

- **[REACT_UI_SETUP.md](REACT_UI_SETUP.md)** - Complete frontend development guide
- **[UI_GUIDE.md](UI_GUIDE.md)** - How to use the web interface
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture

## Future Enhancements

- [ ] Multi-turn conversations with context
- [ ] Save and export trip plans
- [ ] User authentication
- [ ] Rate limiting
- [ ] Add more travel APIs (hotels, flights)
- [ ] Map integration
- [ ] Multi-city trip planning
- [ ] Cost estimation
- [ ] Voice input support

## License

This project is created for educational and portfolio purposes.

## Author

Built with ❤️ as a demonstration of:
- API integration and orchestration
- Async Python programming
- Caching strategies
- Error handling and resilience
- Clean architecture and code organization

