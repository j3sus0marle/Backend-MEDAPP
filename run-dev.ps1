# Script para ejecutar el servidor FastAPI en modo desarrollo
Write-Host "Iniciando servidor FastAPI en modo desarrollo..." -ForegroundColor Green

# Verificar si existe el entorno virtual
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "ERROR: No se encuentra el entorno virtual en .venv\" -ForegroundColor Red
    Write-Host "Ejecuta primero: python -m venv .venv" -ForegroundColor Yellow
    Write-Host "Luego activa: .venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "E instala dependencias: pip install fastapi uvicorn motor python-dotenv python-multipart" -ForegroundColor Yellow
    exit 1
}

Write-Host "URL: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Recarga automática activada" -ForegroundColor Yellow
Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Red
Write-Host ""

# Ejecutar el servidor usando ruta relativa
& ".venv\Scripts\python.exe" -m uvicorn app:app --reload --host localhost --port 8000