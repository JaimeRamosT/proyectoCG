// Detectar si estamos en producción (deployment) o desarrollo (local)
const isProduction = import.meta.env.PROD || window.location.hostname !== 'localhost';

// API Configuration
const API_CONFIG = {
  // Development API (localhost)
  development: {
    baseURL: 'http://localhost:8000',
  },
  // Production API (Vercel Serverless - mismo dominio)
  production: {
    baseURL: '', // Mismo dominio, usa rutas relativas
  }
};

// Seleccionar configuración basada en el entorno
const ENV = isProduction ? 'production' : 'development';

console.log('🌐 Environment:', ENV);
console.log('🔗 Hostname:', window.location.hostname);
console.log('🔗 API Base URL:', API_CONFIG[ENV].baseURL || 'Same domain (relative)');

// Export the current configuration
export const API_BASE_URL = API_CONFIG[ENV].baseURL;

export default {
  baseURL: API_BASE_URL,
  endpoints: {
    upload: '/api/upload', // Ruta actualizada para Vercel
  }
};
