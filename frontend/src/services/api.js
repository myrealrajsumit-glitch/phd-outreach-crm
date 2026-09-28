import axios from 'axios';

let rawBaseUrl = import.meta.env.VITE_API_BASE_URL || import.meta.env.VITE_API_URL || '/api';
rawBaseUrl = rawBaseUrl.trim();
if (rawBaseUrl.endsWith('/')) {
  rawBaseUrl = rawBaseUrl.slice(0, -1);
}
// If an absolute domain was provided without /api (e.g. https://my-backend.domain.com), append /api
const baseURL = (!rawBaseUrl.startsWith('/') && !rawBaseUrl.endsWith('/api'))
  ? `${rawBaseUrl}/api`
  : rawBaseUrl;

const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor: attach bearer token if user is logged in
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token') || localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor: reject HTML responses (e.g. Vercel SPA rewrites when backend is offline or unconfigured)
api.interceptors.response.use(
  (response) => {
    if (typeof response.data === 'string' && (response.data.includes('<!DOCTYPE') || response.data.includes('<html'))) {
      return Promise.reject(new Error("Backend API unavailable. Received HTML response instead of JSON."));
    }
    return response;
  },
  (error) => Promise.reject(error)
);

export default api;

