# 🚀 Deployment en Vercel - AOT-GAN Image Inpainting

Este proyecto está configurado para desplegarse en Vercel con **frontend (React + Vite) y API (Python AOT-GAN)** en el mismo dominio.

## ✅ Configuración Completada

El proyecto incluye:

1. **Frontend**: React con Vite en `image_inpainting_web/`
2. **API Serverless**: Python con FastAPI en `api/`
3. **Modelo AOT-GAN**: G0000000.pt (58 MB) en `api/AOT-GAN-for-Inpainting/experiments/CELEBA-HQ/`
4. **Configuración Vercel**: `vercel.json` con builds duales

## 📋 Verificación Pre-Deployment

Ejecuta el script de verificación:

```bash
node verify-deployment.js
```

Deberías ver **12/12 checks ✅** antes de desplegar.

## 🌐 Deployment en Vercel

### Opción 1: Vercel CLI (Recomendado)

1. **Instala Vercel CLI** (si no lo tienes):
   ```bash
   npm install -g vercel
   ```

2. **Login en Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy a Producción**:
   ```bash
   vercel --prod
   ```

   Durante el deployment, Vercel te preguntará:
   - ✅ **Link to existing project?** → No (primera vez) o Yes (si ya existe)
   - ✅ **Project name?** → `image-inpainting-aot-gan` (o el que prefieras)
   - ✅ **Directory to deploy?** → `.` (raíz del proyecto)

### Opción 2: GitHub Integration

1. **Conecta tu repositorio** a Vercel:
   - Ve a [vercel.com](https://vercel.com)
   - Haz clic en **"Add New Project"**
   - Importa tu repositorio de GitHub

2. **Configuración automática**:
   Vercel detectará el `vercel.json` y configurará todo automáticamente.

3. **Deploy**:
   Cada push a `main` desplegará automáticamente.

## 🔧 Configuración de Vercel

### Build Settings (Auto-detectado)

- **Framework Preset**: Other
- **Build Command**: `cd image_inpainting_web && npm install && npm run vercel-build`
- **Output Directory**: `image_inpainting_web/dist`
- **Install Command**: `npm install` (en image_inpainting_web/)

### Function Settings

- **Memory**: 3008 MB (máximo disponible)
- **Max Duration**: 60 segundos
- **Max Lambda Size**: 100 MB

### Environment Variables

No se requieren variables de entorno adicionales. La API se sirve en `/api` del mismo dominio.

## 📁 Estructura de Deployment

```
proyectoCG/
├── vercel.json                    # Configuración principal
├── .vercelignore                  # Archivos a excluir
├── api/                          # 🐍 Serverless Functions (Python)
│   ├── index.py                  # Handler principal
│   ├── requirements.txt          # Dependencias Python
│   ├── src/
│   │   └── aot_inpainting.py    # Lógica AOT-GAN
│   └── setup/
│       └── experiments/
│           └── CELEBA-HQ/
│               └── G0000000.pt   # Modelo (58 MB)
└── image_inpainting_web/         # ⚛️ Frontend (Static)
    ├── package.json
    ├── vite.config.js
    └── dist/                     # Build output
```

## 🌍 Endpoints Después del Deployment

Suponiendo que tu dominio es `https://tu-proyecto.vercel.app`:

- **Frontend**: `https://tu-proyecto.vercel.app/`
- **API Health Check**: `https://tu-proyecto.vercel.app/api`
- **Inpainting Endpoint**: `https://tu-proyecto.vercel.app/api/upload`

## 🔍 Testing Post-Deployment

### 1. Health Check

```bash
curl https://tu-proyecto.vercel.app/api
```

Respuesta esperada:
```json
{
  "status": "running",
  "model": "AOT-GAN",
  "platform": "Vercel Serverless",
  "device": "cpu"
}
```

### 2. Test de Inpainting

El frontend automáticamente usará el endpoint `/api/upload` del mismo dominio.

1. Abre el sitio web
2. Dibuja una máscara en la imagen
3. Haz clic en "Inpaint"
4. Verifica que los resultados sean de **alta calidad** (no pixelados)

## ⚠️ Limitaciones Importantes

1. **Cold Start**: Primera request tardará ~10-30 segundos (carga del modelo)
2. **Processing Time**: Cada inpainting toma ~5-15 segundos
3. **Model Size**: 58 MB (dentro del límite de 100 MB de Vercel)
4. **CPU Only**: Sin GPU en Vercel Serverless
5. **Timeout**: Máximo 60 segundos por request

## 🐛 Troubleshooting

### Error: "Model not found"

Verifica que el modelo esté en la ruta correcta:
```bash
ls -lh api/setup/experiments/CELEBA-HQ/G0000000.pt
```

### Error: "Function size exceeded"

El modelo + dependencias debe ser < 100 MB. Verifica `.vercelignore` para excluir archivos innecesarios.

### Frontend muestra resultados pixelados

Verifica en `image_inpainting_web/src/config/api.js`:
```javascript
production: {
  baseURL: '',  // Debe estar vacío (mismo dominio)
  endpoints: {
    upload: '/api/upload'  // Debe apuntar a /api
  }
}
```

### Build falla en Vercel

1. Revisa los logs en Vercel Dashboard
2. Verifica que `image_inpainting_web/package.json` tenga `vercel-build` script
3. Asegúrate de que todas las dependencias estén en `package.json`

## 📝 Logs y Monitoring

En Vercel Dashboard:
- **Deployments**: Ver historial y logs de build
- **Functions**: Ver logs de ejecución de la API
- **Analytics**: Ver tráfico y performance

## 🔄 Re-deployment

Para re-desplegar después de cambios:

```bash
# Con Vercel CLI
vercel --prod

# O simplemente haz push a GitHub (si está conectado)
git push origin main
```

## 📚 Documentación Adicional

- [Vercel Serverless Functions](https://vercel.com/docs/functions)
- [Vercel Python Runtime](https://vercel.com/docs/functions/runtimes/python)
- [Vite Deployment](https://vitejs.dev/guide/static-deploy.html)

---

## ✨ Resultado Esperado

Después del deployment exitoso:

1. ✅ Frontend carga en < 2 segundos
2. ✅ API responde en `/api` endpoint
3. ✅ Inpainting produce resultados de **alta calidad** (512x512, sin pixelación)
4. ✅ Mismo dominio para frontend y API (sin CORS issues)

---

**¿Problemas?** Revisa los logs en [Vercel Dashboard](https://vercel.com/dashboard)
