# Script para ejecutar el servidor FastAPI en modo desarrollo
Write-Host "Iniciando servidor FastAPI en modo desarrollo..." -ForegroundColor Green
Write-Host "URL: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Recarga automática activada" -ForegroundColor Yellow
Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Red
Write-Host ""

& "C:/Users/omar-/Documents/Codigos/Web/Backend-MEDAPP/.venv/Scripts/python.exe" -m uvicorn app:app --reload --host localhost --port 8000