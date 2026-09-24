/**
 * Safely extracts a human-readable string message from an API error or exception.
 * Prevents React Error #31 (Objects are not valid as a React child) when FastAPI
 * returns validation error arrays or dictionaries.
 */
export function formatErrorMessage(err, fallback = "An unexpected error occurred.") {
  if (!err) return fallback;
  
  const detail = err.response?.data?.detail;
  
  if (typeof detail === 'string') {
    return detail;
  }
  
  if (Array.isArray(detail) && detail.length > 0) {
    return detail.map(d => {
      if (typeof d === 'string') return d;
      return d.msg || d.message || JSON.stringify(d);
    }).join('; ');
  }
  
  if (typeof detail === 'object' && detail !== null) {
    return detail.msg || detail.message || JSON.stringify(detail);
  }

  if (err.message && typeof err.message === 'string') {
    return err.message;
  }

  return fallback;
}
