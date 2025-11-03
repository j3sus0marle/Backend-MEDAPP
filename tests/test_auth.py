from fastapi.testclient import TestClient
import app
from controllers import auth_controller
from jose import jwt

client = TestClient(app.app)
JWT_SECRET = auth_controller.JWT_SECRET


def make_token(email="test@example.com"):
    """Crea un token temporal para pruebas."""
    payload = {"email": email, "name": "Tester"}
    return auth_controller.create_token(payload, 15)


def test_auth_validate_session_valid_token():
    """Debe retornar los datos del usuario si el token es válido."""

    # Crear token manualmente y establecerlo como cookie del cliente
    token = make_token()
    client.cookies.set("access_token", token)

    response = client.get("/auth/session")

    assert response.status_code == 200
    data = response.json()
    assert data["session_active"] is True
    assert data["user"]["email"] == "test@example.com"


def test_auth_validate_session_invalid_token():
    """Debe fallar si el token es inválido."""
    client.cookies.clear()
    client.cookies.set("access_token", "token_invalido")

    response = client.get("/auth/session")
    assert response.status_code == 401


def test_refresh():
    """Debe generar un nuevo access_token si la sesión es válida."""

    # Simular sesión existente
    session_token = "abc123"
    fake_payload = {"email": "test@example.com", "name": "Tester"}
    refresh_token = auth_controller.create_token(fake_payload, 60 * 24 * 7)
    auth_controller.SESSIONS[session_token] = {
        "user": fake_payload,
        "refresh_token": refresh_token,
    }

    client.cookies.clear()
    client.cookies.set("session_token", session_token)

    response = client.post("/auth/refresh")

    assert response.status_code == 200
    json_data = response.json()
    assert "access_token" in json_data
    assert "access_token" in response.cookies


def test_logout():
    """Debe borrar las cookies y eliminar la sesión."""

    session_token = "xyz123"
    auth_controller.SESSIONS[session_token] = {"user": {"email": "test@example.com"}}

    client.cookies.clear()
    client.cookies.set("session_token", session_token)

    response = client.post("/auth/logout")

    assert response.status_code == 200
    assert response.json()["message"] == "Sesion cerrada"
    assert session_token not in auth_controller.SESSIONS