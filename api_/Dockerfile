FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema para OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar (Railway usa $PORT)
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
