# Proyecto - Mejora de calidad de imágenes

## Integrantes

- Ramos Talla, Jaime Alfonso
- Vásquez Vilchez, Juan Pedro
- Espinoza Hernandez, Gabriel Enrique

## Descripción del proyecto

Este proyecto consiste en la aplicación de modelos de aprendizaje automático que permitan mejorar la calidad de imágenes, con un enfoque en el procesamiento de imágenes basado en redes neuronales.

## Instrucciones para ejecución del proyecto

### Paso 1: Clonar el repositorio

```sh
git clone https://github.com/JaimeRamosT/proyectoCG.git
cd proyectoCG
```

### Paso 2: Construir y ejecutar el contenedor Docker

```sh
cd model_API
docker build -t image_inpainting_model .
docker run -p 8000:8000 image_inpainting_model
```

### Paso 3: Ejecutar la aplicación web

En otra terminal, navega a la carpeta image_inpainting_web y ejecuta los siguientes comandos:

```sh
cd image_inpainting_web
npm install
npm run dev
```

### Paso 4: Acceder a la aplicación

Abre tu navegador web y navega a <http://localhost:5173> para acceder a la aplicación web. Aquí podrás cargar una imagen, dibujar una máscara y enviar la imagen al modelo para su procesamiento.

## Uso de la API

La API está disponible en <http://localhost:8000/upload/>. Puedes enviar una solicitud POST con los siguientes parámetros:

- original_image: La imagen original que deseas procesar.
- mask: La máscara que indica las áreas a mejorar.
Ejemplo de solicitud con curl:

```sh
curl -X POST "http://localhost:8000/upload/" -F "original_image=@ruta/a/tu/imagen.jpg" -F "mask=@ruta/a/tu/mascara.png"
```
