# AOT-GAN Image Inpainting API

Esta API utiliza AOT-GAN (Aggregated Contextual Transformations for High-Resolution Image Inpainting) para realizar inpainting de imágenes de alta calidad.

## Características

- **Modelo AOT-GAN**: Arquitectura de vanguardia para inpainting de imágenes
- **Alta Resolución**: Trabaja con imágenes de 512x512 (escalable)
- **API REST**: Interfaz FastAPI rápida y moderna
- **Compatibilidad**: Diseñado para trabajar con el frontend de proyectoCG

## Requisitos Previos

### Modelo Pre-entrenado

Necesitas el modelo pre-entrenado de AOT-GAN. El archivo debe estar en:
```
../../AOT-GAN-for-Inpainting/experiments/CELEBA-HQ/G0000000.pt
```

O puedes especificar una ruta diferente modificando `main.py`.

### Dependencias del Sistema

- Python 3.10+
- CUDA (opcional, para GPU)

## Instalación

### 1. Crear entorno virtual (recomendado)

```bash
cd proyectoCG/model_API
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

**Nota**: Por defecto, se instalará PyTorch con soporte CUDA. Si solo quieres la versión CPU:

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

## Uso

### Desarrollo Local

```bash
# Desde el directorio proyectoCG/model_API
python main.py
```

O usando uvicorn directamente:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en: `http://localhost:8000`

### Documentación Interactiva

Una vez que la API esté corriendo, visita:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### `GET /`
Health check endpoint

**Respuesta:**
```json
{
  "status": "running",
  "model": "AOT-GAN",
  "device": "cuda" // o "cpu"
}
```

### `POST /upload/`
Realiza inpainting en una imagen

**Parámetros:**
- `original_image` (file): Imagen original
- `mask` (file): Máscara (áreas blancas serán rellenadas)

**Respuesta:**
```json
{
  "status": "success",
  "output_image": {
    "data": "base64_encoded_image..."
  }
}
```

## Docker

### Construir imagen

```bash
docker build -t aotgan-api .
```

### Ejecutar contenedor

```bash
# Con modelo local
docker run -p 8000:8000 \
  -v /path/to/model:/app/models \
  -e MODEL_PATH=/app/models/G0000000.pt \
  aotgan-api
```

## Estructura del Proyecto

```
API/
├── main.py                 # Aplicación FastAPI principal
├── requirements.txt        # Dependencias Python
├── Dockerfile             # Configuración Docker
├── src/
│   ├── aot_inpainting.py  # Módulo de inferencia AOT-GAN
│   ├── model/
│   │   ├── __init__.py
│   │   ├── common.py      # Redes base
│   │   └── aotgan.py      # Arquitectura del modelo
│   └── utils.py           # Utilidades (si es necesario)
└── README_API.md          # Este archivo
```

## Integración con Frontend

El frontend debe hacer una petición POST a `/upload/` con dos archivos:
1. La imagen original
2. La máscara (imagen donde las áreas blancas serán inpainted)

Ejemplo en JavaScript:

```javascript
const formData = new FormData();
formData.append("original_image", imageFile);
formData.append("mask", maskFile);

const response = await fetch("http://localhost:8000/upload/", {
  method: "POST",
  body: formData,
});

const result = await response.json();
// result.output_image.data contiene la imagen en base64
```

## Configuración del Frontend

En el frontend (`image_inpainting_web`), configura la URL de la API:

1. Para desarrollo local, edita `src/config/api.js`:
```javascript
development: {
  baseURL: 'http://localhost:8000',
}
```

2. Ejecuta el frontend en modo desarrollo:
```bash
npm run dev
```

## Resolución de Problemas

### Error: "Model not found"
Asegúrate de que el modelo pre-entrenado esté en la ruta correcta. Verifica la ruta en `main.py`:

```python
model_path = Path(r"c:\Users\HP\Desktop\wea\AOT-GAN-for-Inpainting\experiments\CELEBA-HQ\G0000000.pt")
```

### Error de CUDA
Si no tienes GPU, el modelo automáticamente usará CPU. Para forzar CPU:

```python
device = "cpu"
inpainter = create_inpainter(model_path=str(model_path), device=device)
```

### Memoria insuficiente
Reduce el tamaño de la imagen en `src/aot_inpainting.py`:

```python
self.image_size = 256  # en vez de 512
```

## Rendimiento

- **GPU (CUDA)**: ~1-2 segundos por imagen (512x512)
- **CPU**: ~5-15 segundos por imagen (512x512)

## Licencia

Este proyecto integra AOT-GAN, que está bajo licencia Apache 2.0.

## Referencias

- [AOT-GAN Paper](https://arxiv.org/abs/2104.01431)
- [AOT-GAN GitHub](https://github.com/researchmm/AOT-GAN-for-Inpainting)
