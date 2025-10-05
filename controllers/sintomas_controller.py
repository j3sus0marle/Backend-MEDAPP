from database import sintomas_collection
from bson import ObjectId
from typing import List, Optional

class SintomasController:
    @staticmethod
    async def get_all_sintomas():
        """Obtener todos los síntomas de la base de datos"""
        sintomas = []
        async for sintoma in sintomas_collection.find():
            sintomas.append({
                "id": str(sintoma["_id"]),
                "numero": sintoma.get("numero", 0),
                "nombre": sintoma["nombre"]
            })
        return sintomas
    
    @staticmethod
    async def get_sintoma_by_id(sintoma_id: str):
        """Obtener síntoma por número"""
        try:
            # Intentar buscar por número primero
            numero = int(sintoma_id)
            sintoma = await sintomas_collection.find_one({"numero": numero})
            
            if sintoma:
                return {
                    "id": str(sintoma["_id"]),
                    "numero": sintoma.get("numero", 0),
                    "nombre": sintoma["nombre"]
                }
            return None
        except ValueError:
            # Si no es un número, intentar buscar por ObjectId
            try:
                sintoma = await sintomas_collection.find_one({"_id": ObjectId(sintoma_id)})
                if sintoma:
                    return {
                        "id": str(sintoma["_id"]),
                        "numero": sintoma.get("numero", 0),
                        "nombre": sintoma["nombre"]
                    }
                return None
            except:
                return None
    
    @staticmethod
    async def create_sintoma(nombre: str):
        """Crear nuevo síntoma"""
        # Obtener el siguiente número
        last_sintoma = await sintomas_collection.find_one(sort=[("numero", -1)])
        next_numero = (last_sintoma.get("numero", 0) + 1) if last_sintoma else 1
        
        result = await sintomas_collection.insert_one({
            "numero": next_numero,
            "nombre": nombre
        })
        new_sintoma = await sintomas_collection.find_one({"_id": result.inserted_id})
        return {
            "id": str(new_sintoma["_id"]),
            "numero": new_sintoma["numero"],
            "nombre": new_sintoma["nombre"]
        }
    
    @staticmethod
    async def update_sintoma(sintoma_id: str, nombre: str):
        try:
            # Intentar buscar por número primero
            if sintoma_id.isdigit():
                filtro = {"numero": int(sintoma_id)}
            else:
                # Si no es número, buscar por ObjectId
                filtro = {"_id": ObjectId(sintoma_id)}
            
            # Actualizar el documento
            result = await sintomas_collection.update_one(
                filtro,
                {"$set": {"nombre": nombre}}
            )
            
            if result.modified_count > 0:
                # Devolver el documento actualizado
                updated_sintoma = await sintomas_collection.find_one(filtro)
                return {
                    "id": str(updated_sintoma["_id"]),
                    "numero": updated_sintoma["numero"],
                    "nombre": updated_sintoma["nombre"]
                }
            return None
        except Exception as e:
            raise e