from database import campo_info_collection, info_pack_collection
from bson import ObjectId
from typing import List, Optional

class CampoInfoController:
    
    @staticmethod
    async def get_all_campos():
        """Obtener todos los campos informativos"""
        campos = []
        async for campo in campo_info_collection.find():
            campos.append({
                "id": str(campo["_id"]),
                "titulo": campo.get("titulo", ""),
                "terminos_relacionados": campo.get("terminos_relacionados", []),
                "info_pack_id": str(campo["info_pack_id"]) if campo.get("info_pack_id") else None
            })
        return campos

    @staticmethod
    async def get_campo_by_id(campo_id: str):
        """Obtener campo por ID y agregar info completa del info_pack si existe"""
        try:
            # Buscar el campo informativo
            campo = await campo_info_collection.find_one({"_id": ObjectId(campo_id)})
            if not campo:
                return None
                
            # Construir respuesta limpia (sin ObjectId)
            return {
                "id": str(campo["_id"]),
                "titulo": campo.get("titulo", ""),
                "terminos_relacionados": campo.get("terminos_relacionados", []),
                "info_pack_id": str(campo["info_pack_id"]) if campo.get("info_pack_id") else None,
            }

        except Exception as e:
            raise e
        
    
    @staticmethod
    async def create_campo(
    titulo: str,
    terminos_relacionados: Optional[List[dict]] = None,
    info_pack_id: Optional[str] = None
    ):
        """Crear nuevo campo informativo"""

        doc = {
        "titulo": titulo,
        "terminos_relacionados": terminos_relacionados or []
        }

        if info_pack_id and ObjectId.is_valid(info_pack_id):
            doc["info_pack_id"] = ObjectId(info_pack_id)

        result = await campo_info_collection.insert_one(doc)
        new_campo = await campo_info_collection.find_one({"_id": result.inserted_id})
        
        return {
        "id": str(new_campo["_id"]),
        "titulo": new_campo.get("titulo", ""),
        "terminos_relacionados": new_campo.get("terminos_relacionados", []),
        "info_pack_id": str(new_campo.get("info_pack_id")) if new_campo.get("info_pack_id") else None
        }

    @staticmethod
    async def update_campo(campo_id: str, titulo: Optional[str] = None, terminos_relacionados: Optional[List[dict]] = None, info_pack_id: Optional[str] = None):
        """Actualizar un campo informativo"""
        try:
            filtro = {"_id": ObjectId(campo_id)}
            update_data = {}
            if titulo is not None:
                update_data["titulo"] = titulo
            if terminos_relacionados is not None:
                update_data["terminos_relacionados"] = terminos_relacionados
            if info_pack_id is not None:
                update_data["info_pack_id"] = ObjectId(info_pack_id)
            
            if not update_data:
                return None  # Nada que actualizar

            result = await campo_info_collection.update_one(filtro, {"$set": update_data})
            if result.modified_count > 0:
                updated_campo = await campo_info_collection.find_one(filtro)
                return {
                    "id": str(updated_campo["_id"]),
                    "titulo": updated_campo.get("titulo", ""),
                    "terminos_relacionados": updated_campo.get("terminos_relacionados", []),
                    "info_pack_id": str(updated_campo["info_pack_id"]) if updated_campo.get("info_pack_id") else None
                }
            return None
        except Exception as e:
            raise e

    @staticmethod
    async def delete_campo(campo_id: str):
        """Eliminar un campo informativo"""
        try:
            result = await campo_info_collection.delete_one({"_id": ObjectId(campo_id)})
            return result.deleted_count > 0
        except:
            return False