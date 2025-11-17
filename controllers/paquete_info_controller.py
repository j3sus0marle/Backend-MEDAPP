from database import info_pack_collection
from bson import ObjectId
from typing import List, Optional

class PaqueteInfoController:
    @staticmethod
    async def get_all_packs():
        """Obtener todos los paquetes de información"""
        packs = []
        async for pack in info_pack_collection.find():
            packs.append({
                "id": str(pack["_id"]),  # convertir ObjectId a str
                "textos": pack.get("textos", []),
                "audios": pack.get("audios", []),
                "imagenes": pack.get("imagenes", []),
                "videos": pack.get("videos", [])
            })
        return packs

    @staticmethod
    async def get_pack_by_id(pack_id: str):
        """Obtener paquete por ID"""
        if not ObjectId.is_valid(pack_id):
            return None
        pack = await info_pack_collection.find_one({"_id": ObjectId(pack_id)})
        if not pack:
            return None
        return {
            "id": str(pack["_id"]),  # convertir ObjectId a str
            "textos": pack.get("textos", []),
            "audios": pack.get("audios", []),
            "imagenes": pack.get("imagenes", []),
            "videos": pack.get("videos", [])
        }

    @staticmethod
    async def create_pack(
        textos: Optional[List[dict]] = None,
        audios: Optional[List[dict]] = None,
        imagenes: Optional[List[dict]] = None,
        videos: Optional[List[dict]] = None
    ):
        """Crear un nuevo paquete de información"""
        
        doc = {
        "textos": to_dict_list(textos),
        "audios": to_dict_list(audios),
        "imagenes": to_dict_list(imagenes),
        "videos": to_dict_list(videos)
        }

        result = await info_pack_collection.insert_one(doc)
        new_pack = await info_pack_collection.find_one({"_id": result.inserted_id})

        return {
            "id": str(new_pack["_id"]),
            "textos": new_pack.get("textos", []),
            "audios": new_pack.get("audios", []),
            "imagenes": new_pack.get("imagenes", []),
            "videos": new_pack.get("videos", [])
        }

    @staticmethod
    async def update_pack(
        pack_id: str,
        textos: Optional[List[dict]] = None,
        audios: Optional[List[dict]] = None,
        imagenes: Optional[List[dict]] = None,
        videos: Optional[List[dict]] = None
    ):
        """Actualizar un paquete de información"""
        if not ObjectId.is_valid(pack_id):
            return None

        update_data = {}
        if textos is not None:
            update_data["textos"] = to_dict_list(textos)
        if audios is not None:
            update_data["audios"] = to_dict_list(audios)
        if imagenes is not None:
            update_data["imagenes"] = to_dict_list(imagenes)
        if videos is not None:
            update_data["videos"] = to_dict_list(videos)

        if not update_data:
            return None  # nada que actualizar

        result = await info_pack_collection.update_one(
            {"_id": ObjectId(pack_id)},
            {"$set": update_data}
        )

        if result.modified_count > 0:
            updated_pack = await info_pack_collection.find_one({"_id": ObjectId(pack_id)})
            return {
                "id": str(updated_pack["_id"]),
                "textos": updated_pack.get("textos", []),
                "audios": updated_pack.get("audios", []),
                "imagenes": updated_pack.get("imagenes", []),
                "videos": updated_pack.get("videos", [])
            }
        return None

    @staticmethod
    async def delete_pack(pack_id: str):
        """Eliminar un paquete de información"""
        if not ObjectId.is_valid(pack_id):
            return False
        result = await info_pack_collection.delete_one({"_id": ObjectId(pack_id)})
        return result.deleted_count > 0


def to_dict_list(items):
    if not items:
        return []
    result = []
    for i in items:
        if isinstance(i, dict):
            result.append(i)
        else:
            # Convierte el modelo Pydantic a dict
            result.append(i.model_dump())
    return result