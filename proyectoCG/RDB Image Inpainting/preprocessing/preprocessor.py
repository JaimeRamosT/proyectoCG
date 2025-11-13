import os
from PIL import Image
import shutil
from pathlib import Path
import logging

class ImagePreprocessor:
    def __init__(self):
        self.valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
        self.logger = logging.getLogger(__name__)

    def process_dataset(self, input_dir, output_dir):
        """Process image dataset and convert to RGB format"""
        input_path = Path(input_dir).resolve()
        output_path = Path(output_dir).resolve()
        
        # Validar que los directorios sean diferentes
        if input_path == output_path:
            raise ValueError("Input and output directories must be different")
            
        output_path.mkdir(parents=True, exist_ok=True)
        
        total_images = 0
        rgb_images = 0
        
        for filename in os.listdir(input_dir):
            if any(filename.lower().endswith(ext) for ext in self.valid_extensions):
                total_images += 1
                input_path = os.path.join(input_dir, filename)
                
                try:
                    self._process_single_image(input_path, output_dir, filename)
                    rgb_images += 1
                except Exception as e:
                    self.logger.error(f"Error processing {filename}: {str(e)}")
        
        return total_images, rgb_images

    def _process_single_image(self, input_path, output_dir, filename):
        """Process a single image file"""
        with Image.open(input_path) as img:
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            if img.mode == 'RGB':
                output_path = os.path.join(output_dir, filename)
                shutil.copy2(input_path, output_path)
            else:
                raise ValueError(f"Unsupported image mode: {img.mode}")