from pydantic import BaseModel, Field
from typing import List, Optional


class Coordinates(BaseModel):
    """Geographic coordinates."""
    lat: float
    lon: float


class WeatherDay(BaseModel):
    """Weather information for a single day."""
    date: str
    temp_avg: float = Field(description="Average temperature in Celsius")
    temp_min: float = Field(description="Minimum temperature in Celsius")
    temp_max: float = Field(description="Maximum temperature in Celsius")
    description: str = Field(description="Weather description")
    humidity: int = Field(description="Humidity percentage")
    wind_speed: float = Field(description="Wind speed in m/s")


class Attraction(BaseModel):
    """Point of interest / attraction."""
    name: str
    category: str
    distance: Optional[float] = Field(None, description="Distance from city center in km")
    address: Optional[str] = None
    rating: Optional[float] = None


class DistanceCluster(BaseModel):
    """Group of attractions by distance."""
    cluster_name: str = Field(description="e.g., 'Within 2km', 'Within 5km'")
    count: int
    attractions: List[str]


class TravelNotes(BaseModel):
    """Additional travel information."""
    distance_clusters: List[DistanceCluster]
    total_attractions: int


class TripResponse(BaseModel):
    """Main API response for trip planning."""
    city: str
    country: Optional[str] = None
    coordinates: Coordinates
    days: int
    weather_forecast: List[WeatherDay]
    top_attractions: List[Attraction]
    travel_notes: TravelNotes
    cached: bool = Field(default=False, description="Whether response was served from cache")


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    query: str = Field(description="Natural language travel query")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    query: str = Field(description="Original user query")
    response: str = Field(description="Natural language response")
    trip_data: Optional[TripResponse] = Field(None, description="Structured trip data if available")
    error: Optional[str] = Field(None, description="Error message if any")

