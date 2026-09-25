import axios from 'axios';

let rawBaseUrl = import.meta.env.VITE_API_BASE_URL || import.meta.env.VITE_API_URL || '/api';
rawBaseUrl = rawBaseUrl.trim();
if (rawBaseUrl.endsWith('/')) {
  rawBaseUrl = rawBaseUrl.slice(0, -1);
}
// If an absolute domain was provided without /api (e.g. https://my-backend.onrender.com), append /api
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

export default api;

