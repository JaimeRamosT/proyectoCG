# 🎨 Image Inpainting - Arquitectura de Deployment

## 📊 Arquitectura del Proyecto

```
┌──────────────────────────────────────────────────────────┐
│                        USUARIO                           │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────┐
│              VERCEL (Frontend)                         │
│  ┌──────────────────────────────────────────────┐     │
│  │  React + Vite App                             │     │
│  │  - Upload de imágenes                         │     │
│  │  - Canvas interactivo (Konva)                 │     │
│  │  - Visualización de resultados                │     │
│  └──────────────────────────────────────────────┘     │
│  ✅ Gratis                                             │
│  ✅ CDN Global                                         │
│  ✅ Deploy automático desde GitHub                    │
└────────────────┬───────────────────────────────────────┘
                 │ HTTP POST
                 │ /api/upload
                 ▼
┌────────────────────────────────────────────────────────┐
│              RAILWAY (Backend API)                     │
│  ┌──────────────────────────────────────────────┐     │
│  │  FastAPI + PyTorch                            │     │
│  │  - AOT-GAN Model (512x512)                    │     │
│  │  - Image Processing con OpenCV               │     │
│  │  - Servidor persistente (no serverless)      │     │
│  └──────────────────────────────────────────────┘     │
│  💰 $5 USD/mes (o gratis con crédito trial)           │
│  🚀 Sin cold starts                                    │
│  💪 Maneja cargas ML pesadas                           │
└────────────────────────────────────────────────────────┘
```

---

## 🚫 Por qué NO usar Vercel para la API?

### Limitaciones de Vercel Serverless Functions:

| Aspecto | Vercel Limit | Tu API Necesita | Resultado |
|---------|--------------|-----------------|-----------|
| Tamaño | 250 MB | ~2 GB (PyTorch + modelo) | ❌ No cabe |
| Timeout | 60 seg (Pro) | 5-10 seg por request | ⚠️ Límite justo |
| Memoria | 3 GB (Pro) | 2-4 GB para PyTorch | ⚠️ Muy ajustado |
| Cold Start | 10-30 seg | Modelo carga en 5-10 seg | ❌ Experiencia mala |
| Costo | $20/mes (Pro) | - | 💸 Caro |

### Por qué Railway es mejor:

| Aspecto | Railway | Ventaja |
|---------|---------|---------|
| Tamaño | Sin límite | ✅ Cabe todo |
| Timeout | Sin límite | ✅ No hay prisa |
| Memoria | 512 MB - 8 GB | ✅ Suficiente |
| Cold Start | No aplica (servidor persistente) | ✅ Siempre rápido |
| Costo | $5/mes (gratis trial) | ✅ Económico |

---

## 🚀 Deployment Steps

### 1. Desplegar Backend (Railway)

**Sigue:** `DEPLOY_API_RAILWAY.md`

Resumen rápido:
```bash
# 1. Crear cuenta en Railway
https://railway.app

# 2. New Project → Deploy from GitHub
Selecciona: proyectoCG
Root directory: api_

# 3. Espera el build (5-10 min)
# 4. Copia tu URL: https://xxx.up.railway.app
```

### 2. Configurar Frontend

```bash
# Edita image_inpainting_web/.env.production
VITE_API_URL=https://tu-proyecto.up.railway.app
```

### 3. Desplegar Frontend (Vercel)

```bash
# 1. Push a GitHub
git add .
git commit -m "Update API URL to Railway"
git push origin main

# 2. Vercel despliega automáticamente
# Tu app estará en: https://tu-proyecto.vercel.app
```

---

## 📁 Estructura del Repositorio

```
proyectoCG/
├── api_/                          ← Backend (Railway)
│   ├── Dockerfile               ← Para Railway
│   ├── railway.json             ← Config de Railway
│   ├── main.py                  ← FastAPI server
│   ├── requirements.txt         ← PyTorch, OpenCV, etc.
│   ├── src/
│   │   └── aot_inpainting.py   ← Lógica del modelo
│   └── setup/
│       └── experiments/
│           └── CELEBA-HQ/
│               └── G0000000.pt  ← Modelo AOT-GAN
│
├── image_inpainting_web/        ← Frontend (Vercel)
│   ├── src/
│   │   ├── components/          ← React components
│   │   ├── config/
│   │   │   └── api.js          ← URL de la API
│   │   └── App.jsx
│   ├── .env.production         ← VITE_API_URL
│   └── package.json
│
├── vercel.json                  ← Config Vercel (solo frontend)
├── DEPLOY_API_RAILWAY.md       ← Guía completa Railway
└── DEPLOY_ARCHITECTURE.md      ← Este archivo
```

