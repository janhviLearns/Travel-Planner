import asyncio
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import logging
from pathlib import Path

from models import (
    TripResponse, WeatherDay, Attraction, TravelNotes, 
    DistanceCluster, Coordinates, ChatRequest, ChatResponse
)
from api_clients.nominatim import NominatimClient
from api_clients.openweather import OpenWeatherClient
from api_clients.foursquare import FoursquareClient
from api_clients.openai_client import OpenAIClient
from cache import cache_manager
from config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Multi-Source Travel Planner API",
    description="Aggregate travel information from multiple sources with AI-powered natural language interface",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize API clients
nominatim_client = NominatimClient()
weather_client = OpenWeatherClient()
foursquare_client = FoursquareClient()
openai_client = OpenAIClient()

# Setup static files directory
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)


@app.get("/", include_in_schema=False)
async def root():
    """Redirect to UI."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/ui")


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "message": "Multi-Source Travel Planner API",
        "version": "2.0.0",
        "status": "online"
    }


@app.get("/trip", response_model=TripResponse, tags=["Travel"])
async def get_trip_plan(
    city: str = Query(..., description="City name (e.g., Rome, Paris, Tokyo)"),
    days: int = Query(3, ge=1, le=5, description="Number of days (1-5)")
):
    """
    Get a comprehensive travel plan for a city.
    
    Returns:
    - Daily weather forecast
    - Top nearby attractions
    - Travel notes with distance clustering
    
    This endpoint showcases:
    - Parallel API calls to multiple services
    - Response normalization
    - Timeout and fallback handling
    - City-level caching with Redis
    """
    logger.info(f"[TRIP] Trip request received: city={city}, days={days}")
    
    # Check cache first
    logger.info(f"[TRIP] Checking cache for {city}...")
    cached_data = cache_manager.get(city, days)
    if cached_data:
        logger.info(f"[TRIP] Cache HIT - Returning cached data for {city}")
        cached_data["cached"] = True
        return TripResponse(**cached_data)
    
    logger.info(f"[TRIP] Cache MISS - Fetching fresh data for {city}")
    
    # Step 1: Geocode the city (this must complete first)
    logger.info(f"[TRIP] Step 1: Geocoding city '{city}'...")
    geocode_result = await nominatim_client.geocode_city(city)
    if not geocode_result:
        logger.error(f"[TRIP] Geocoding failed - city '{city}' not found")
        raise HTTPException(
            status_code=404,
            detail=f"City '{city}' not found. Please check the spelling and try again."
        )
    
    lat = geocode_result["lat"]
    lon = geocode_result["lon"]
    country = geocode_result.get("country", "")
    
    logger.info(f"[TRIP] Geocoded {city}: lat={lat}, lon={lon}, country={country}")
    
    # Step 2: Fetch weather and attractions in parallel
    logger.info(f"[TRIP] Step 2: Fetching weather and attractions in parallel...")
    weather_task = weather_client.get_forecast(lat, lon, days)
    attractions_task = foursquare_client.get_attractions(lat, lon, limit=20)
    
    # Wait for both API calls to complete
    weather_data, attractions_data = await asyncio.gather(
        weather_task,
        attractions_task,
        return_exceptions=True
    )
    logger.info(f"[TRIP] Parallel API calls completed")
    
    # Step 3: Handle results with fallbacks
    logger.info(f"[TRIP] Step 3: Processing API results...")
    weather_forecast = []
    if isinstance(weather_data, Exception):
        logger.error(f"[TRIP] Weather API failed: {weather_data}")
        weather_forecast = _get_fallback_weather(days)
    elif weather_data:
        weather_forecast = [WeatherDay(**day) for day in weather_data]
        logger.info(f"[TRIP] Weather data processed: {len(weather_forecast)} days")
    else:
        logger.warning(f"[TRIP] No weather data returned, using fallback")
        weather_forecast = _get_fallback_weather(days)
    
    top_attractions = []
    if isinstance(attractions_data, Exception):
        logger.error(f"[TRIP] Attractions API failed: {attractions_data}")
        top_attractions = _get_fallback_attractions()
    elif attractions_data:
        top_attractions = [Attraction(**attr) for attr in attractions_data[:10]]
        logger.info(f"[TRIP] Attractions data processed: {len(top_attractions)} attractions")
    else:
        logger.warning(f"[TRIP] No attractions data returned, using fallback")
        top_attractions = _get_fallback_attractions()
    
    # Step 4: Generate travel notes with distance clustering
    logger.info(f"[TRIP] Step 4: Generating travel notes...")
    travel_notes = _generate_travel_notes(attractions_data if attractions_data and not isinstance(attractions_data, Exception) else [])
    
    # Step 5: Build response
    logger.info(f"[TRIP] Step 5: Building response...")
    response_data = {
        "city": city,
        "country": country,
        "coordinates": Coordinates(lat=lat, lon=lon).model_dump(),
        "days": days,
        "weather_forecast": [w.model_dump() for w in weather_forecast],
        "top_attractions": [a.model_dump() for a in top_attractions],
        "travel_notes": travel_notes.model_dump(),
        "cached": False
    }
    
    # Cache the response
    logger.info(f"[TRIP] Caching response data for {city}...")
    cache_success = cache_manager.set(city, days, response_data)
    logger.info(f"[TRIP] Cache save {'successful' if cache_success else 'failed'}")
    
    logger.info(f"[TRIP] Successfully generated trip plan for {city}")
    trip_response = TripResponse(**response_data)
    logger.info(f"[TRIP] Response object created successfully")
    return trip_response


def _get_fallback_weather(days: int) -> list[WeatherDay]:
    """Provide fallback weather data when API fails."""
    logger.warning("Using fallback weather data")
    fallback = []
    for i in range(days):
        fallback.append(WeatherDay(
            date=f"Day {i+1}",
            temp_avg=20.0,
            temp_min=15.0,
            temp_max=25.0,
            description="Weather data unavailable",
            humidity=50,
            wind_speed=5.0
        ))
    return fallback


def _get_fallback_attractions() -> list[Attraction]:
    """Provide fallback attraction data when API fails."""
    logger.warning("Using fallback attractions data")
    return [
        Attraction(
            name="Attractions data unavailable",
            category="Information",
            distance=None,
            address="Please check API configuration",
            rating=None
        )
    ]


def _generate_travel_notes(attractions: list) -> TravelNotes:
    """
    Generate travel notes with distance clustering.
    
    Args:
        attractions: List of attraction dictionaries
        
    Returns:
        TravelNotes object with distance clusters
    """
    if not attractions:
        return TravelNotes(
            distance_clusters=[],
            total_attractions=0
        )
    
    # Define distance thresholds (in km)
    thresholds = [
        (2, "Within 2km (Walking distance)"),
        (5, "Within 5km (Short trip)"),
        (10, "Within 10km (Moderate trip)"),
        (float('inf'), "Beyond 10km")
    ]
    
    clusters = {name: [] for _, name in thresholds}
    
    for attraction in attractions:
        distance = attraction.get("distance")
        if distance is None:
            continue
        
        for threshold, cluster_name in thresholds:
            if distance <= threshold:
                clusters[cluster_name].append(attraction["name"])
                break
    
    distance_clusters = []
    for _, cluster_name in thresholds:
        cluster_attractions = clusters[cluster_name]
        if cluster_attractions:
            distance_clusters.append(DistanceCluster(
                cluster_name=cluster_name,
                count=len(cluster_attractions),
                attractions=cluster_attractions[:5]  # Limit to 5 per cluster
            ))
    
    return TravelNotes(
        distance_clusters=distance_clusters,
        total_attractions=len(attractions)
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.post("/chat", response_model=ChatResponse, tags=["AI Chat"])
async def chat_with_ai(request: ChatRequest):
    """
    Natural language interface for travel planning using OpenAI.
    
    This endpoint:
    - Parses natural language queries using GPT-4
    - Fetches relevant travel data
    - Generates human-friendly responses
    
    Examples:
    - "Plan a 3-day trip to Paris"
    - "What's the weather like in Tokyo?"
    - "Tell me about attractions in Rome"
    """
    logger.info(f"[CHAT] ===== NEW CHAT REQUEST =====")
    logger.info(f"[CHAT] User query: '{request.query}'")
    
    try:
        # Parse the user query to extract parameters
        logger.info("[CHAT] Step 1: Parsing user query with OpenAI...")
        parsed = await openai_client.parse_travel_query(request.query)
        logger.info(f"[CHAT] Parse result: {parsed}")
        
        if not parsed:
            logger.warning("[CHAT] Failed to parse query - returning error response")
            return ChatResponse(
                query=request.query,
                response="I'm having trouble understanding your request. Could you please rephrase it?",
                error="Failed to parse query"
            )
        
        # Check if it's an error (not a travel query)
        if "error" in parsed:
            logger.info(f"[CHAT] Query not recognized as travel query: {parsed['error']}")
            return ChatResponse(
                query=request.query,
                response="I'm a travel planning assistant. Please ask me about destinations, weather, or attractions in cities around the world!",
                error=parsed["error"]
            )
        
        # Extract city and days
        city = parsed.get("city")
        days = parsed.get("days", 3)
        logger.info(f"[CHAT] Extracted parameters - City: {city}, Days: {days}")
        
        if not city:
            logger.warning("[CHAT] No city found in parsed query")
            return ChatResponse(
                query=request.query,
                response="I couldn't identify a city in your query. Which city would you like to know about?",
                error="No city specified"
            )
        
        # Fetch trip data (reusing existing endpoint logic)
        logger.info(f"[CHAT] Step 2: Fetching trip data for {city}...")
        try:
            trip_data = await get_trip_plan(city=city, days=days)
            trip_dict = trip_data.model_dump()
            logger.info(f"[CHAT] Successfully fetched trip data for {city}")
        except HTTPException as e:
            logger.error(f"[CHAT] Failed to fetch trip data: {e.detail}")
            return ChatResponse(
                query=request.query,
                response=f"I couldn't find information about {city}. Please check the city name and try again.",
                error=e.detail
            )
        
        # Generate natural language response
        logger.info("[CHAT] Step 3: Generating natural language response with OpenAI...")
        nl_response = await openai_client.generate_travel_response(
            user_query=request.query,
            trip_data=trip_dict
        )
        logger.info(f"[CHAT] Generated response length: {len(nl_response)} characters")
        
        chat_response = ChatResponse(
            query=request.query,
            response=nl_response,
            trip_data=trip_data
        )
        
        logger.info("[CHAT] ===== CHAT REQUEST COMPLETED SUCCESSFULLY =====")
        logger.info(f"[CHAT] Response preview: {nl_response[:150]}...")
        return chat_response
        
    except Exception as e:
        logger.error(f"[CHAT] ===== CHAT REQUEST FAILED =====")
        logger.error(f"[CHAT] Unexpected error in chat endpoint: {e}", exc_info=True)
        return ChatResponse(
            query=request.query,
            response="I encountered an error processing your request. Please try again.",
            error=str(e)
        )


# Mount static files for the UI (assets like JS, CSS, images)
if static_dir.exists():
    app.mount("/assets", StaticFiles(directory=str(static_dir / "assets")), name="assets")


@app.get("/ui", include_in_schema=False)
async def serve_ui():
    """Serve the React UI."""
    ui_file = static_dir / "index.html"
    if ui_file.exists():
        return FileResponse(ui_file)
    return JSONResponse(
        status_code=404,
        content={
            "message": "UI not found. Please build the frontend first: cd frontend && npm install && npm run build"
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "An unexpected error occurred. Please try again later.",
            "status_code": 500
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

