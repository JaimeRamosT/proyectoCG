# 🎨 Image Inpainting Web - Frontend

Aplicación web interactiva para realizar inpainting de imágenes usando el modelo AOT-GAN.

## 🚀 Tecnologías

- **React 18** - Framework UI
- **Vite** - Build tool ultrarrápido
- **TailwindCSS** - Estilos utility-first
- **Konva/React-Konva** - Canvas interactivo para dibujar máscaras
- **React Router** - Navegación
- **React Markdown** - Renderizado de markdown

## 📦 Instalación Local

```bash
# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev

# Build para producción
npm run build

# Preview del build
npm run preview
```

## 🌐 Despliegue en Vercel

Ver la guía completa: [DEPLOY_VERCEL.md](./DEPLOY_VERCEL.md)

**Resumen rápido:**

1. Actualizar `.env.production` con la URL de tu API
2. Push a GitHub
3. Importar proyecto en Vercel
4. Configurar root directory: `proyectoCG/image_inpainting_web`
5. Agregar variable de entorno: `VITE_API_URL`
6. Deploy! 🚀

## ⚙️ Configuración

### Variables de Entorno

Crea un archivo `.env` basado en `.env.example`:

```env
# URL de la API backend
VITE_API_URL=http://localhost:8000
```

Para producción, usa `.env.production`:
```env
VITE_API_URL=https://tu-api-backend.com
```

### API Configuration

La configuración de la API se encuentra en `src/config/api.js`:

```javascript
const API_CONFIG = {
  development: {
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  },
  production: {
    baseURL: import.meta.env.VITE_API_URL || 'https://api.example.com',
  }
};
```

## 📁 Estructura del Proyecto

```
image_inpainting_web/
├── public/              # Archivos estáticos
├── src/
│   ├── components/      # Componentes React
│   ├── config/          # Configuración (API, etc.)
│   ├── pages/           # Páginas/Rutas
│   ├── App.jsx          # Componente principal
│   └── main.jsx         # Entry point
├── .env.example         # Ejemplo de variables de entorno
├── .env.production      # Variables para producción
├── vercel.json          # Configuración de Vercel
├── vite.config.js       # Configuración de Vite
├── tailwind.config.js   # Configuración de Tailwind
└── package.json         # Dependencias
```

## 🎯 Características

- ✅ Carga de imágenes (drag & drop o click)
- ✅ Dibujo de máscaras interactivo con Konva
- ✅ Ajuste de tamaño de pincel
- ✅ Deshacer/rehacer
- ✅ Limpiar máscara
- ✅ Procesamiento con AOT-GAN
- ✅ Descarga de resultados
- ✅ Responsive design
- ✅ Dark mode compatible

## 🔗 Integración con Backend

El frontend se comunica con la API mediante:

```javascript
// Upload image and mask for inpainting
const formData = new FormData();
formData.append("original_image", imageFile);
formData.append("mask", maskFile);

const response = await fetch(`${API_BASE_URL}/upload/`, {
  method: "POST",
  body: formData,
});

const result = await response.json();
// result.output_image.data contiene la imagen en base64
```

## 🐛 Solución de Problemas

### CORS Errors

Si ves errores de CORS, asegúrate de que la API tenga configurado:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://tu-dominio.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API No Responde

1. Verifica que la API esté corriendo
2. Verifica la URL en la consola del navegador (F12)
3. Verifica las variables de entorno

### Build Errors

```bash
# Limpiar cache y reinstalar
rm -rf node_modules package-lock.json
npm install
npm run build
```

## 📚 Scripts Disponibles

```bash
npm run dev      # Servidor de desarrollo (puerto 5173)
npm run build    # Build para producción
npm run preview  # Preview del build
npm run lint     # Linter ESLint
```

## 🌟 Deploy Platforms

Este proyecto está configurado para:
- ✅ **Vercel** (Recomendado) - Ver [DEPLOY_VERCEL.md](./DEPLOY_VERCEL.md)
- ✅ **Netlify** - Similar a Vercel
- ✅ **GitHub Pages** - Requiere configuración adicional
- ✅ **Railway** - Fullstack deployment

## 📄 Licencia

Parte del proyecto Image Inpainting - UTEC 2025

---

**Desarrollado con ❤️ usando React + Vite**
