from fastapi.testclient import TestClient
import app
from controllers import paquete_info_controller, auth_controller

client = TestClient(app.app)

# Crear token de prueba
def make_token(email="tester@example.com"):
    payload = {"email": email, "name": "Tester"}
    return auth_controller.create_token(payload, 15)

def setup_module(module):
    """Configura token válido antes de todos los tests."""
    token = make_token()
    client.cookies.set("access_token", token)

def test_get_paquetes(monkeypatch):
    async def fake_get_all_packs():
        return [{"_id": "012345678987654321012345", 
                 "textos": [
                            {
                                "subtitulo": "¿Qué es el ojo?",
                                "lugar": 1,
                                "texto": "El ojo permite captar la luz y formar imágenes del entorno."
                            }
                            ],
                "audios": [
                            {
                                "titulo": "Sonido de parpadeo",
                                "lugar": 2,
                                "link": "https://example.com/audio/parpadeo.mp3"
                            }
                            ],
                "imagenes": [
                            {
                                "titulo": "Imagen anatómica del ojo humano",
                                "lugar": 3,
                                "link": "https://example.com/img/ojo.png"
                            }
                            ],
                "videos": [
                            {
                                "titulo": "Video explicativo del funcionamiento del ojo",
                                "lugar": 4,
                                "link": "https://example.com/video/ojo.mp4"
                            }
  ]}]
    monkeypatch.setattr(paquete_info_controller.PaqueteInfoController, "get_all_packs", fake_get_all_packs)

    response = client.get("/paquetes_info/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "_id" in response.json()[0]

def test_get_paquete_by_id(monkeypatch):
    async def fake_get_pack_by_id(pack_id):
        return {"_id": "012345678987654321012345", "textos": [], "audios": [], "imagenes": [], "videos": []}
    monkeypatch.setattr(paquete_info_controller.PaqueteInfoController, "get_pack_by_id", fake_get_pack_by_id)

    response = client.get("/paquetes_info/012345678987654321012345")
    assert response.status_code == 200
    assert response.json()["_id"] == "012345678987654321012345"

# ---- POST crear paquete ----
def test_create_paquete(monkeypatch):
    async def fake_create_pack(**kwargs):
        return {"_id": "012345678987654321012345", **kwargs}
    monkeypatch.setattr(paquete_info_controller.PaqueteInfoController, "create_pack", fake_create_pack)

    data = {"textos": [], "audios": [], "imagenes": [], "videos": []}
    response = client.post("/paquetes_info/", json=data)
    assert response.status_code == 200
    assert response.json()["_id"] == "012345678987654321012345"

def test_update_paquete(monkeypatch):
    async def fake_update_pack(pack_id, **kwargs):
        return {"id": pack_id, **kwargs}
    monkeypatch.setattr(paquete_info_controller.PaqueteInfoController, "update_pack", fake_update_pack)

    data = {"_id": "012345678987654321012345", "textos": [], "audios": [], "imagenes": [], "videos": []}
    response = client.put("/paquetes_info/012345678987654321012345", json=data)
    assert response.status_code == 200
    assert response.json()["_id"] == "012345678987654321012345"

def test_delete_paquete(monkeypatch):
    async def fake_delete_pack(pack_id):
        return True
    monkeypatch.setattr(paquete_info_controller.PaqueteInfoController, "delete_pack", fake_delete_pack)

    response = client.delete("/paquetes_info/012345678987654321012345")
    assert response.status_code == 200
    assert "eliminado" in response.json()["detail"].lower()