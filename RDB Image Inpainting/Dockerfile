# Usar una imagen base de Ubuntu
FROM ubuntu:22.04

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    python3-pip \
    && apt-get clean

# Eliminar el enlace simbólico existente y crear uno nuevo para python3
RUN rm /usr/bin/python3 && ln -s /usr/bin/python3.10 /usr/bin/python3

# Copiar los archivos de requerimientos
COPY requirements.txt ./

# Instalar las dependencias
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación
COPY . .

# Instalar las dependencias del sistema
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Instalar OpenCV
RUN pip install opencv-python-headless

# Comando por defecto para ejecutar el contenedor
CMD ["bash"]