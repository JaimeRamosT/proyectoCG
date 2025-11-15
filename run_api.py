#!/usr/bin/env python
"""
Run the AOT-GAN Image Inpainting API
Usage: python run_api.py
"""

import subprocess
import sys
from pathlib import Path

def main():
    # Get the project root directory
    project_root = Path(__file__).parent
    api_dir = project_root / "API"
    
    # Path to Python in venv
    python_exe = project_root / ".venv" / "Scripts" / "python.exe"
    
    if not python_exe.exists():
        print("❌ Virtual environment not found!")
        print("Please run setup.ps1 first")
        sys.exit(1)
    
    # Change to API directory and run
    print("🚀 Starting AOT-GAN Image Inpainting API...")
    print(f"📁 API directory: {api_dir}")
    print(f"🐍 Python: {python_exe}")
    print("")
    print("API will be available at: http://localhost:8000")
    print("API documentation: http://localhost:8000/docs")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        subprocess.run(
            [str(python_exe), "main.py"],
            cwd=str(api_dir),
            check=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 API server stopped")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
