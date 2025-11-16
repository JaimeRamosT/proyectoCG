git status# 🚂 Desplegar API en Railway

## Por qué Railway y no Vercel para la API?

**Vercel NO soporta tu API** porque:
- ❌ Límite de 250MB (tu modelo + PyTorch > 2GB)
- ❌ Máximo 60 segundos de ejecución
- ❌ Cold starts lentos (10-30 segundos)
- ❌ No está diseñado para ML/AI workloads

**Railway SÍ funciona** porque:
- ✅ Sin límite de tamaño
- ✅ Servidor persistente (no serverless)
- ✅ 500MB RAM gratis (suficiente para CPU inference)
- ✅ $5 USD de crédito gratis al mes

---

## 📋 Paso a Paso

### 1. Crear cuenta en Railway

1. Ve a https://railway.app
2. Sign up con GitHub
3. Verifica tu cuenta

### 2. Preparar el proyecto

Los archivos ya están listos:
- ✅ `api_/Dockerfile` - Para construir la imagen
- ✅ `api_/requirements.txt` - Dependencias
- ✅ `api_/main.py` - FastAPI server
- ✅ `api_/railway.json` - Configuración de Railway

### 3. Desplegar desde GitHub

#### Opción A: Desde Railway Dashboard (Recomendada)

1. **Ir a Railway Dashboard**
   ```
   https://railway.app/dashboard
   ```

2. **New Project**
   - Click en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Autoriza Railway a acceder a tu GitHub
   - Selecciona `proyectoCG` repository

3. **Configurar el servicio**
   - **Root Directory**: `api_`
   - **Build Command**: (automático con Dockerfile)
   - **Start Command**: (automático desde railway.json)

4. **Variables de Entorno**
   
   En Settings → Variables, agrega:
   
   ```env
   PORT=8000
   PYTHONUNBUFFERED=1
   ```

5. **Desplegar**
   - Railway detectará automáticamente el Dockerfile
   - Comenzará el build (tarda 5-10 minutos la primera vez)
   - Te dará una URL tipo: `https://tu-proyecto.up.railway.app`

#### Opción B: Desde Railway CLI

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Ir a la carpeta api
cd api

# Inicializar proyecto
railway init

# Desplegar
railway up

# Obtener URL
railway domain
```

### 4. Configurar CORS

El archivo `api_/main.py` ya tiene CORS configurado:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica tu dominio de Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Para producción, cambia `allow_origins` a:
```python
allow_origins=[
    "http://localhost:5173",
    "https://tu-proyecto.vercel.app"
]
```

### 5. Actualizar Frontend

1. **Edita `.env.production` en `image_inpainting_web/`:**
   ```env
   VITE_API_URL=https://tu-proyecto.up.railway.app
   ```

2. **Commit y push:**
   ```bash
   git add .
   git commit -m "Update API URL to Railway"
   git push origin main
   ```

3. **Vercel redesplegará automáticamente** el frontend con la nueva URL

---

## 🧪 Verificar el Deployment

### 1. Health Check

```bash
curl https://tu-proyecto.up.railway.app/
```

Deberías ver:
```json
{
  "status": "running",
  "model": "AOT-GAN",
  "device": "cpu"
}
```

### 2. Test Upload

```bash
curl -X POST https://tu-proyecto.up.railway.app/api/upload \
  -F "original_image=@test.jpg" \
  -F "mask=@mask.png"
```

### 3. Desde el Frontend

1. Abre tu app en Vercel: `https://tu-proyecto.vercel.app`
2. Sube una imagen
3. Dibuja una máscara
4. Verifica que funcione

---

## 📊 Monitoreo

### Ver Logs en Railway

1. Dashboard → Tu Proyecto → Deployments
2. Click en el deployment activo
3. Pestaña "Logs" para ver en tiempo real

### Métricas

Railway muestra:
- CPU usage
- Memory usage
- Request count
- Build time

---

## 💰 Costos

### Plan Gratis (Trial)
- **$5 USD de crédito** (suficiente para ~100-500 requests/mes)
- **500MB RAM**
- **1GB storage**
- **100GB network**

### Cuando se acabe el crédito gratuito

**Opción 1: Railway Hobby ($5/mes)**
- 8GB RAM
- 100GB egress
- Unlimited services

**Opción 2: Render (Gratis con limitaciones)**
- Spin down después de 15 min inactivo
- Tarda ~30 seg en arrancar de nuevo

**Opción 3: Hugging Face Spaces (Gratis)**
- Bueno para demos
- Puede ser lento

---

## 🔧 Troubleshooting

### Build falla por memoria

**Error:** `killed (out of memory)`

**Solución:** Reduce el tamaño de la imagen Docker
```dockerfile
# En Dockerfile, usa torch CPU-only
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### Cold starts lentos

**Problema:** Primera request tarda mucho

**Solución:** Railway mantiene el servicio activo (no como Vercel serverless)

### Modelo no se encuentra

**Error:** `Model not found at...`

**Solución:** Asegúrate de que el modelo esté en `api_/setup/experiments/CELEBA-HQ/G0000000.pt`

---

## 🚀 Arquitectura Final

```
┌─────────────────────┐
│   Usuario           │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Vercel (Frontend)   │  ← React + Vite
│ - HTML/CSS/JS       │  ← CDN Global
│ - Static Assets     │  ← Gratis
└──────────┬──────────┘
           │ API calls
           ▼
┌─────────────────────┐
│ Railway (Backend)   │  ← FastAPI + PyTorch
│ - AOT-GAN Model     │  ← Servidor persistente
│ - Image Processing  │  ← $5/mes (o gratis con crédito)
└─────────────────────┘
```

---

## ✅ Checklist de Deployment

- [ ] Cuenta en Railway creada
- [ ] Repositorio conectado a Railway
- [ ] Build completado exitosamente
- [ ] URL de Railway obtenida
- [ ] CORS configurado en la API
- [ ] `.env.production` actualizado con URL de Railway
- [ ] Frontend redesplegado en Vercel
- [ ] Health check funcionando
- [ ] Test de upload funcionando
- [ ] App completa funcionando end-to-end

---

## 📚 Recursos

- **Railway Docs:** https://docs.railway.app
- **Railway Discord:** https://discord.gg/railway
- **Render (alternativa):** https://render.com
- **Hugging Face (alternativa):** https://huggingface.co/spaces

---

**¿Listo?** 🚂

1. Ve a https://railway.app
2. "New Project" → "Deploy from GitHub"
3. Selecciona `proyectoCG`
4. Root directory: `api_`
5. Deploy! ✨
