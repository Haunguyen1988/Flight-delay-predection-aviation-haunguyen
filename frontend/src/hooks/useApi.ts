import { useState, useEffect, useCallback } from 'react';
import api from '../services/api';
import type { FlightStats, RouteDelay, WeatherDelay, TimeDelay } from '../types/flight';

// ── Generic fetch hook ─────────────────────────────────────
function useApi<T>(url: string, defaultValue: T) {
  const [data, setData] = useState<T>(defaultValue);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.get(url);
      if (res.data.success) {
        setData(res.data.data);
      } else {
        setError(res.data.message || 'Unknown error');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Connection failed');
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
  return useApi<any>(`/api/flights?${params.toString()}`, {
    flights: [],
    total: 0,
    page: 1,
    limit: 20,
    total_pages: 0,
  });
}

// ── Model Info ─────────────────────────────────────────────
export function useModelInfo() {
  return useApi<any>('/api/predict/model/info', { status: 'unknown' });
}

// ── Prediction (manual call) ───────────────────────────────
export function usePrediction() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const predict = async (data: {
    airline: string;
    origin: string;
    destination: string;
    departure_datetime: string;
    weather_condition?: string;
  }) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await api.post('/api/predict', data);
      if (res.data.success) {
        setResult(res.data.data);
      } else {
        setError(res.data.message || 'Prediction failed');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Prediction failed');
    } finally {
      setLoading(false);
    }
  };

  return { result, loading, error, predict };
}

// ── Upload CSV ─────────────────────────────────────────────
export function useUpload() {
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState<any>(null);
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
      const res = await api.post('/api/data/upload', formData, {
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
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  const generateSample = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await api.post('/api/data/generate-sample');
      if (res.data.success) {
        setResult(res.data.data);
      } else {
        setError(res.data.message);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  const trainModel = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.post('/api/predict/train');
      if (res.data.success) {
        setResult({ ...res.data.data, type: 'training' });
      } else {
        setError(res.data.message);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  return { progress, result, loading, error, upload, generateSample, trainModel };
}
