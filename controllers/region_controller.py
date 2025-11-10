from database import  regiones_collection,campo_info_collection,info_pack_collection
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
        #print(region) 
        
        #Buscar campo de info que pertenece
        info_campo = await campo_info_collection.find_one({"_id":ObjectId(str(region["info_camp_id"]))})
        #print(info_campo)
         
        #buscar info que pertenece
        info_paquete = await info_pack_collection.find_one({"_id":ObjectId(str(info_campo["info_pack_id"]))})
        #print(info_paquete) 
        
        data = RegionController.data2Info(region,info_campo,info_paquete)
        
        if (not region) or (not info_campo) or (not info_paquete):
            return None
        
        return {
        "region_name": data.get("region_name",""),
        "titulo": data.get("titulo",""),
        "contenido":data.get("contenido"),
        "terminos_relacionados":data.get("terminos_relacionados",[])    
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
            
    def data2Info(region,info_campo,info_paquete):
        
        contenido = []

        for tipo, lista in [
            ("audio", info_paquete.get("audios", [])),
            ("texto", info_paquete.get("textos", [])),
            ("video", info_paquete.get("videos", [])),
            ("imagen", info_paquete.get("imagenes", []))
        ]:
            for item in lista:
                contenido.append({
                "tipo": tipo,
                "titulo": item.get("titulo") or item.get("subtitulo"),
                "info": item.get("link") or item.get("texto"),
                "lugar": item.get("lugar", 0)
                })

        # Ordenar por "lugar"
        contenido.sort(key=lambda x: x["lugar"])
        
        return {
        "region_name": region.get("meshName",""),
        "titulo": info_campo.get("titulo",""),
        "contenido":contenido,
        "terminos_relacionados":info_campo.get("terminos_relacionados")    
        } 
       
     
    
        