# main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
from keras.models import load_model
import base64
from io import BytesIO
from PIL import Image
from src.utils import display_results
from src.inpainting import PConv2D, dice_coef
import tensorflow as tf
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array


app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once at startup
custom_objects = {'PConv2D': PConv2D, 'dice_coef': dice_coef}
inpainting_model = load_model('image_inpainting_model.h5', custom_objects=custom_objects)
sr_model = tf.keras.models.load_model('resolution_enhancer_model.h5')

def enhance_resolution(image):
    """Apply super-resolution to image"""
    # Convert to PIL Image
    pil_image = Image.fromarray(image)
    
    # Convert to YCbCr
    ycbcr = pil_image.convert("YCbCr")
    y, cb, cr = ycbcr.split()
    
    # Process Y channel
    y = img_to_array(y)
    y = y.astype("float32") / 255.0
    input_sr = np.expand_dims(y, axis=0)
    
    # Predict
    output_sr = sr_model.predict(input_sr)[0]
    
    # Post-process
    output_sr = (output_sr * 255.0).clip(0, 255)
    output_sr = output_sr.reshape((output_sr.shape[0], output_sr.shape[1]))
    output_sr = Image.fromarray(np.uint8(output_sr))
    
    # Resize Cb and Cr
    cb = cb.resize(output_sr.size, Image.Resampling.BICUBIC)
    cr = cr.resize(output_sr.size, Image.Resampling.BICUBIC)
    
    # Merge channels
    enhanced = Image.merge("YCbCr", (output_sr, cb, cr))
    enhanced = enhanced.convert("RGB")
    
    return np.array(enhanced)


def process_image(image_array):
    """Preprocess image for model"""
    resized = cv2.resize(image_array, (64, 64))
    return resized / 255.0

def process_mask(mask_array):
    """Process mask for model"""
    resized = cv2.resize(mask_array, (64, 64))
    # Convert to binary mask
    _, binary_mask = cv2.threshold(resized, 127, 1, cv2.THRESH_BINARY)
    return np.stack([binary_mask] * 3, axis=-1)

@app.post("/upload/")
async def upload_files(
    original_image: UploadFile = File(...),
    mask: UploadFile = File(...)
):
    try:
        # Read files
        original_content = await original_image.read()
        mask_content = await mask.read()

        # Convert to numpy arrays
        original_array = np.frombuffer(original_content, np.uint8)
        mask_array = np.frombuffer(mask_content, np.uint8)

        # Decode images
        img = cv2.imdecode(original_array, cv2.IMREAD_COLOR)
        mask_img = cv2.imdecode(mask_array, cv2.IMREAD_GRAYSCALE)

        # Process images
        processed_img = process_image(img)
        processed_mask = process_mask(mask_img)

        # Prepare for model
        input_image = np.expand_dims(processed_img, axis=0)
        input_mask = np.expand_dims(processed_mask, axis=0)

        # Generate inpainting prediction
        predicted = inpainting_model.predict([input_image, input_mask])
        output_image = predicted.squeeze()
        output_image = (output_image * 255).astype(np.uint8)
        
        # Enhance resolution
        enhanced_image = enhance_resolution(output_image)
        
        # Convert to base64
        _, buffer = cv2.imencode('.png', enhanced_image)
        output_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return JSONResponse({
            "status": "success",
            "output_image": {
                "data": output_base64
            }
        })

    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)