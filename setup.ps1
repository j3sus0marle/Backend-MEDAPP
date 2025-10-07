# Script de configuración automática para Backend MEDAPP
Write-Host "=== Configuración automática de Backend MEDAPP ===" -ForegroundColor Cyan
Write-Host ""

# Verificar que Python esté instalado
try {
    $pythonVersion = python --version 2>$null
    Write-Host "✓ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Python no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "Instala Python desde: https://python.org" -ForegroundColor Yellow
    exit 1
}

# Crear entorno virtual si no existe
if (-not (Test-Path ".venv")) {
    Write-Host "📦 Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "✓ Entorno virtual creado" -ForegroundColor Green
} else {
    Write-Host "✓ Entorno virtual ya existe" -ForegroundColor Green
}

# Activar entorno virtual
Write-Host "🔄 Activando entorno virtual..." -ForegroundColor Yellow
& ".venv\Scripts\Activate.ps1"

# Instalar dependencias
Write-Host "📚 Instalando dependencias..." -ForegroundColor Yellow
& ".venv\Scripts\pip.exe" install fastapi uvicorn motor python-dotenv python-multipart

Write-Host ""
Write-Host "=== ✅ CONFIGURACIÓN COMPLETADA ===" -ForegroundColor Green
Write-Host ""
Write-Host "Para ejecutar el servidor:" -ForegroundColor Cyan
Write-Host "  npm run dev" -ForegroundColor White
Write-Host "  o" -ForegroundColor Gray
Write-Host "  ./run-dev.ps1" -ForegroundColor White
Write-Host ""
Write-Host "URLs importantes:" -ForegroundColor Cyan
Write-Host "  API: http://localhost:8000" -ForegroundColor White
Write-Host "  Docs: http://localhost:8000/docs" -ForegroundColor White