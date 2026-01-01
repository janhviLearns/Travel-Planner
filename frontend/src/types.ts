export interface ChatMessage {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
}

export interface ChatRequest {
  query: string;
}

export interface TripData {
  city: string;
  country?: string;
  coordinates: {
    lat: number;
    lon: number;
  };
  days: number;
  weather_forecast: WeatherDay[];
  top_attractions: Attraction[];
  travel_notes: TravelNotes;
  cached: boolean;
}

export interface WeatherDay {
  date: string;
  temp_avg: number;
  temp_min: number;
  temp_max: number;
  description: string;
  humidity: number;
  wind_speed: number;
}

export interface Attraction {
  name: string;
  category: string;
  distance?: number;
  address?: string;
  rating?: number;
}

export interface TravelNotes {
  distance_clusters: DistanceCluster[];
  total_attractions: number;
}

export interface DistanceCluster {
  cluster_name: string;
  count: number;
  attractions: string[];
}

export interface ChatResponse {
  query: string;
  response: string;
  trip_data?: TripData;
  error?: string;
}

