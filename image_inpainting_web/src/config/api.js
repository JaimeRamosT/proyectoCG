// API Configuration
const API_CONFIG = {
  // Development API
  development: {
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  },
  // Production API (Vercel Serverless - mismo dominio)
  // La API se despliega en el mismo proyecto de Vercel en /api
  production: {
    baseURL: import.meta.env.VITE_API_URL || '', // Mismo dominio, ruta /api
  }
};

// Automatically detect environment
const ENV = import.meta.env.MODE || 'development';

console.log('🌐 Environment:', ENV);
console.log('🔗 API URL:', API_CONFIG[ENV]?.baseURL || 'Same domain (/api)');

// Export the current configuration
export const API_BASE_URL = API_CONFIG[ENV]?.baseURL || API_CONFIG.development.baseURL;

export default {
  baseURL: API_BASE_URL,
  endpoints: {
    upload: '/api/upload', // Ruta actualizada para Vercel
  }
};
