from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import base64
import sys
import os
from pathlib import Path

# Agregar el directorio API al path para importar módulos
api_dir = Path(__file__).parent
sys.path.insert(0, str(api_dir))

from src.aot_inpainting import AOTGANInpainter

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global inpainter (se inicializa lazy)
inpainter = None


def get_inpainter():
    """Lazy load del modelo"""
    global inpainter
    if inpainter is None:
        try:
            # Ruta al modelo - funciona igual que versión local
            # En Windows api/ y API/ son la misma carpeta (case-insensitive)
            # En Linux/Vercel necesitamos la ruta correcta del repo
            project_root = api_dir.parent if api_dir.name == "api" else api_dir
            model_path = project_root / "API" / "setup" / "experiments" / "CELEBA-HQ" / "G0000000.pt"
            
            if not model_path.exists():
                raise FileNotFoundError(f"Model not found at {model_path}")
            
            print(f"Loading model from {model_path}")
            device = "cpu"  # Vercel Serverless no tiene GPU
            inpainter = AOTGANInpainter(model_path=str(model_path), device=device, image_size=512)
            print(f"Model loaded successfully on {device}")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    return inpainter


@app.get("/api")
async def root():
    """Health check endpoint"""
    try:
        model = get_inpainter()
        return {
            "status": "running",
            "model": "AOT-GAN",
            "platform": "Vercel Serverless",
            "device": "cpu"
        }
    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": f"Model not loaded: {str(e)}"
        }, status_code=500)


@app.post("/api/upload")
async def upload_files(
    original_image: UploadFile = File(...),
    mask: UploadFile = File(...)
):
    """Perform image inpainting"""
    try:
        model = get_inpainter()
        
        # Read files
        original_content = await original_image.read()
        mask_content = await mask.read()

        # Convert to numpy arrays
        original_array = np.frombuffer(original_content, np.uint8)
        mask_array = np.frombuffer(mask_content, np.uint8)

        # Decode images
        img = cv2.imdecode(original_array, cv2.IMREAD_COLOR)
        mask_img = cv2.imdecode(mask_array, cv2.IMREAD_GRAYSCALE)
        
        if img is None or mask_img is None:
            return JSONResponse({
                "status": "error",
                "message": "Failed to decode images"
            }, status_code=400)
        
        print(f"Processing image: {img.shape}, mask: {mask_img.shape}")
        
        # Perform inpainting
        output_image = model.inpaint(img, mask_img)
        
        # Convert RGB to BGR for encoding
        output_image_bgr = cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR)
        
        # Encode to PNG
        _, buffer = cv2.imencode('.png', output_image_bgr)
        output_base64 = base64.b64encode(buffer).decode('utf-8')
        
        print("Inpainting completed successfully")
        
        return JSONResponse({
            "status": "success",
            "output_image": {
                "data": output_base64
            }
        })

    except Exception as e:
        print(f"Error during inpainting: {str(e)}")
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)


# Handler para Vercel
handler = app
