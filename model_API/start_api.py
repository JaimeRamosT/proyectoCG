#!/usr/bin/env python
"""
Startup script for AOT-GAN Image Inpainting API
"""
import sys
from pathlib import Path

def check_model_exists():
    """Check if the pre-trained model exists"""
    possible_paths = [
        Path(__file__).parent.parent / "API" / "setup" / "experiments" / "CELEBA-HQ" / "G0000000.pt",
        Path(__file__).parent.parent / "AOT-GAN-for-Inpainting" / "experiments" / "CELEBA-HQ" / "G0000000.pt",
        Path(r"c:\Users\HP\Desktop\wea\AOT-GAN-for-Inpainting\experiments\CELEBA-HQ\G0000000.pt"),
        Path("models/G0000000.pt"),
    ]
    
    for path in possible_paths:
        if path.exists():
            print(f"✓ Model found at: {path}")
            return True
    
    print("✗ Model not found in any of the following locations:")
    for path in possible_paths:
        print(f"  - {path}")
    print("\nPlease download the pre-trained model from:")
    print("https://drive.google.com/drive/folders/1Zks5Hyb9WAEpupbTdBqsCafmb25yqsGJ?usp=sharing")
    return False

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import torch
        import torchvision
        import fastapi
        import cv2
        print("✓ All dependencies are installed")
        print(f"  - PyTorch version: {torch.__version__}")
        print(f"  - CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"  - CUDA device: {torch.cuda.get_device_name(0)}")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("\nPlease install dependencies:")
        print("  pip install -r requirements.txt")
        return False

def main():
    """Main startup function"""
    print("=" * 60)
    print("AOT-GAN Image Inpainting API - Startup Check")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check model
    if not check_model_exists():
        print("\nNote: The API will fail to start without a model.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    print("\n" + "=" * 60)
    print("Starting API server...")
    print("=" * 60)
    print("API will be available at: http://localhost:8000")
    print("API documentation: http://localhost:8000/docs")
    print("Press Ctrl+C to stop")
    print("=" * 60 + "\n")
    
    # Start uvicorn
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
