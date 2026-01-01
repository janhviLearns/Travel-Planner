"""
OpenAI Client for Natural Language Travel Planning
"""
import json
import logging
from typing import Optional, Dict, Any
from openai import AsyncOpenAI
from config import settings

logger = logging.getLogger(__name__)


class OpenAIClient:
    """Client for OpenAI API to handle natural language travel queries."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        self.client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        self.model = "gpt-4o-mini"  # Using GPT-4o-mini for cost efficiency
        
    async def parse_travel_query(self, user_query: str) -> Optional[Dict[str, Any]]:
        """
        Parse a natural language travel query into structured parameters.
        
        Args:
            user_query: User's natural language query
            
        Returns:
            Dictionary with parsed parameters (city, days) or None if parsing fails
        """
        if not self.client:
            logger.error("OpenAI client not initialized. Please set OPENAI_API_KEY.")
            return None
            
        try:
            logger.info(f"[OpenAI] Starting to parse query: '{user_query}'")
            system_prompt = """You are a travel query parser. Extract the city name and number of days from the user's query.
Return a JSON object with 'city' (string) and 'days' (integer, 1-5, default 3) keys.
If the query is not about travel planning, return {"error": "Not a travel query"}.

Examples:
- "Plan a 3-day trip to Paris" -> {"city": "Paris", "days": 3}
- "I want to visit Tokyo for 5 days" -> {"city": "Tokyo", "days": 5}
- "Tell me about Rome" -> {"city": "Rome", "days": 3}
- "What's the weather in London?" -> {"city": "London", "days": 3}
- "What's the capital of France?" -> {"error": "Not a travel query"}"""

            logger.info("[OpenAI] Sending request to OpenAI API for query parsing...")
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info(f"[OpenAI] Successfully parsed query: {user_query} -> {result}")
            return result
            
        except Exception as e:
            logger.error(f"[OpenAI] Error parsing travel query: {e}", exc_info=True)
            return None
    
    async def generate_travel_response(
        self, 
        user_query: str, 
        trip_data: Dict[str, Any]
    ) -> str:
        """
        Generate a natural language response about the trip.
        
        Args:
            user_query: Original user query
            trip_data: Structured trip data from the API
            
        Returns:
            Natural language response as a string
        """
        if not self.client:
            logger.error("[OpenAI] OpenAI client not initialized. Please set OPENAI_API_KEY.")
            return "I'm unable to process your request. Please check the OpenAI API configuration."
            
        try:
            logger.info(f"[OpenAI] Generating natural language response for query: '{user_query}'")
            # Format trip data for the LLM
            city = trip_data.get("city", "Unknown")
            country = trip_data.get("country", "")
            days = trip_data.get("days", 0)
            weather = trip_data.get("weather_forecast", [])
            attractions = trip_data.get("top_attractions", [])
            
            logger.info(f"[OpenAI] Trip data summary - City: {city}, Days: {days}, Weather items: {len(weather)}, Attractions: {len(attractions)}")
            
            # Create a concise data summary
            data_summary = f"""
City: {city}, {country}
Days: {days}

Weather Forecast:
"""
            for day in weather[:3]:  # Limit to first 3 days
                data_summary += f"- {day.get('date', 'N/A')}: {day.get('temp_avg', 'N/A')}°C, {day.get('description', 'N/A')}\n"
            
            data_summary += "\nTop Attractions:\n"
            for i, attr in enumerate(attractions[:5], 1):  # Limit to top 5
                data_summary += f"{i}. {attr.get('name', 'N/A')}"
                if attr.get('distance'):
                    data_summary += f" ({attr.get('distance')}km away)"
                data_summary += "\n"
            
            system_prompt = """You are a friendly and knowledgeable travel assistant. 
Based on the travel data provided, give a helpful, conversational response to the user's query.
Be concise but informative. Highlight key weather patterns and must-visit attractions.
Use a warm, encouraging tone. Keep responses to 3-4 paragraphs maximum."""

            logger.info("[OpenAI] Sending request to OpenAI API for response generation...")
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"User Query: {user_query}\n\nTravel Data:\n{data_summary}"}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            generated_response = response.choices[0].message.content.strip()
            logger.info(f"[OpenAI] Successfully generated response (length: {len(generated_response)} chars)")
            logger.debug(f"[OpenAI] Response preview: {generated_response[:200]}...")
            return generated_response
            
        except Exception as e:
            logger.error(f"[OpenAI] Error generating travel response: {e}", exc_info=True)
            return f"I found information about {trip_data.get('city', 'your destination')}, but I'm having trouble formatting a response. Please try again."

