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
regiones_collection = database.get_collection("regiones")
users_collection = database.get_collection("users")

# Funciones para usuarios
async def get_user_by_email(email: str):
    return await users_collection.find_one({"email": email})

async def get_user_by_google_sub(google_sub: str):
    return await users_collection.find_one({"google_sub": google_sub})

async def create_user(user_data: dict):
    result = await users_collection.insert_one(user_data)
    created_user = await users_collection.find_one({"_id": result.inserted_id})
    return created_user

async def update_user_last_login(user_id: str):
    from bson import ObjectId
    await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"last_login": datetime.now(timezone.utc)}}  # ✅ AHORA FUNCIONA
    )

async def update_user_role(user_id: str, new_role: str):
    from bson import ObjectId
    result = await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"role": new_role}}
    )
    return result.modified_count > 0