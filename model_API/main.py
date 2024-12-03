import base64
from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
import cv2
from src.processing import createMask, inpaint_image

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir estas fuentes
    allow_credentials=True, # Permitir envío de credenciales (cookies, auth headers)
    allow_methods=["*"],    # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],    # Permitir todos los encabezados
)


@app.get("/")
def read_root():
    return {"msg": "Hello world"}


@app.post("/upload/")
async def upload_images(
    original_image: UploadFile = File(...),
    mask: UploadFile = File(...)
):
    try:
        # Leer el contenido de las imágenes subidas
        original_image_content = await original_image.read()
        mask_content = await mask.read()
        
        # Convertir el contenido a arrays de NumPy
        original_image_array = np.frombuffer(original_image_content, np.uint8)
        mask_array = np.frombuffer(mask_content, np.uint8)
        
        # Leer las imágenes usando OpenCV
        original_image_cv2 = cv2.imdecode(original_image_array, cv2.IMREAD_COLOR)  # Leer como imagen en color
        mask_cv2 = cv2.imdecode(mask_array, cv2.IMREAD_GRAYSCALE)  # Leer como escala de grises (opcional)

        # Verificar que las imágenes se hayan leído correctamente
        if original_image_cv2 is None or mask_cv2 is None:
            return JSONResponse(
                content={"message": "Error al decodificar las imágenes con OpenCV"},
                status_code=400,
            )

        # Procesar imagenes y generar prediccion del modelo
        _, _, masked_image, output_image = inpaint_image(original_image_cv2, mask_cv2)
        
        # Convertir las imágenes procesadas a Base64
        # _, masked_image_encoded = cv2.imencode('.png', masked_image)
        _, output_image_encoded = cv2.imencode('.png', output_image)

        # masked_image_base64 = base64.b64encode(masked_image_encoded).decode('utf-8')
        output_image_base64 = base64.b64encode(output_image_encoded).decode('utf-8')

        # Devolver información sobre ambas imágenes como ejemplo
        return JSONResponse(content={
            "message": "Imágenes procesadas con éxito usando OpenCV",
            # "masked_image": {
            #     "shape": masked_image.shape,
            #     "dtype": str(masked_image.dtype),
            #     "data": masked_image_base64
            # },
            "output_image": {
                "shape": output_image.shape,
                "dtype": str(output_image.dtype),
                "data": output_image_base64
            }
        }, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": f"Error al procesar las imágenes: {str(e)}"}, status_code=500)