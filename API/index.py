from http.server import BaseHTTPRequestHandler
import json
import numpy as np
import cv2
import base64
import sys
from pathlib import Path
from io import BytesIO
import cgi

# Agregar el directorio API al path para importar módulos
api_dir = Path(__file__).parent
sys.path.insert(0, str(api_dir))

from src.aot_inpainting import AOTGANInpainter

# Global inpainter (se inicializa lazy)
inpainter = None

def get_inpainter():
    """Lazy load del modelo"""
    global inpainter
    if inpainter is None:
        try:
            project_root = api_dir.parent if api_dir.name == "api" else api_dir
            model_path = project_root / "api" / "setup" / "experiments" / "CELEBA-HQ" / "G0000000.pt"
            
            if not model_path.exists():
                raise FileNotFoundError(f"Model not found at {model_path}")
            
            print(f"Loading model from {model_path}")
            device = "cpu"
            inpainter = AOTGANInpainter(model_path=str(model_path), device=device, image_size=512)
            print(f"Model loaded successfully on {device}")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    return inpainter

class handler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_OPTIONS(self):
        self._set_headers(200)
        
    def do_GET(self):
        try:
            model = get_inpainter()
            self._set_headers(200)
            response = {
                "status": "running",
                "model": "AOT-GAN",
                "platform": "Vercel Serverless",
                "device": "cpu"
            }
            self.wfile.write(json.dumps(response).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({
                "status": "error",
                "message": str(e)
            }).encode())
    
    def do_POST(self):
        try:
            # Parse multipart form data
            content_type = self.headers['Content-Type']
            if 'multipart/form-data' not in content_type:
                self._set_headers(400)
                self.wfile.write(json.dumps({
                    "status": "error",
                    "message": "Content-Type must be multipart/form-data"
                }).encode())
                return
            
            # Get content length
            content_length = int(self.headers['Content-Length'])
            
            # Parse form data
            form_data = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': content_type,
                }
            )
            
            # Get files
            original_image = form_data['original_image'].file.read()
            mask = form_data['mask'].file.read()
            
            # Load model
            model = get_inpainter()
            
            # Convert to numpy arrays
            original_array = np.frombuffer(original_image, np.uint8)
            mask_array = np.frombuffer(mask, np.uint8)
            
            # Decode images
            img = cv2.imdecode(original_array, cv2.IMREAD_COLOR)
            mask_img = cv2.imdecode(mask_array, cv2.IMREAD_GRAYSCALE)
            
            if img is None or mask_img is None:
                self._set_headers(400)
                self.wfile.write(json.dumps({
                    "status": "error",
                    "message": "Failed to decode images"
                }).encode())
                return
            
            print(f"Processing image: {img.shape}, mask: {mask_img.shape}")
            
            # Perform inpainting
            output_image = model.inpaint(img, mask_img)
            
            # Convert RGB to BGR for encoding
            output_image_bgr = cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR)
            
            # Encode to PNG
            _, buffer = cv2.imencode('.png', output_image_bgr)
            output_base64 = base64.b64encode(buffer).decode('utf-8')
            
            print("Inpainting completed successfully")
            
            self._set_headers(200)
            self.wfile.write(json.dumps({
                "status": "success",
                "output_image": {
                    "data": output_base64
                }
            }).encode())
            
        except Exception as e:
            print(f"Error during inpainting: {str(e)}")
            import traceback
            traceback.print_exc()
            self._set_headers(500)
            self.wfile.write(json.dumps({
                "status": "error",
                "message": str(e)
            }).encode())
