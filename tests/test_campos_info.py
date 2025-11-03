from fastapi.testclient import TestClient
import app
from controllers import auth_controller, campo_info_controller

client = TestClient(app.app)

# Token de prueba
def make_token(email="tester@example.com"):
    payload = {"email": email, "name": "Tester"}
    return auth_controller.create_token(payload, 15)

def setup_module(module):
    """Configura token válido antes de todos los tests."""
    token = make_token()
    client.cookies.set("access_token", token)

def test_get_campos(monkeypatch):
    """Debe retornar lista de campos informativos."""

    async def fake_get_all_campos():
        return [
            {
                "_id": "012345678987654321012345",
                "titulo": "Campo A",
                "terminos_relacionados": [],
                "info_pack_id": None
            }
        ]

    monkeypatch.setattr(
        campo_info_controller.CampoInfoController,
        "get_all_campos",
        fake_get_all_campos
    )

    response = client.get("/campos_info/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_campo_id(monkeypatch):
    """Debe retornar un campo por ID."""

    async def fake_get_campo_by_id(campo_id):
        return {
            "_id": "012345678987654321012345",
            "titulo": "Campo Prueba",
            "terminos_relacionados": [],
            "info_pack_id": None,
            "info_pack_data": {"_id": "012345678987654321012345", "nombre": "Pack demo"},
        }

    monkeypatch.setattr(
        campo_info_controller.CampoInfoController,
        "get_campo_by_id",
        fake_get_campo_by_id
    )

    response = client.get("/campos_info/012345678987654321012345")
    assert response.status_code == 200
    assert response.json()["titulo"] == "Campo Prueba"

def test_create_campo(monkeypatch):
    """Debe crear un campo informativo."""

    async def fake_create_campo(**kwargs):
        return {"_id": "012345678987654321012345", **kwargs}

    monkeypatch.setattr(
        campo_info_controller.CampoInfoController,
        "create_campo",
        fake_create_campo
    )

    data = {
        "titulo": "Nuevo Campo",
        "terminos_relacionados": [],
        "info_pack_id": None,
    }

    response = client.post("/campos_info/", json=data)
    assert response.status_code == 200
    assert response.json()["titulo"] == "Nuevo Campo"