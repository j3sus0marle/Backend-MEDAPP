from database import  regiones_collection
from bson import ObjectId
from typing import List, Optional


class RegionController:
    # Para el modelo 3D - obtener región por meshName
    @staticmethod
    async def get_region_by_mesh_name(mesh_name: str):
        """
        Obtener información médica de una región del cuerpo por su meshName
        Para usar con el modelo 3D del frontend
        """
        # Buscar en la colección REGIONES por meshName
        region = await regiones_collection.find_one({"meshName": mesh_name})
                
        if not region:
            return None
            
        return {
            "id": str(region["_id"]),
            "meshName": region.get("meshName",""),
            "info_camp_id": str(region["info_camp_id"]) if region.get("info_camp_id") else None
        }
                
       

        # Health check para verificar conexión a la base de datos
    @staticmethod
    async def health_check():
        """
        Verificar estado de la base de datos
        """
        try:
            # Intentar una operación simple para verificar conexión
            await regiones_collection.find_one({})
            return {
                "status": "healthy",
                "database": "connected",
                "message": "Conexión a MongoDB establecida correctamente"
            }
        except Exception as e:
            return {
                "status": "unhealthy", 
                "database": "disconnected",
                "error": str(e),
                "message": "Error en la conexión a MongoDB"
            }