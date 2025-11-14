# 🚀 Guía de Despliegue - API de AOT-GAN

## ⚠️ IMPORTANTE

La API antigua (RDB) genera resultados **pixeleados de baja calidad**.  
La API de AOT-GAN genera resultados **de alta calidad (512x512)**.

**DEBES desplegar esta API (AOT-GAN) para obtener resultados de alta calidad.**

---

## 📋 Opciones de Despliegue

### Opción 1: Railway (Recomendada - Fácil)

Railway es ideal para proyectos con GPU o que requieren más recursos.

#### Pasos:

1. **Ir a Railway**
   - Visita https://railway.app
   - Crea una cuenta o inicia sesión

2. **Nuevo Proyecto**
   - Click en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Conecta tu repositorio `proyectoCG`

3. **Configurar Service**
   - Root Directory: `API`
   - Build Command: (dejar vacío, usará Dockerfile)
   - Start Command: `python main.py`

4. **Variables de Entorno**
   No son necesarias para la configuración básica

5. **Desplegar**
   - Railway detectará automáticamente el `Dockerfile`
   - Esperará ~5-10 minutos para el build
   - Recibirás una URL como: `https://tu-proyecto.railway.app`

6. **Actualizar Frontend**
   - Copia la URL de Railway
   - Actualiza `.env.production` en `image_inpainting_web/`
   - Redeploy en Vercel

---

### Opción 2: Render (Gratuito pero Limitado)

Render tiene plan gratuito pero es más lento y tiene menos recursos.

#### Pasos:

1. **Ir a Render**
   - Visita https://render.com
   - Crea una cuenta

2. **Nuevo Web Service**
   - Click en "New +" → "Web Service"
   - Conecta tu repositorio de GitHub

3. **Configuración**
   - **Name:** `aotgan-inpainting-api`
   - **Root Directory:** `API`
   - **Environment:** Docker
   - **Plan:** Free

4. **Configurar Dockerfile**
   Render detectará automáticamente el Dockerfile en `API/`

5. **Deploy**
   - Click en "Create Web Service"
   - Esperará ~10-15 minutos
   - URL: `https://aotgan-inpainting-api.onrender.com`

⚠️ **Limitaciones del Plan Gratuito:**
- Se duerme después de 15 minutos de inactividad
- Primera request puede tardar 30-60 segundos en despertar
- 512 MB RAM (puede ser insuficiente para el modelo)

---

### Opción 3: Hugging Face Spaces (Alternativa)

Buena opción para modelos de ML, plan gratuito incluye GPU.

#### Pasos:

1. **Crear Space**
   - Ir a https://huggingface.co/spaces
   - Click en "Create new Space"
   - Selecciona Docker SDK

2. **Configurar**
   - Sube el contenido de la carpeta `API/`
   - Usa el Dockerfile existente

3. **URL**
   - `https://huggingface.co/spaces/tu-usuario/aotgan-api`

---

## 🐳 Verificar Dockerfile

Asegúrate de que `API/Dockerfile` existe y está configurado correctamente:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copiar archivos
COPY requirements.txt .
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["python", "main.py"]
```

---

## 🧪 Probar la API Desplegada

Una vez desplegada, prueba estos endpoints:

### Health Check
```bash
curl https://tu-api.railway.app/
```

Respuesta esperada:
```json
{
  "status": "running",
  "model": "AOT-GAN",
  "device": "cpu"
}
```

### Probar Inpainting
```bash
curl -X POST "https://tu-api.railway.app/upload/" \
  -F "original_image=@test_image.jpg" \
  -F "mask=@test_mask.png"
```

---

## 🔄 Actualizar Frontend

Una vez que tengas la URL de la API desplegada:

1. **Editar `.env.production`:**
   ```env
   VITE_API_URL=https://tu-api.railway.app
   ```

2. **Commit y Push:**
   ```bash
   git add .
   git commit -m "Update API URL to AOT-GAN deployment"
   git push origin main
   ```

3. **Vercel redesplegará automáticamente**

---

## ⚙️ Configurar CORS

Si tienes problemas de CORS, edita `API/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://tu-frontend.vercel.app",  # ← Agregar tu dominio de Vercel
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🐛 Solución de Problemas

### Error: Model not found

El modelo `G0000000.pt` debe estar en:
```
API/AOT-GAN-for-Inpainting/experiments/CELEBA-HQ/G0000000.pt
```

Asegúrate de incluirlo en el repositorio o descargarlo durante el build.

### Error: Out of Memory

El modelo AOT-GAN requiere ~2GB de RAM. Opciones:
- Usar Railway (más RAM)
- Usar Hugging Face con GPU
- Optimizar el modelo

### API muy lenta

La primera request siempre es lenta (carga del modelo). Opciones:
- Mantener la API "caliente" con requests periódicas
- Usar un plan de pago con instancias siempre activas

---

## 📊 Comparación de Servicios

| Servicio | Plan Gratuito | RAM | GPU | Tiempo Inicio | Recomendación |
|----------|---------------|-----|-----|---------------|---------------|
| **Railway** | 5$/mes crédito | 8GB | No | Rápido | ⭐ Mejor |
| **Render** | Sí | 512MB | No | Lento | ⚠️ Limitado |
| **Hugging Face** | Sí | 16GB | Sí (limitado) | Medio | ✅ Buena |
| **Fly.io** | Sí (limitado) | 256MB | No | Rápido | ⚠️ Poco RAM |

---

## ✅ Checklist

- [ ] Desplegar API en Railway/Render/HuggingFace
- [ ] Obtener URL de la API desplegada
- [ ] Probar endpoint `/` y `/upload/`
- [ ] Actualizar `.env.production` con nueva URL
- [ ] Configurar CORS en la API
- [ ] Commit y push cambios
- [ ] Verificar que Vercel redespliega
- [ ] Probar inpainting desde el sitio web
- [ ] Verificar que los resultados son de alta calidad (no pixeleados)

---

**¿Necesitas ayuda?** Revisa los logs del deployment para ver errores específicos.
