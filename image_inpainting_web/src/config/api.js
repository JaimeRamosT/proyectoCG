// Detectar si estamos en producción (deployment) o desarrollo (local)
const isProduction = import.meta.env.PROD || window.location.hostname !== 'localhost';

// API Configuration
const API_CONFIG = {
  // Development API (localhost)
  development: {
    baseURL: 'http://localhost:8000',
  },
  // Production API (Railway)
  production: {
    baseURL: import.meta.env.VITE_API_URL || 'https://image-inpainting-web-production.up.railway.app/',
  }
};

// Seleccionar configuración basada en el entorno
const ENV = isProduction ? 'production' : 'development';

console.log('🌐 Environment:', ENV);
console.log('🔗 Hostname:', window.location.hostname);
console.log('🔗 API Base URL:', API_CONFIG[ENV].baseURL);

// Export the current configuration
export const API_BASE_URL = API_CONFIG[ENV].baseURL;

export default {
  baseURL: API_BASE_URL,
  endpoints: {
    upload: '/api/upload',
  }
};
