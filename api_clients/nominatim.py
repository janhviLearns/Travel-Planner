import httpx
from typing import Optional, Dict
from config import settings
import logging

logger = logging.getLogger(__name__)


class NominatimClient:
    """Client for OpenStreetMap Nominatim geocoding API."""
    
    def __init__(self):
        self.base_url = settings.nominatim_base_url
        self.timeout = settings.api_timeout
        
    async def geocode_city(self, city: str) -> Optional[Dict]:
        """
        Geocode a city name to coordinates.
        
        Args:
            city: City name to geocode
            
        Returns:
            Dictionary with lat, lon, and display_name, or None if failed
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/search",
                    params={
                        "q": city,
                        "format": "json",
                        "limit": 1,
                        "addressdetails": 1
                    },
                    headers={
                        "User-Agent": "TravelPlannerAPI/1.0"
                    },
                    timeout=self.timeout
                )
                response.raise_for_status()
                data = response.json()
                
                if not data:
                    logger.warning(f"No geocoding results found for city: {city}")
                    return None
                
                result = data[0]
                return {
                    "lat": float(result["lat"]),
                    "lon": float(result["lon"]),
                    "display_name": result.get("display_name", ""),
                    "country": result.get("address", {}).get("country", "")
                }
                
        except httpx.TimeoutException:
            logger.error(f"Timeout while geocoding city: {city}")
            return None
        except httpx.HTTPError as e:
            logger.error(f"HTTP error while geocoding city {city}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while geocoding city {city}: {e}")
            return None

