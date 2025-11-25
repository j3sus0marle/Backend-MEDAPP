from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

MONGO_URL = os.getenv("MONGO_URI", "mongodb+srv://omarleal_db_user:sBq4WiRLEe1NhCkH@cluster0.zv5i3qo.mongodb.net/APPMEDDB")
DATABASE_NAME = "APPMEDDB"

client = AsyncIOMotorClient(MONGO_URL)
database = client[DATABASE_NAME]

# Colecciones
campo_info_collection = database.get_collection("Campo_Informativo")
info_pack_collection = database.get_collection("Paquete_Informacion")
regiones_collection = database.get_collection("Region")
users_collection = database.get_collection("User")