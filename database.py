from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de MongoDB
MONGO_URL = os.getenv("MONGO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Cliente de MongoDB
client = AsyncIOMotorClient(MONGO_URL)
database = client[DATABASE_NAME]

# Colecciones
sintomas_collection = database.get_collection("Sintomas")