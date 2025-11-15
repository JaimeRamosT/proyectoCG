# main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import base64
import torch
from pathlib import Path
import logging

from src.aot_inpainting import create_inpainter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AOT-GAN Image Inpainting API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable for model
inpainter = None


@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    global inpainter
    
    try:
        # Ruta correcta del modelo en API/setup
        model_path = Path(__file__).parent / "setup" / "experiments" / "CELEBA-HQ" / "G0000000.pt"
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found at {model_path}")
        
        # Determine device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {device}")
        
        # Load model
        inpainter = create_inpainter(model_path=str(model_path), device=device)
        logger.info("AOT-GAN model loaded successfully!")
        
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        raise


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "model": "AOT-GAN",
        "device": str(inpainter.device) if inpainter else "not loaded"
    }


@app.get("/api")
async def api_health():
    """API health check endpoint (matches Vercel structure)"""
    return {
        "status": "running",
        "model": "AOT-GAN",
        "device": str(inpainter.device) if inpainter else "not loaded"
    }


@app.post("/api/upload")
async def upload_files(
    original_image: UploadFile = File(...),
    mask: UploadFile = File(...)
):
    """
    Perform image inpainting using AOT-GAN
    
    Args:
        original_image: Original image file
        mask: Mask file (white areas will be inpainted)
        
    Returns:
        JSON with inpainted image in base64 format
    """
    try:
        if inpainter is None:
            return JSONResponse({
                "status": "error",
                "message": "Model not loaded"
            }, status_code=500)
        
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
        
        logger.info(f"Processing image: {img.shape}, mask: {mask_img.shape}")
        logger.info(f"Image dtype: {img.dtype}, range: [{img.min()}, {img.max()}]")
        logger.info(f"Mask dtype: {mask_img.dtype}, range: [{mask_img.min()}, {mask_img.max()}]")
        
        # Perform inpainting using AOT-GAN (expects BGR, returns RGB)
        output_image = inpainter.inpaint(img, mask_img)
        
        # Convert RGB to BGR for encoding
        output_image_bgr = cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR)
        
        # Encode to PNG
        _, buffer = cv2.imencode('.png', output_image_bgr)
        output_base64 = base64.b64encode(buffer).decode('utf-8')
        
        logger.info("Inpainting completed successfully")
        
        return JSONResponse({
            "status": "success",
            "output_image": {
                "data": output_base64
            }
        })

    except Exception as e:
        logger.error(f"Error during inpainting: {str(e)}", exc_info=True)
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)