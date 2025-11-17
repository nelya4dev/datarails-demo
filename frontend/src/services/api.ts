import axios from 'axios';
import type { AxiosError, InternalAxiosRequestConfig } from 'axios';
import { logRequest, logResponse, logError } from '@/utils/logger';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - log outgoing requests
api.interceptors.request.use(
  (config) => {
    // Store request start time for duration tracking
    (config as InternalAxiosRequestConfig & { metadata?: { startTime: number } }).metadata = {
      startTime: Date.now(),
    };

    // Log request
    logRequest(
      config.method?.toUpperCase() || 'GET',
      config.url || '',
      config.data
    );

    // Add auth token here if needed in future
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - log responses and errors
api.interceptors.response.use(
  (response) => {
    // Calculate request duration
    const startTime = (response.config as InternalAxiosRequestConfig & { metadata?: { startTime: number } }).metadata?.startTime;
    const duration = startTime ? Date.now() - startTime : 0;

    // Log successful response
    logResponse(
      response.config.method?.toUpperCase() || 'GET',
      response.config.url || '',
      response.status,
      duration
    );

    return response;
  },
  (error: AxiosError) => {
    // Calculate request duration
    const startTime = (error.config as InternalAxiosRequestConfig & { metadata?: { startTime: number } })?.metadata?.startTime;
    const duration = startTime ? Date.now() - startTime : undefined;

    const method = error.config?.method?.toUpperCase() || 'REQUEST';
    const url = error.config?.url || 'unknown';

    // Handle common errors
    if (error.response) {
      // Server responded with error status
      const status = error.response.status;
      const data = error.response.data as { message?: string; detail?: string } | undefined;
      const message = data?.message || data?.detail || 'An error occurred';

      logError(method, url, status, message, duration);

      return Promise.reject(new Error(message));
    } else if (error.request) {
      // Request made but no response
      const message = 'No response from server. Please check your connection.';

      logError(method, url, null, message, duration);

      return Promise.reject(new Error(message));
    } else {
      // Something else happened
      logError(method, url, null, error.message || 'Request failed', duration);

      return Promise.reject(error);
    }
  }
);

export default api;
