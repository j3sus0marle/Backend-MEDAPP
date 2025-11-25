import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from bson import ObjectId

# Configuración
MONGO_URI = "mongodb://localhost:27017"  # Cambia por tu URI de Atlas
DB_NAME = "tu_base_de_datos"

# Nombres reales en MongoDB Atlas
COLECCIONES = {
    "User": {},
    "Region": {},
    "Paquete_Informacion": {},
    "Campo_Informativo": {}
}

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]


async def init_db():
    print("🚀 Inicializando base de datos...")

    existentes = await db.list_collection_names()

    # ---------- CREAR COLECCIONES ----------
    for nombre in COLECCIONES.keys():
        if nombre not in existentes:
            await db.create_collection(nombre)
            print(f"Colección '{nombre}' creada")
        else:
            print(f"Colección '{nombre}' ya existe")

    # ---------- DATOS DE EJEMPLO ----------

    # User
    user_example = {
        "_id": ObjectId(),
        "email": "demo@ejemplo.com",
        "name": "Usuario Demo",
        "google_sub": "1234567890",
        "role": "Admin",
        "is_active": True,
        "created_at": datetime.utcnow(),
        "last_login": datetime.utcnow()
    }

    # Paquete_Informacion
    info_pack_example = {
    "textos": [
        {
            "subtitulo": "Introducción",
            "lugar": 1,
            "texto": "Este es un texto de ejemplo para el paquete de información."
        }
    ],
    "audios": [
        {
            "titulo": "Audio introductorio",
            "lugar": 2,
            "link": "http://localhost:5000/audios/intro_cabeza.mp3"
        }
    ],
    "imagenes": [
        {
            "titulo": "Imagen ejemplo 1",
            "lugar": 3,
            "link": "http://localhost:5000/imagenes/ver/cabeza_ejemplo_1.png"
        },
        {
            "titulo": "Imagen ejemplo 2",
            "lugar": 4,
            "link": "http://localhost:5000/imagenes/ver/cabeza_ejemplo_2.png"
        }
    ],
    "videos": [
        {
            "titulo": "Video introductorio",
            "lugar": 5,
            "link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        }
        ]
    }

    # Campo_Informativo
    campo_info_example = {
        "_id": ObjectId(),
        "titulo": "Ejemplo Campo",
        "terminos_relacionados": [
            {"nombre": "Ejemplo", "tipo": "Demo"}
        ],
        "info_pack_id": info_pack_example["_id"]
    }

    # Region
    region_example = {
        "_id": ObjectId(),
        "meshName": "Region_Ejemplo",
        "info_camp_id": campo_info_example["_id"]
    }

    # ---------- INSERTAR SOLO SI ESTÁN VACÍAS ----------
    async def insert_if_empty(nombre, data):
        collection = db[nombre]
        count = await collection.count_documents({})
        if count == 0:
            await collection.insert_one(data)
            print(f"Dato de ejemplo insertado en '{nombre}'")
        else:
            print(f"'{nombre}' ya tiene datos, se omitió insert")

    await insert_if_empty("User", user_example)
    await insert_if_empty("Paquete_Informacion", info_pack_example)
    await insert_if_empty("Campo_Informativo", campo_info_example)
    await insert_if_empty("Region", region_example)

    print("Base de datos inicializada correctamente")


if __name__ == "__main__":
    asyncio.run(init_db())