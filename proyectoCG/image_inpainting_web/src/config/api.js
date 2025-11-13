// API Configuration
const API_CONFIG = {
  // Development API (local)
  development: {
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  },
  // Production API (from environment variable or fallback)
  production: {
    baseURL: import.meta.env.VITE_API_URL || 'https://rdb-image-inpainting-model-1-0.onrender.com',
  }
};

// Automatically detect environment
const ENV = import.meta.env.MODE || 'development';

console.log('🌐 Environment:', ENV);
console.log('🔗 API URL:', API_CONFIG[ENV]?.baseURL);

// Export the current configuration
export const API_BASE_URL = API_CONFIG[ENV]?.baseURL || API_CONFIG.development.baseURL;

export default {
  baseURL: API_BASE_URL,
  endpoints: {
    upload: '/upload/',
  }
};
