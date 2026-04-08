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
  risk_band: string;
  severity_band: string;
  recommendations: string[];
  explanations: ExplanationItem[];
  error?: string;
  model_scores?: {
    xgboost: number;
    random_forest: number;
  };
}

export interface PredictionHistoryItem {
  id: number;
  airline: string;
  origin: string;
  destination: string;
  departure_datetime: string | null;
  delay_probability: number;
  estimated_delay_minutes: number;
  risk_band: string;
  severity_band: string;
  confidence: string;
  created_at: string | null;
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

export type PredictionHistoryResponse = PaginatedData<PredictionHistoryItem>;

export interface FlightListItem {
  id: number;
  flight_number: string;
  airline_code: string;
  origin: string;
  destination: string;
  scheduled_departure: string | null;
  weather: string | null;
  delay_minutes: number;
  is_delayed: boolean;
}

export interface FlightListResponse {
  flights: FlightListItem[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

export interface ModelMetricSummary {
  accuracy?: number | null;
  precision?: number | null;
  recall?: number | null;
  f1_score?: number | null;
}

export interface FeatureImportanceItem {
  feature: string;
  importance: number;
}

export interface ExplanationItem {
  factor: string;
  impact: string;
  message: string;
}

export interface ModelInfo {
  status: string;
  xgboost?: ModelMetricSummary;
  random_forest?: ModelMetricSummary;
  ensemble?: ModelMetricSummary;
  feature_importance?: FeatureImportanceItem[];
  dataset_size?: number | null;
  train_size?: number | null;
  test_size?: number | null;
  trained_at?: string | null;
  accuracy?: number | null;
  precision?: number | null;
  recall?: number | null;
  f1_score?: number | null;
  features?: string[];
}

export interface UploadActionResult {
  filename?: string;
  rows_imported?: number;
  total_rows?: number;
  duration_seconds?: number;
  file_path?: string;
  type?: 'training';
  ensemble?: ModelMetricSummary;
}
