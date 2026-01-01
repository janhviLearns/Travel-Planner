import redis
import json
from typing import Optional, Any
from config import settings
import logging

logger = logging.getLogger(__name__)


class CacheManager:
    """Redis cache manager for API responses."""
    
    def __init__(self):
        """Initialize Redis connection."""
        try:
            self.redis_client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                password=settings.redis_password if settings.redis_password else None,
                decode_responses=True,
                socket_connect_timeout=5
            )
            # Test connection
            self.redis_client.ping()
            logger.info("Redis connection established")
            self.enabled = True
        except (redis.ConnectionError, redis.TimeoutError) as e:
            logger.warning(f"Redis connection failed: {e}. Caching disabled.")
            self.enabled = False
        except Exception as e:
            logger.warning(f"Unexpected error connecting to Redis: {e}. Caching disabled.")
            self.enabled = False
    
    def _generate_key(self, city: str, days: int) -> str:
        """Generate cache key for city and days."""
        # Normalize city name (lowercase, strip whitespace)
        normalized_city = city.lower().strip()
        return f"trip:{normalized_city}:{days}"
    
    def get(self, city: str, days: int) -> Optional[dict]:
        """
        Get cached trip data.
        
        Args:
            city: City name
            days: Number of days
            
        Returns:
            Cached data dictionary or None if not found
        """
        if not self.enabled:
            return None
        
        try:
            key = self._generate_key(city, days)
            cached_data = self.redis_client.get(key)
            
            if cached_data:
                logger.info(f"Cache hit for key: {key}")
                return json.loads(cached_data)
            
            logger.info(f"Cache miss for key: {key}")
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving from cache: {e}")
            return None
    
    def set(self, city: str, days: int, data: dict) -> bool:
        """
        Set trip data in cache.
        
        Args:
            city: City name
            days: Number of days
            data: Data to cache
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            key = self._generate_key(city, days)
            serialized_data = json.dumps(data)
            
            self.redis_client.setex(
                key,
                settings.cache_ttl,
                serialized_data
            )
            
            logger.info(f"Cached data for key: {key} (TTL: {settings.cache_ttl}s)")
            return True
            
        except Exception as e:
            logger.error(f"Error setting cache: {e}")
            return False
    
    def delete(self, city: str, days: int) -> bool:
        """
        Delete cached trip data.
        
        Args:
            city: City name
            days: Number of days
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            key = self._generate_key(city, days)
            self.redis_client.delete(key)
            logger.info(f"Deleted cache for key: {key}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting from cache: {e}")
            return False
    
    def clear_all(self) -> bool:
        """Clear all cached trip data."""
        if not self.enabled:
            return False
        
        try:
            keys = self.redis_client.keys("trip:*")
            if keys:
                self.redis_client.delete(*keys)
                logger.info(f"Cleared {len(keys)} cached entries")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False


# Global cache instance
cache_manager = CacheManager()

