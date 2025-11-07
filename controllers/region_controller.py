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
        try:
            # Buscar en la colección REGIONES por meshName
            region = await regiones_collection.find_one({"meshName": mesh_name})
                
            if not region:
                # Si no existe, devolver información por defecto
                return {
                    "name": mesh_name,
                    "description": "Información médica no disponible para esta región.",
                    "commonIssues": ["Consulta médica requerida para evaluación específica"],
                    "recommendations": ["Acudir a valoración médica especializada"],
                    "specialists": ["Médico general"]
                }
                
                # Convertir a formato que espera el frontend del modelo 3D
            return {
                "name": region.get("name", mesh_name),
                "description": region.get("description", "Descripción no disponible."),
                "commonIssues": region.get("commonIssues", []),
                "recommendations": region.get("recommendations", []),
                "specialists": region.get("specialists", [])
            }
                
        except Exception as e:
            # En caso de error, devolver información por defecto
            return {
                "name": mesh_name,
                "description": "Error al cargar información desde la base de datos.",
                "commonIssues": ["No se pudo cargar la información médica"],
                "recommendations": ["Intente nuevamente más tarde"],
                "specialists": ["Médico general"]
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