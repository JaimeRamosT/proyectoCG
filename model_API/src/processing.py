import numpy as np
import cv2
from src.inpainting import KerasNoNANUtil, dice_coef
from keras.models import load_model

SIZE = 64

def load_inpainting_model(model_path, custom_objects):
    return load_model(model_path, custom_objects=custom_objects)

def createMask(img, mask):
    masked_image = img.copy()
    masked_image[mask == 0] = 1
    return masked_image, mask

def inpaint_image(original_image, mask_cv2):
    resized_image = cv2.resize(original_image, (SIZE, SIZE))
    mask_resized = cv2.resize(mask_cv2, (SIZE, SIZE))  # Redimensionar la máscara a 64x64 si es necesario
    mask = np.stack([mask_resized] * 3, axis=-1)  # Convertir a una matriz 3 canales (64, 64, 3)
    mask = mask.astype(np.float32) / 255.0  # Escalar los valores a [0, 1] para mantener consistencia
    normalized_image = resized_image / 255.0

    input_image, input_mask = createMask(normalized_image, mask) #<--- Aqui la mascara es utilizada
    input_image = np.expand_dims(input_image, axis=0)
    input_mask = np.expand_dims(input_mask, axis=0)
    
    # Load model
    model_path = 'image_inpainting_model.h5'
    custom_objects = {'PConv2D': KerasNoNANUtil, 'dice_coef': dice_coef}
    model = load_inpainting_model(model_path, custom_objects)
    predicted_image = model.predict([input_image, input_mask])
    output_image = predicted_image.squeeze()
    output_image = (output_image * 255).astype(np.uint8)

    return resized_image, input_mask, input_image, output_image