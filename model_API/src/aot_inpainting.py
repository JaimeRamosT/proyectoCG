import torch
import numpy as np
from PIL import Image
from torchvision.transforms import ToTensor, ToPILImage
import cv2
from pathlib import Path

from .model.aotgan import InpaintGenerator


class AOTGANInpainter:
    """
    Image inpainting processor
    """
    
    def __init__(self, model_path: str, device: str = "cuda", image_size: int = 512):
        """
        Initialize inpainting model
        
        Args:
            model_path: Path to the pre-trained model (.pt or .pth file)
            device: Device to run inference on ('cuda' or 'cpu')
            image_size: Size to resize images to (default: 512)
        """
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.image_size = image_size
        self.to_tensor = ToTensor()
        self.to_pil = ToPILImage()
        
        # Initialize model
        self.model = InpaintGenerator(block_num=8, rates=[1, 2, 4, 8])
        
        # Load pre-trained weights
        print(f"Loading model from: {model_path}")
        checkpoint = torch.load(model_path, map_location=self.device)
        
        # Handle different checkpoint formats
        if isinstance(checkpoint, dict):
            # If checkpoint contains 'state_dict' or other keys
            if 'state_dict' in checkpoint:
                state_dict = checkpoint['state_dict']
            elif 'generator' in checkpoint:
                state_dict = checkpoint['generator']
            elif 'model' in checkpoint:
                state_dict = checkpoint['model']
            else:
                # Assume the dict itself is the state dict
                state_dict = checkpoint
        else:
            # If checkpoint is directly the state dict
            state_dict = checkpoint
        
        # Remove 'module.' prefix if present (from DataParallel)
        new_state_dict = {}
        for k, v in state_dict.items():
            name = k.replace('module.', '') if k.startswith('module.') else k
            new_state_dict[name] = v
        
        self.model.load_state_dict(new_state_dict)
        self.model.to(self.device)
        self.model.eval()
        
        print(f"Model loaded successfully on {self.device}")
        print(f"Model loaded from {model_path} on {self.device}")
    
    def preprocess_image(self, image: np.ndarray) -> torch.Tensor:
        """
        Preprocess image for model input
        
        Args:
            image: Input image as numpy array (H, W, C) in BGR format (OpenCV default)
            
        Returns:
            Preprocessed image tensor in RGB, normalized to [-1, 1]
        """
        # CRITICAL: Convert BGR to RGB (OpenCV uses BGR, PyTorch expects RGB)
        if len(image.shape) == 3 and image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        elif len(image.shape) == 2:
            # Grayscale to RGB
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        
        # Convert to PIL Image
        pil_image = Image.fromarray(image.astype(np.uint8))
        
        # Resize to target size
        pil_image = pil_image.resize((self.image_size, self.image_size), Image.LANCZOS)
        
        # Convert to tensor and normalize to [-1, 1]
        image_tensor = self.to_tensor(pil_image)
        image_tensor = (image_tensor * 2.0 - 1.0)
        
        return image_tensor.unsqueeze(0)
    
    def preprocess_mask(self, mask: np.ndarray) -> torch.Tensor:
        """
        Preprocess mask for model input
        
        Args:
            mask: Input mask as numpy array (H, W) or (H, W, C)
                  Frontend sends BLACK (0) where to inpaint, WHITE (255) to keep
            
        Returns:
            Preprocessed mask tensor where 1 = inpaint, 0 = keep
        """
        # Convert to grayscale if needed
        if len(mask.shape) == 3:
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        
        mask = 255 - mask.astype(np.uint8)
        
        # Convert to PIL Image
        pil_mask = Image.fromarray(mask).convert('L')
        
        # Resize to target size
        pil_mask = pil_mask.resize((self.image_size, self.image_size), Image.LANCZOS)
        
        # Convert to tensor (0-1 range)
        mask_tensor = self.to_tensor(pil_mask)
        
        return mask_tensor.unsqueeze(0)
    
    def postprocess(self, tensor: torch.Tensor) -> np.ndarray:
        """
        Postprocess model output to numpy array
        
        Args:
            tensor: Output tensor from model
            
        Returns:
            Image as numpy array in RGB format
        """
        # Clamp to [-1, 1] and convert to [0, 1]
        tensor = torch.clamp(tensor, -1.0, 1.0)
        tensor = (tensor + 1.0) / 2.0
        
        # Convert to numpy array
        image = tensor.squeeze(0).permute(1, 2, 0).cpu().numpy()
        image = (image * 255.0).astype(np.uint8)
        
        return image
    
    @torch.no_grad()
    def inpaint(self, image: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """
        Perform image inpainting
        
        Args:
            image: Input image as numpy array (BGR format from OpenCV)
            mask: Input mask as numpy array (black=inpaint, white=keep)
            
        Returns:
            Inpainted image as numpy array in RGB format
        """
        # Store original size
        original_h, original_w = image.shape[:2]
        
        # Preprocess inputs
        image_tensor = self.preprocess_image(image).to(self.device)
        mask_tensor = self.preprocess_mask(mask).to(self.device)
        
        print(f"[DEBUG] Image tensor shape: {image_tensor.shape}, range: [{image_tensor.min():.2f}, {image_tensor.max():.2f}]")
        print(f"[DEBUG] Mask tensor shape: {mask_tensor.shape}, range: [{mask_tensor.min():.2f}, {mask_tensor.max():.2f}]")
        
        # Areas to inpaint are set to 1 (white), areas to keep show the original image
        masked_image = image_tensor * (1 - mask_tensor) + mask_tensor
        
        # Run inference
        predicted = self.model(masked_image, mask_tensor)
        
        print(f"[DEBUG] Predicted shape: {predicted.shape}, range: [{predicted.min():.2f}, {predicted.max():.2f}]")
        
        # Composite: use prediction for masked area, original for unmasked
        output = predicted * mask_tensor + image_tensor * (1 - mask_tensor)
        
        # Postprocess
        output_image = self.postprocess(output)
        
        # Resize back to original size
        output_image = cv2.resize(output_image, (original_w, original_h), interpolation=cv2.INTER_LANCZOS4)
        
        return output_image


def create_inpainter(model_path: str = None, device: str = "cuda") -> AOTGANInpainter:
    """
    Factory function to create inpainter instance
    
    Args:
        model_path: Path to pre-trained model. If None, uses default path
        device: Device to run on ('cuda' or 'cpu')
        
    Returns:
        Initialized AOTGANInpainter instance
    """
    if model_path is None:
        # Default model path - adjust as needed
        model_path = "../../AOT-GAN-for-Inpainting/experiments/CELEBA-HQ/G0000000.pt"
    
    return AOTGANInpainter(model_path=model_path, device=device)
