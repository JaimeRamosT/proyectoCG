# Run Frontend - Image Inpainting Web UI
# Usage: .\run_frontend.ps1

Write-Host "🚀 Starting Frontend Development Server..." -ForegroundColor Cyan
Write-Host ""

$frontendDir = "image_inpainting_web"

if (-not (Test-Path $frontendDir)) {
    Write-Host "❌ Frontend directory not found: $frontendDir" -ForegroundColor Red
    exit 1
}

# Check if node_modules exists
if (-not (Test-Path "$frontendDir\node_modules")) {
    Write-Host "📦 Installing npm dependencies..." -ForegroundColor Yellow
    Set-Location $frontendDir
    npm install
    Set-Location ..
}

Write-Host "Frontend will be available at: http://localhost:5173" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ("=" * 60) -ForegroundColor Cyan
Write-Host ""

Set-Location $frontendDir
npm run dev
