import httpx
from typing import Optional, List, Dict
from config import settings
import logging

logger = logging.getLogger(__name__)


class FoursquareClient:
    """Client for Foursquare Places API."""
    
    def __init__(self):
        self.base_url = settings.foursquare_base_url
        self.api_key = settings.foursquare_api_key
        self.timeout = settings.api_timeout
        
    async def get_attractions(self, lat: float, lon: float, limit: int = 20) -> Optional[List[Dict]]:
        """
        Get attractions/points of interest near coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
            limit: Maximum number of results
            
        Returns:
            List of attractions, or None if failed
        """
        if not self.api_key:
            logger.error("Foursquare API key not configured")
            return None
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/places/search",
                    params={
                        "ll": f"{lat},{lon}",
                        "limit": limit
                    },
                    headers={
                        "X-Places-Api-Version": "2025-06-17",
                        "Accept": "application/json",
                        "Authorization": f"Bearer {self.api_key}"
                    },
                    timeout=self.timeout
                )
                response.raise_for_status()
                data = response.json()
                
                attractions = self._process_places(data, lat, lon)
                return attractions
                
        except httpx.TimeoutException:
            logger.error(f"Timeout while fetching attractions for lat={lat}, lon={lon}")
            return None
        except httpx.HTTPError as e:
            logger.error(f"HTTP error while fetching attractions: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while fetching attractions: {e}")
            return None
    
    def _process_places(self, data: Dict, origin_lat: float, origin_lon: float) -> List[Dict]:
        """Process Foursquare Places API response into simplified attraction format."""
        attractions = []
        
        for place in data.get("results", []):
            # Get coordinates
            geocode = place.get("geocodes", {}).get("main", {})
            lat = geocode.get("latitude")
            lon = geocode.get("longitude")
            
            # Calculate distance from origin
            distance = None
            if lat and lon:
                distance = self._calculate_distance(
                    origin_lat, origin_lon, lat, lon
                )
            
            # Get category
            categories = place.get("categories", [])
            category = categories[0].get("name") if categories else "Attraction"
            
            # Get address
            location = place.get("location", {})
            address = location.get("formatted_address", "")
            
            attractions.append({
                "name": place.get("name", "Unknown"),
                "category": category,
                "distance": distance,
                "address": address,
                "rating": None
            })
        
        # Sort by distance
        attractions.sort(key=lambda x: x["distance"] if x["distance"] is not None else float('inf'))
        
        return attractions
    
    @staticmethod
    def _calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points using Haversine formula.
        
        Returns:
            Distance in kilometers
        """
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = radians(lat1)
        lat2_rad = radians(lat2)
        delta_lat = radians(lat2 - lat1)
        delta_lon = radians(lon2 - lon1)
        
        a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        distance = R * c
        return round(distance, 2)

