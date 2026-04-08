import axios from 'axios';
import { useState, useEffect, useCallback } from 'react';
import api from '../services/api';
import type {
  ApiResponse,
  FlightListResponse,
  FlightStats,
  ModelInfo,
  PredictionHistoryResponse,
  PredictionRequest,
  PredictionResult,
  RouteDelay,
  TimeDelay,
  UploadActionResult,
  WeatherDelay,
} from '../types/flight';

function getErrorMessage(error: unknown, fallback: string) {
  if (axios.isAxiosError(error)) {
    const data = error.response?.data as { detail?: string; message?: string } | undefined;
    return data?.detail ?? data?.message ?? error.message ?? fallback;
  }

  if (error instanceof Error) {
    return error.message;
  }

  return fallback;
}

// ── Generic fetch hook ─────────────────────────────────────
function useApi<T>(url: string, defaultValue: T) {
  const [data, setData] = useState<T>(defaultValue);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.get<ApiResponse<T>>(url);
      if (res.data.success) {
        setData(res.data.data);
      } else {
        setError(res.data.message || 'Unknown error');
      }
    } catch (error: unknown) {
      setError(getErrorMessage(error, 'Connection failed'));
    } finally {
      setLoading(false);
    }
  }, [url]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}

// ── Dashboard Stats ────────────────────────────────────────
export function useFlightStats() {
  return useApi<FlightStats>('/api/flights/stats', {
    total_flights: 0,
    delayed_count: 0,
    delay_rate: 0,
    avg_delay_minutes: 0,
    ontime_rate: 0,
  });
}

// ── Route Delays ───────────────────────────────────────────
export function useRouteDelays(top = 10) {
  return useApi<RouteDelay[]>(`/api/flights/by-route?top=${top}`, []);
}

// ── Weather Delays ─────────────────────────────────────────
export function useWeatherDelays() {
  return useApi<WeatherDelay[]>('/api/flights/by-weather', []);
}

// ── Time Delays ────────────────────────────────────────────
export function useTimeDelays(group: 'hour' | 'day' | 'month' = 'month') {
  return useApi<TimeDelay[]>(`/api/flights/by-time?group=${group}`, []);
}

// ── Flight List ────────────────────────────────────────────
export function useFlightList(page = 1, limit = 20, filters: Record<string, string> = {}) {
  const params = new URLSearchParams({ page: String(page), limit: String(limit) });
  Object.entries(filters).forEach(([k, v]) => {
    if (v) params.set(k, v);
  });
  return useApi<FlightListResponse>(`/api/flights?${params.toString()}`, {
    flights: [],
    total: 0,
    page: 1,
    limit: 20,
    total_pages: 0,
  });
}

// ── Model Info ─────────────────────────────────────────────
export function useModelInfo() {
  return useApi<ModelInfo>('/api/predict/model/info', { status: 'unknown' });
}
export function usePredictionHistory(page = 1, limit = 5, filters: Record<string, string> = {}) {
  const params = new URLSearchParams({ page: String(page), limit: String(limit) });
  Object.entries(filters).forEach(([key, value]) => {
    if (value) params.set(key, value);
  });

  return useApi<PredictionHistoryResponse>(`/api/predict/history?${params.toString()}`, {
    items: [],
    total: 0,
    page,
    limit,
    total_pages: 0,
  });
}

// ── Prediction (manual call) ───────────────────────────────
export function usePrediction() {
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const predict = async (data: PredictionRequest) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await api.post<ApiResponse<PredictionResult>>('/api/predict', data);
      if (res.data.success) {
        setResult(res.data.data);
      } else {
        setError(res.data.message || 'Prediction failed');
      }
    } catch (error: unknown) {
      setError(getErrorMessage(error, 'Prediction failed'));
    } finally {
      setLoading(false);
    }
  };

  return { result, loading, error, predict };
}

// ── Upload CSV ─────────────────────────────────────────────
export function useUpload() {
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState<UploadActionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const upload = async (file: File) => {
    setLoading(true);
    setError(null);
    setResult(null);
    setProgress(0);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await api.post<ApiResponse<UploadActionResult>>('/api/data/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 300000, // 5 min for large files
        onUploadProgress: (e) => {
          if (e.total) setProgress(Math.round((e.loaded / e.total) * 100));
        },
      });

      if (res.data.success) {
        setResult(res.data.data);
      } else {
        setError(res.data.message || 'Upload failed');
      }
    } catch (error: unknown) {
      setError(getErrorMessage(error, 'Upload failed'));
    } finally {
      setLoading(false);
    }
  };

  const generateSample = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await api.post<ApiResponse<UploadActionResult>>('/api/data/generate-sample');
      if (res.data.success) {
        setResult(res.data.data);
      } else {
        setError(res.data.message);
      }
    } catch (error: unknown) {
      setError(getErrorMessage(error, 'Sample generation failed'));
    } finally {
      setLoading(false);
    }
  };

  const trainModel = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.post<ApiResponse<UploadActionResult>>('/api/predict/train');
      if (res.data.success) {
        setResult({ ...res.data.data, type: 'training' });
      } else {
        setError(res.data.message);
      }
    } catch (error: unknown) {
      setError(getErrorMessage(error, 'Training failed'));
    } finally {
      setLoading(false);
    }
  };

  return { progress, result, loading, error, upload, generateSample, trainModel };
}