---

## 🔄 Flujo de una Request

```
1. Usuario sube imagen en https://tu-proyecto.vercel.app
   │
   ├─> Canvas.jsx captura imagen + máscara
   │
2. Frontend hace POST a Railway
   │
   POST https://tu-proyecto.up.railway.app/api/upload
   FormData: { original_image, mask }
   │
3. Railway procesa
   │
   ├─> main.py recibe request
   ├─> Carga modelo AOT-GAN (si no está en memoria)
   ├─> Procesa imagen (5-10 seg)
   └─> Retorna imagen base64
   │
4. Frontend muestra resultado
   │
   └─> Canvas.jsx renderiza imagen procesada
```

---

## 💰 Costos Mensuales

### Gratis (Trial)
- **Vercel:** Gratis (hobby tier)
- **Railway:** $5 USD de crédito gratis
- **Total:** $0 USD (primeros ~100-500 requests)

### Después del trial
- **Vercel:** $0 USD (sigue gratis)
- **Railway:** $5 USD/mes (Hobby plan)
- **Total:** $5 USD/mes

### Alternativas si Railway se vuelve caro
1. **Render:** Gratis con spin-down (tarda 30 seg en arrancar)
2. **Hugging Face Spaces:** Gratis para demos
3. **Fly.io:** $5/mes similar a Railway

---

## 🧪 Testing

### Local Development

```bash
# Terminal 1: Backend
cd api_
python main.py
# Corre en http://localhost:8000

# Terminal 2: Frontend  
cd image_inpainting_web
npm run dev
# Corre en http://localhost:5173
```

### Production

```bash
# Health check Backend
curl https://tu-proyecto.up.railway.app/

# Health check Frontend
curl https://tu-proyecto.vercel.app/
```

---

## 📊 Monitoreo

### Railway (Backend)
- Dashboard → Logs (tiempo real)
- Métricas de CPU/RAM
- Request count

### Vercel (Frontend)
- Dashboard → Analytics
- Page views
- Performance metrics

---

## ⚡ Performance

### Tiempos esperados:

| Operación | Tiempo | Nota |
|-----------|--------|------|
| Load frontend | < 2 seg | Vercel CDN |
| First API call | 5-10 seg | Carga modelo |
| Subsequent calls | 2-5 seg | Modelo en memoria |
| Image processing | 3-8 seg | Depende del tamaño |

### Optimizaciones:

1. **Keep-alive en Railway:** El servidor permanece activo
2. **Modelo en memoria:** Solo se carga una vez
3. **CDN de Vercel:** Frontend ultra rápido
4. **Compresión de imágenes:** Reduce transfer time

---

## 🔒 Seguridad

### CORS
```python
# En api_/main.py
allow_origins=[
    "https://tu-proyecto.vercel.app",  # Tu dominio
    "http://localhost:5173"             # Desarrollo
]
```

### Environment Variables
- Railway: Settings → Variables
- Vercel: Settings → Environment Variables

### Secrets
- Nunca commitees API keys
- Usa variables de entorno

---

## ✅ Checklist Final

- [ ] Backend desplegado en Railway
- [ ] URL de Railway copiada
- [ ] `.env.production` actualizado
- [ ] CORS configurado en backend
- [ ] Frontend desplegado en Vercel
- [ ] Test: Upload imagen funciona
- [ ] Test: Inpainting funciona
- [ ] Monitoreo configurado
- [ ] Costos entendidos

---

## 🆘 Soporte

### Si algo falla:

1. **Check Railway logs:** Dashboard → Deployments → Logs
2. **Check Vercel logs:** Dashboard → Deployments → Function Logs
3. **Check browser console:** F12 → Console

### Recursos:
- [Railway Discord](https://discord.gg/railway)
- [Vercel Discord](https://discord.gg/vercel)
- GitHub Issues de este repo

---

**Última actualización:** Noviembre 2025
