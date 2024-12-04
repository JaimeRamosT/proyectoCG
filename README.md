# Residual Dense Image Inpainting CNN

## Integrantes

- Ramos Talla, Jaime Alfonso
- Vásquez Vilchez, Juan Pedro
- Espinoza Hernandez, Gabriel Enrique

## Descripción del proyecto

Este proyecto consiste en la aplicación de modelos de aprendizaje automático para la tarea de Image Inpainting, utilizando una CNN que incorpora Residual Dense Blocks, Global Feature Fusion y Partial Convolutions.

## Instrucciones para ejecución del proyecto

### Paso 1: Clonar el repositorio

```sh
git clone https://github.com/JaimeRamosT/proyectoCG.git
cd proyectoCG
```

### Paso 2: Construir y ejecutar el contenedor Docker

```sh
cd API
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

## Preprocesamiento y Entrenamiento del Modelo

Para poder correr el preprocesamiento del dataset y el entrenamiento del modelo, sigue estos pasos:

1. Navega a la carpeta `RDB Image Inpainting`:
   ```sh
   cd RDB Image Inpainting
   ```

2. Asegúrate de que tu dataset esté dentro de esta carpeta `RDB Image Inpainting`. Las imágenes del dataset deben estar contenidas en una carpeta, del nombre que desees.

3. Construye la imagen Docker:
   ```sh
   docker build -t image_inpainting . 
   ```

4. Ejecuta un contenedor interactivo:
   ```sh
   docker run -it --rm -v ${PWD}/data:/app/data image_inpainting bash
   ```

5. Dentro del contenedor, podrás preprocesar el dataset para que sea compatible con el entrenamiento del modelo y entrenar el modelo en sí mismo.

   Para preprocesar el dataset:
   ```sh
   python cli.py preprocess "nombre_del_dataset" "data/nombre_del_dataset_procesado"
   ```

   Para entrenar el modelo:
   ```sh
   python cli.py train "data/nombre_del_dataset_procesado" --output "inpainting_model.h5" --epochs 100 --batch-size 16
   ```

## Preprocesamiento de Imágenes

Para preprocesar tu conjunto de datos de imágenes y convertirlas al formato RGB, utiliza el siguiente comando:

```sh
python cli.py preprocess <input_dir> <output_dir>
```

- `<input_dir>`: Directorio que contiene las imágenes de entrada.
- `<output_dir>`: Directorio donde se guardarán las imágenes procesadas.

Ejemplo:

```sh
python cli.py preprocess "data/raw_images" "data/processed_images"
```

## Entrenamiento del Modelo

Para entrenar el modelo de inpainting, utiliza el siguiente comando:

```sh
python cli.py train <dataset_path> --output <output_model_path> --epochs <num_epochs> --batch-size <batch_size>
```

- `<dataset_path>`: Ruta al conjunto de datos de entrenamiento.
- `<output_model_path>`: Ruta donde se guardará el modelo entrenado (por defecto: `image_inpainting_model.h5`).
- `<num_epochs>`: Número de épocas de entrenamiento (por defecto: 50).
- `<batch_size>`: Tamaño del lote para el entrenamiento (por defecto: 32).

Ejemplo:

```sh
python cli.py train data/processed_images --output models/inpainting_model.h5 --epochs 100 --batch-size 16
```

## Configuración

La configuración predeterminada del modelo se encuentra en el archivo `config.py`. Puedes modificar los parámetros según tus necesidades.

```python
default_config = {
    'image_size': (256, 256),
    'batch_size': 8,
    'epochs': 50,
    'learning_rate': 1e-4,
    'early_stopping_patience': 10,
    'lr_reduce_factor': 0.5,
    'lr_reduce_patience': 5,
    'loss_function': 'mse',
    'num_channels': 3,
    'num_rdbs': 3,
    'layers_per_rdb': 3
}
```
