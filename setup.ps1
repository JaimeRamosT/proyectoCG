# Setup Script - Image Inpainting with AOT-GAN

Write-Host "🚀 Setting up Image Inpainting with AOT-GAN" -ForegroundColor Cyan
Write-Host ""

# Check Python version
$pythonVersion = python --version 2>&1
Write-Host "✓ Python: $pythonVersion" -ForegroundColor Green

# Check if .venv exists
if (Test-Path ".venv") {
    Write-Host "✓ Virtual environment exists at .venv" -ForegroundColor Green
} else {
    Write-Host "⚠ Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate venv and install dependencies
Write-Host ""
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
& ".venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
& ".venv\Scripts\python.exe" -m pip install -r requirements.txt --quiet

Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Check model
Write-Host ""
$modelPath = "API\setup\experiments\CELEBA-HQ\G0000000.pt"
if (Test-Path $modelPath) {
    $modelSize = [math]::Round((Get-Item $modelPath).Length / 1MB, 2)
    Write-Host "✓ Model found: $modelSize MB" -ForegroundColor Green
} else {
    Write-Host "⚠ Model not found at $modelPath" -ForegroundColor Yellow
    Write-Host "  The model will be downloaded on first API run" -ForegroundColor Gray
}

# Summary
Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "✨ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To run the project:" -ForegroundColor White
Write-Host "  Backend API:  cd API && ..\.venv\Scripts\python.exe main.py" -ForegroundColor Gray
Write-Host "  Frontend:     cd image_inpainting_web && npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "API will be at:      http://localhost:8000" -ForegroundColor White
Write-Host "Frontend will be at: http://localhost:5173" -ForegroundColor White
Write-Host "=" * 60 -ForegroundColor Cyan
