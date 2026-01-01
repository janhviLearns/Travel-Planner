import httpx
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from config import settings
import logging

logger = logging.getLogger(__name__)


class OpenWeatherClient:
    """Client for OpenWeatherMap API."""
    
    def __init__(self):
        self.base_url = settings.openweather_base_url
        self.api_key = settings.openweather_api_key
        self.timeout = settings.api_timeout
        
    async def get_forecast(self, lat: float, lon: float, days: int) -> Optional[List[Dict]]:
        """
        Get weather forecast for specified coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
            days: Number of days for forecast
            
        Returns:
            List of daily weather data, or None if failed
        """
        if not self.api_key:
            logger.error("OpenWeatherMap API key not configured")
            return None
            
        try:
            async with httpx.AsyncClient() as client:
                # Use 5-day forecast API
                response = await client.get(
                    f"{self.base_url}/forecast",
                    params={
                        "lat": lat,
                        "lon": lon,
                        "appid": self.api_key,
                        "units": "metric"
                    },
                    timeout=self.timeout
                )
                response.raise_for_status()
                data = response.json()
                
                # Process forecast data into daily summaries
                daily_forecasts = self._process_forecast(data, days)
                return daily_forecasts
                
        except httpx.TimeoutException:
            logger.error(f"Timeout while fetching weather for lat={lat}, lon={lon}")
            return None
        except httpx.HTTPError as e:
            logger.error(f"HTTP error while fetching weather: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while fetching weather: {e}")
            return None
    
    def _process_forecast(self, data: Dict, days: int) -> List[Dict]:
        """Process raw forecast data into daily summaries."""
        daily_data = {}
        
        for item in data.get("list", []):
            dt = datetime.fromtimestamp(item["dt"])
            date_key = dt.strftime("%Y-%m-%d")
            
            if date_key not in daily_data:
                daily_data[date_key] = {
                    "date": date_key,
                    "temps": [],
                    "descriptions": [],
                    "humidity": [],
                    "wind_speed": []
                }
            
            daily_data[date_key]["temps"].append(item["main"]["temp"])
            daily_data[date_key]["descriptions"].append(
                item["weather"][0]["description"]
            )
            daily_data[date_key]["humidity"].append(item["main"]["humidity"])
            daily_data[date_key]["wind_speed"].append(item["wind"]["speed"])
        
        # Aggregate daily data
        result = []
        for date_key in sorted(daily_data.keys())[:days]:
            day = daily_data[date_key]
            temps = day["temps"]
            
            result.append({
                "date": day["date"],
                "temp_avg": round(sum(temps) / len(temps), 1),
                "temp_min": round(min(temps), 1),
                "temp_max": round(max(temps), 1),
                "description": max(set(day["descriptions"]), 
                                 key=day["descriptions"].count),
                "humidity": int(sum(day["humidity"]) / len(day["humidity"])),
                "wind_speed": round(sum(day["wind_speed"]) / len(day["wind_speed"]), 1)
            })
        
        return result

