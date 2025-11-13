# Script de inicio rápido para proyectoCG
# Ejecutar desde: proyectoCG\start_all.ps1

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  AOT-GAN Integration Startup  " -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si estamos en el directorio correcto
if (-not (Test-Path "model_API") -or -not (Test-Path "image_inpainting_web")) {
    Write-Host "❌ Error: Ejecuta este script desde el directorio proyectoCG" -ForegroundColor Red
    Write-Host "   Directorio actual: $PWD" -ForegroundColor Yellow
    exit 1
}

Write-Host "📋 Verificando requisitos..." -ForegroundColor Yellow

# Verificar Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python no encontrado. Por favor instala Python 3.10+" -ForegroundColor Red
    exit 1
}

# Verificar Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js encontrado: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js no encontrado. Por favor instala Node.js" -ForegroundColor Red
    exit 1
}

# Verificar modelo
$modelPath = "..\AOT-GAN-for-Inpainting\experiments\CELEBA-HQ\G0000000.pt"
if (Test-Path $modelPath) {
    Write-Host "✅ Modelo AOT-GAN encontrado" -ForegroundColor Green
} else {
    Write-Host "⚠️  Modelo no encontrado en: $modelPath" -ForegroundColor Yellow
    Write-Host "   La API fallará al iniciar sin el modelo" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🚀 Iniciando servicios..." -ForegroundColor Yellow
Write-Host ""

# Iniciar Backend
Write-Host "1️⃣  Iniciando Backend API..." -ForegroundColor Cyan
$backendPath = "model_API"

# Crear entorno virtual si no existe
if (-not (Test-Path "$backendPath\venv")) {
    Write-Host "   Creando entorno virtual..." -ForegroundColor Yellow
    Set-Location $backendPath
    python -m venv venv
    Set-Location ..
}

# Script para backend
$backendScript = @"
Set-Location '$PWD\$backendPath'
.\venv\Scripts\Activate.ps1
Write-Host 'Instalando dependencias...' -ForegroundColor Yellow
pip install -q -r requirements.txt
Write-Host '✅ Backend iniciado en http://localhost:8000' -ForegroundColor Green
python start_api.py
"@

# Iniciar backend en nueva ventana
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript

Write-Host "   Esperando que el backend inicie..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Iniciar Frontend
Write-Host "2️⃣  Iniciando Frontend..." -ForegroundColor Cyan
$frontendPath = "image_inpainting_web"

# Instalar dependencias si no existen
if (-not (Test-Path "$frontendPath\node_modules")) {
    Write-Host "   Instalando dependencias de Node.js..." -ForegroundColor Yellow
    Set-Location $frontendPath
    npm install
    Set-Location ..
}

# Script para frontend
$frontendScript = @"
Set-Location '$PWD\$frontendPath'
Write-Host '✅ Frontend iniciado en http://localhost:5173' -ForegroundColor Green
npm run dev
"@

# Iniciar frontend en nueva ventana
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "  ✅ Servicios Iniciados!      " -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Backend API:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "🌐 Frontend UI:  http://localhost:5173" -ForegroundColor Cyan
Write-Host "📚 API Docs:     http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Abre tu navegador en http://localhost:5173 para usar la aplicación" -ForegroundColor Yellow
Write-Host ""
Write-Host "Para detener los servicios, cierra las ventanas de PowerShell abiertas" -ForegroundColor Gray
Write-Host ""

# Esperar un momento y abrir navegador
Start-Sleep -Seconds 3
Start-Process "http://localhost:5173"
