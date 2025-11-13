# 🚀 Guía de Despliegue en Vercel

## Prerequisitos

1. **Cuenta en Vercel**: Crea una cuenta en [vercel.com](https://vercel.com)
2. **API Backend desplegada**: Tu API debe estar desplegada en algún servicio (Railway, Render, etc.)
3. **Git Repository**: Tu proyecto debe estar en GitHub, GitLab o Bitbucket

---

## 📋 Paso a Paso

### 1. Preparar el Proyecto

#### A. Verificar que los archivos de configuración existan

Ya están creados en el proyecto:
- ✅ `vercel.json` - Configuración de Vercel
- ✅ `.env.example` - Ejemplo de variables de entorno
- ✅ `.env.production` - Variables de producción
- ✅ `.gitignore` - Archivos ignorados por Git

#### B. Actualizar la URL de la API

Edita `.env.production` y actualiza `VITE_API_URL` con la URL de tu API desplegada:

```env
VITE_API_URL=https://tu-api-backend.railway.app
```

O si usas Render:
```env
VITE_API_URL=https://tu-api-backend.onrender.com
```

#### C. Hacer commit de los cambios

```bash
git add .
git commit -m "Add Vercel configuration"
git push origin main
```

---

### 2. Desplegar en Vercel

#### Opción A: Desde el Dashboard de Vercel (Recomendada)

1. **Ir a Vercel Dashboard**
   - Visita https://vercel.com/dashboard
   - Click en "Add New Project"

2. **Importar Repositorio**
   - Conecta tu cuenta de GitHub/GitLab/Bitbucket
   - Selecciona el repositorio `proyectoCG`
   - Click en "Import"

3. **Configurar el Proyecto**
   
   **Root Directory:**
   ```
   proyectoCG/image_inpainting_web
   ```
   
   **Framework Preset:**
   ```
   Vite
   ```
   
   **Build Command:**
   ```
   npm run build
   ```
   
   **Output Directory:**
   ```
   dist
   ```
   
   **Install Command:**
   ```
   npm install
   ```

4. **Configurar Variables de Entorno**
   
   En "Environment Variables", agrega:
   
   | Name | Value |
   |------|-------|
   | `VITE_API_URL` | `https://tu-api-backend.com` |
   
   **Importante:** Marca las variables para todos los entornos (Production, Preview, Development)

5. **Desplegar**
   - Click en "Deploy"
   - Espera a que el build termine (2-5 minutos)
   - ✅ ¡Tu aplicación está desplegada!

#### Opción B: Desde la CLI de Vercel

```bash
# Instalar Vercel CLI
npm install -g vercel

# Ir a la carpeta del frontend
cd proyectoCG/image_inpainting_web

# Login en Vercel
vercel login

# Desplegar
vercel

# Seguir las instrucciones:
# - Set up and deploy? Y
# - Which scope? [Tu cuenta]
# - Link to existing project? N
# - What's your project's name? image-inpainting-web
# - In which directory is your code located? ./
# - Want to override the settings? N

# Para producción
vercel --prod
```

---

### 3. Configurar Variables de Entorno en Vercel

Si desplegaste desde la CLI y no configuraste las variables:

1. Ir a tu proyecto en https://vercel.com/dashboard
2. Click en "Settings" → "Environment Variables"
3. Agregar:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://tu-api-backend.com`
   - **Environments:** Production, Preview, Development

4. Click en "Save"
5. Ir a "Deployments" → Click en los tres puntos del último deployment → "Redeploy"

---

### 4. Verificar el Despliegue

1. **Visita la URL de tu aplicación**
   ```
   https://tu-proyecto.vercel.app
   ```

2. **Abrir la consola del navegador (F12)**
   - Debes ver:
     ```
     🌐 Environment: production
     🔗 API URL: https://tu-api-backend.com
     ```

3. **Probar la funcionalidad**
   - Sube una imagen
   - Dibuja una máscara
   - Verifica que la API responda correctamente

---

## 🔧 Configuración Avanzada

### Dominios Personalizados

1. Ir a "Settings" → "Domains"
2. Click en "Add Domain"
3. Ingresa tu dominio: `inpainting.tudominio.com`
4. Sigue las instrucciones para configurar el DNS

### CORS en la API

Tu API debe permitir requests desde el dominio de Vercel:

```python
# En API/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://tu-proyecto.vercel.app",
        "https://inpainting.tudominio.com",  # Si tienes dominio personalizado
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

O permitir todos los orígenes (menos seguro):
```python
allow_origins=["*"],
```

### Múltiples Entornos

**Preview Deployments:**
- Cada PR crea un deployment de preview automáticamente
- Usa variables de entorno específicas para preview si es necesario

**Environment-specific URLs:**
```javascript
// src/config/api.js
const API_CONFIG = {
  development: {
    baseURL: 'http://localhost:8000',
  },
  preview: {
    baseURL: import.meta.env.VITE_API_URL || 'https://api-preview.example.com',
  },
  production: {
    baseURL: import.meta.env.VITE_API_URL || 'https://api.example.com',
  }
};
```

---

## 🐛 Solución de Problemas

### Build falla en Vercel

**Error:** `npm install` falla
```bash
# Verificar localmente
npm install
npm run build
```

**Error:** Variables de entorno no encontradas
- Verificar que `VITE_API_URL` esté configurada en Vercel
- Las variables de Vite **deben** empezar con `VITE_`

### CORS Errors

```
Access to fetch at 'https://api.example.com' from origin 'https://tu-proyecto.vercel.app' 
has been blocked by CORS policy
```

**Solución:**
- Agregar el dominio de Vercel en `allow_origins` de la API
- Verificar que la API esté corriendo

### 404 en rutas

**Problema:** Refresh en `/page` da 404

**Solución:** Ya está configurado en `vercel.json`:
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### API URL incorrecta

**Verificar en la consola del navegador:**
```javascript
console.log('API URL:', import.meta.env.VITE_API_URL);
```

**Actualizar en Vercel:**
- Settings → Environment Variables → Edit `VITE_API_URL`
- Redeploy el proyecto

---

## 📊 Monitoreo

### Analytics

Vercel incluye analytics gratuitos:
- Ir a "Analytics" en el dashboard
- Ver page views, unique visitors, top pages

### Logs

Ver logs de build y runtime:
- Ir a "Deployments"
- Click en un deployment
- Ver "Build Logs" y "Function Logs"

---

## 🔄 Despliegues Automáticos

Vercel despliega automáticamente cuando:
- ✅ Haces `git push` al branch principal → Production
- ✅ Creas un Pull Request → Preview deployment
- ✅ Actualizas un PR → Actualiza el preview

### Desactivar despliegues automáticos

Settings → Git → Auto Deployments → Toggle off

---

## 💡 Mejores Prácticas

1. **Variables de Entorno**
   - Nunca commitees archivos `.env`
   - Usa `.env.example` para documentar variables necesarias
   - Configura todas las variables en Vercel

2. **Performance**
   - Vite ya optimiza el bundle automáticamente
   - Usa lazy loading para rutas: `React.lazy()`
   - Comprime imágenes antes de subirlas

3. **Seguridad**
   - Configura CORS correctamente
   - No expongas API keys en el frontend
   - Usa HTTPS siempre

4. **Testing**
   - Prueba en preview deployments antes de mergear a main
   - Verifica que la API esté disponible

---

## 📚 Recursos

- **Documentación de Vercel:** https://vercel.com/docs
- **Vite Deploy Guide:** https://vitejs.dev/guide/static-deploy.html#vercel
- **Vercel CLI:** https://vercel.com/docs/cli

---

## ✅ Checklist de Despliegue

- [ ] API backend desplegada y funcionando
- [ ] URL de la API actualizada en `.env.production`
- [ ] Código commiteado y pusheado a GitHub
- [ ] Proyecto importado en Vercel
- [ ] Root directory configurado correctamente
- [ ] Variable `VITE_API_URL` configurada en Vercel
- [ ] Build exitoso en Vercel
- [ ] CORS configurado en la API
- [ ] Aplicación funcional en el dominio de Vercel
- [ ] Todas las funcionalidades probadas

---

**¿Listo para desplegar?** 🚀

```bash
cd proyectoCG/image_inpainting_web
git add .
git commit -m "Ready for Vercel deployment"
git push origin main
```

Luego sigue las instrucciones en https://vercel.com/new
