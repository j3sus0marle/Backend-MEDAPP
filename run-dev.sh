#!/bin/bash

# Script para ejecutar el servidor FastAPI en modo desarrollo (Linux/Mac)
echo "🚀 Iniciando servidor FastAPI en modo desarrollo..."

# Verificar si existe el entorno virtual
if [ ! -f ".venv/bin/python" ]; then
    echo "❌ ERROR: No se encuentra el entorno virtual en .venv/"
    echo "📦 Ejecuta primero: python -m venv .venv"
    echo "🔄 Luego activa: source .venv/bin/activate"
    echo "📚 E instala dependencias: pip install fastapi uvicorn motor python-dotenv python-multipart"
    exit 1
fi

echo "🌐 URL: http://localhost:8000"
echo "📖 Docs: http://localhost:8000/docs"
echo "🔄 Recarga automática activada"
echo "⏹️  Presiona Ctrl+C para detener"
echo ""

# Ejecutar el servidor usando ruta relativa
.venv/bin/python -m uvicorn app:app --reload --host localhost --port 8000