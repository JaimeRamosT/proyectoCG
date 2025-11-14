# 📋 Configuración para Despliegue en Vercel - Resumen

## ✅ Archivos Creados/Actualizados

### Nuevos Archivos
1. ✅ `vercel.json` - Configuración de Vercel
2. ✅ `.env.example` - Ejemplo de variables de entorno
3. ✅ `.env.production` - Variables para producción
4. ✅ `.gitignore` - Archivos a ignorar (incluye .vercel)
5. ✅ `DEPLOY_VERCEL.md` - Guía completa de despliegue

### Archivos Actualizados
1. ✅ `src/config/api.js` - Ahora usa variables de entorno
2. ✅ `vite.config.js` - Optimizado para producción
3. ✅ `README.md` - Documentación completa

---

## 🚀 Pasos Rápidos para Desplegar

### 1. Actualizar la URL de tu API

Edita `.env.production`:
```env
VITE_API_URL=https://tu-api-desplegada.com
```

### 2. Commit y Push

```bash
cd image_inpainting_web
git add .
git commit -m "Configure for Vercel deployment"
git push origin main
```

### 3. Desplegar en Vercel

**Opción A: Dashboard Web**
1. Ir a https://vercel.com/new
2. Importar tu repositorio de GitHub
3. Configurar:
   - **Root Directory:** `image_inpainting_web`
   - **Framework:** Vite
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
4. Agregar variable de entorno:
   - **Name:** `VITE_API_URL`
   - **Value:** URL de tu API
5. Click en "Deploy"

**Opción B: CLI**
```bash
npm install -g vercel
cd proyectoCG/image_inpainting_web
vercel login
vercel
vercel --prod
```

### 4. Configurar CORS en tu API

Actualiza `API/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://tu-proyecto.vercel.app",  # ← Tu dominio de Vercel
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📁 Configuración de Archivos

### vercel.json
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### Variables de Entorno en Vercel

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `VITE_API_URL` | `https://tu-api.com` | URL de tu API desplegada |

**Importante:** Configurar para Production, Preview y Development

---

## 🔍 Verificación Post-Despliegue

### 1. Verificar Build
- ✅ Build debe completarse sin errores
- ✅ Tiempo de build: ~2-5 minutos

### 2. Verificar URL
- ✅ Abrir `https://tu-proyecto.vercel.app`
- ✅ La aplicación debe cargar correctamente

### 3. Verificar API Connection
- ✅ Abrir consola del navegador (F12)
- ✅ Debe mostrar: `🌐 Environment: production`
- ✅ Debe mostrar: `🔗 API URL: https://tu-api.com`

### 4. Probar Funcionalidad
- ✅ Subir una imagen
- ✅ Dibujar máscara
- ✅ Procesar con la API
- ✅ Verificar que devuelva resultado

---

## 🐛 Problemas Comunes

### Build Falla

**Error:** `Module not found`
```bash
# Verificar localmente primero
npm install
npm run build
```

**Error:** `vite: command not found`
```bash
npm install --save-dev vite
```

### CORS Error

```
Access blocked by CORS policy
```

**Solución:**
1. Agregar dominio de Vercel en `allow_origins` de la API
2. Verificar que la API esté corriendo
3. Redeploy la API si es necesario

### Variables de Entorno No Funcionan

**Problema:** La app usa localhost en producción

**Solución:**
1. Verificar que la variable en Vercel empiece con `VITE_`
2. Redeploy después de agregar variables
3. Verificar en la consola del navegador el valor

### 404 en Rutas

**Problema:** Refresh en `/about` da 404

**Solución:** Ya configurado en `vercel.json` con rewrites

---

## 📊 Estructura Final

```
proyectoCG/
├── API/
│   └── AOT-GAN-for-Inpainting/  # Modelo pre-entrenado
└── image_inpainting_web/
    ├── .env.example              # 🆕 Ejemplo de variables
    ├── .env.production           # 🆕 Variables de producción
    ├── .gitignore               # 🆕 Actualizado
    ├── vercel.json              # 🆕 Config de Vercel
    ├── DEPLOY_VERCEL.md         # 🆕 Guía completa
    ├── README.md                # ✅ Actualizado
    ├── vite.config.js           # ✅ Optimizado
    ├── src/
    │   └── config/
    │       └── api.js           # ✅ Usa env vars
    └── package.json
```

---

## 🎯 Siguientes Pasos Recomendados

### Inmediato
1. [ ] Actualizar `.env.production` con URL real de API
2. [ ] Hacer commit y push
3. [ ] Desplegar en Vercel
4. [ ] Configurar CORS en API
5. [ ] Probar aplicación desplegada

### Opcional
- [ ] Configurar dominio personalizado
- [ ] Configurar analytics de Vercel
- [ ] Configurar preview deployments
- [ ] Agregar tests antes de deploy
- [ ] Configurar CI/CD con GitHub Actions

---

## 📚 Recursos

- **Guía Completa:** [DEPLOY_VERCEL.md](./DEPLOY_VERCEL.md)
- **Documentación Vercel:** https://vercel.com/docs
- **Vite Deploy:** https://vitejs.dev/guide/static-deploy.html

---

## ✨ Características de Vercel

- ✅ Despliegue automático desde Git
- ✅ Preview deployments para PRs
- ✅ Edge Network global (CDN)
- ✅ SSL automático (HTTPS)
- ✅ Dominios personalizados
- ✅ Analytics incluido
- ✅ Rollbacks con un click
- ✅ 100% gratis para proyectos personales

---

**¿Necesitas ayuda?** Revisa [DEPLOY_VERCEL.md](./DEPLOY_VERCEL.md) para solución de problemas detallada.
