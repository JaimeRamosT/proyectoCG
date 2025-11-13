# 🚀 Quick Start Guide - AOT-GAN Integration

## Inicio Rápido (5 minutos)

### 1. Backend (Terminal 1)

```bash
cd proyectoCG/model_API

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor
python start_api.py
```

✅ API corriendo en: http://localhost:8000

### 2. Frontend (Terminal 2)

```bash
cd proyectoCG/image_inpainting_web

# Instalar dependencias (primera vez)
npm install

# Iniciar desarrollo
npm run dev
```

✅ Frontend corriendo en: http://localhost:5173

### 3. Probar

1. Abrir navegador: http://localhost:5173
2. Cargar imagen
3. Dibujar sobre área a rellenar
4. Click "Guardar Máscara"
5. Ver resultado!

## ¿Qué cambió?

### Antes ❌
- Modelo TensorFlow/Keras básico
- Resolución 64x64 (baja calidad)
- Necesitaba super-resolution

### Ahora ✅
- Modelo AOT-GAN (state-of-the-art)
- Resolución 512x512 (alta calidad)
- Sin post-procesamiento necesario

## Verificación Rápida

### Backend funcionando?
```bash
curl http://localhost:8000/
```
Deberías ver: `{"status":"running","model":"AOT-GAN",...}`

### Frontend funcionando?
Abrir: http://localhost:5173
Deberías ver la interfaz de carga de imágenes

## Problemas Comunes

### "Model not found"
El modelo debe estar en:
```
AOT-GAN-for-Inpainting/experiments/CELEBA-HQ/G0000000.pt
```

### Frontend no conecta con Backend
Verificar en `image_inpainting_web/src/config/api.js`:
```javascript
development: {
  baseURL: 'http://localhost:8000',
}
```

### Instalación lenta de PyTorch
Normal, PyTorch es grande (~2GB). Solo se hace una vez.

## Documentación Completa

- **INTEGRACION.md** - Guía completa de integración
- **proyectoCG/model_API/README_API.md** - Documentación de la API

## Siguiente Paso

Para producción, ver sección "Deployment" en INTEGRACION.md
