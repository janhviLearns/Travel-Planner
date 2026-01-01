from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    openweather_api_key: str = ""
    foursquare_api_key: str = ""
    openai_api_key: str = ""
    
    # Redis Configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None
    
    # Cache TTL (in seconds)
    cache_ttl: int = 3600  # 1 hour
    
    # API Timeouts (in seconds)
    api_timeout: int = 10
    
    # API URLs
    openweather_base_url: str = "https://api.openweathermap.org/data/2.5"
    nominatim_base_url: str = "https://nominatim.openstreetmap.org"
    foursquare_base_url: str = "https://places-api.foursquare.com"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

