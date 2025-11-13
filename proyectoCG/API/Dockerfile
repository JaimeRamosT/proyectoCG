# Usar una imagen base de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para OpenCV, PyTorch y otras librerías
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar los archivos de requerimientos
COPY requirements.txt ./

# Instalar las dependencias de Python
# Para PyTorch CPU-only, usamos la versión sin CUDA para reducir tamaño
RUN pip install --upgrade pip && \
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY src ./src
COPY main.py ./

# Crear directorio para modelos si no existe
RUN mkdir -p models

# Nota: El modelo pre-entrenado debe ser copiado o montado como volumen
# COPY path/to/G0000000.pt ./models/

# Exponer el puerto para FastAPI
EXPOSE 8000

# Comando para ejecutar FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]