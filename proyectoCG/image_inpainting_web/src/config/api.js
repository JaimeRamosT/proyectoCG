// API Configuration
const API_CONFIG = {
  // Development API (local)
  development: {
    baseURL: 'http://localhost:8000',
  },
  // Production API (Render or other deployment)
  production: {
    baseURL: 'https://rdb-image-inpainting-model-1-0.onrender.com',
  }
};

// Automatically detect environment
const ENV = import.meta.env.MODE || 'development';

// Export the current configuration
export const API_BASE_URL = API_CONFIG[ENV]?.baseURL || API_CONFIG.development.baseURL;

export default {
  baseURL: API_BASE_URL,
  endpoints: {
    upload: '/upload/',
  }
};
