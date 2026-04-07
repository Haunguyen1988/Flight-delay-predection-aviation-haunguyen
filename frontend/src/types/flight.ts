export interface Flight {
  id: number;
  flight_number: string;
  airline_code: string;
  origin_airport: string;
  destination_airport: string;
  scheduled_departure: string;
  actual_departure: string;
  scheduled_arrival: string;
  actual_arrival: string;
  delay_minutes: number;
  delay_reason: string;
  distance: number;
  weather_condition: string;
  day_of_week: number;
  month: number;
  is_delayed: boolean;
}

export interface FlightStats {
  total_flights: number;
  delayed_count: number;
  delay_rate: number;
  avg_delay_minutes: number;
  ontime_rate: number;
}

export interface RouteDelay {
  route: string;
  origin: string;
  destination: string;
  total_flights: number;
  delayed_flights: number;
  delay_rate: number;
  avg_delay_minutes: number;
}

export interface WeatherDelay {
  weather: string;
  total: number;
  delayed: number;
  rate: number;
}

export interface TimeDelay {
  label: string;
  total: number;
  delayed: number;
  rate: number;
}

export interface PredictionRequest {
  airline: string;
  origin: string;
  destination: string;
  departure_datetime: string;
  weather_condition?: string;
}

export interface PredictionResult {
  delay_probability: number;
  estimated_delay_minutes: number;
  confidence: string;
  model_scores?: {
    xgboost: number;
    random_forest: number;
  };
}

export interface PredictionHistory {
  id: string;
  airline: string;
  origin: string;
  destination: string;
  datetime: string;
  result: PredictionResult;
  created_at: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message: string;
  timestamp?: string;
}

export interface PaginatedData<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}
