from fastapi.testclient import TestClient
import app
from controllers import region_controller
client = TestClient(app.app)

def test_get_region_info(monkeypatch):
    """Debe retornar la información de una región médica por meshName."""

    async def fake_get_region_by_mesh_name(mesh_name: str):
        return {
            "region_name": "Cabeza",
            "titulo": "Anatomía de la cabeza",
            "contenido": [
                {"tipo": "audio", "titulo": "Explicación general", "info": "https://audio.link/123", "lugar": 1},
                {"tipo": "texto", "titulo": "Detalles anatómicos", "info": "El cráneo protege el cerebro.", "lugar": 2},
                {"tipo": "video", "titulo": "Video ilustrativo", "info": "https://youtube.com/example", "lugar": 3}
            ],
            "terminos_relacionados": [
                    {"nombre": "Cráneo", "tipo": "Hueso"},
                    {"nombre": "Cerebro", "tipo": "Órgano"},
                    {"nombre": "Nervios craneales", "tipo": "Sistema"}
            ]
        }

    monkeypatch.setattr(
        region_controller.RegionController,
        "get_region_by_mesh_name",
        fake_get_region_by_mesh_name
    )

    response = client.get("/regiones/Cabeza")
    assert response.status_code == 200
    data = response.json()

    assert data["region_name"] == "Cabeza"
    assert data["titulo"] == "Anatomía de la cabeza"
    assert isinstance(data["contenido"], list)
    assert len(data["contenido"]) == 3
    assert "terminos_relacionados" in data
    
def test_health_check(monkeypatch):
    """Debe retornar estado de la base de datos."""

    async def fake_health_check():
        return {
            "status": "healthy",
            "database": "connected",
            "message": "Conexión a MongoDB establecida correctamente"
        }

    monkeypatch.setattr(
        region_controller.RegionController,
        "health_check",
        fake_health_check
    )

    response = client.get("/regiones/health/status")
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert "Conexión a MongoDB" in data["message"]