# Archivo principal para Vercel Serverless
import sys
sys.path.append('..')  # Permite importar desde la raíz
from app import app

# Vercel espera una variable llamada 'app' para FastAPI
# No necesitas cambiar nada más aquí