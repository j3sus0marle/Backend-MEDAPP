from fastapi.testclient import TestClient
import app

client = TestClient(app.app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"¡Bienvenido a Backend MEDAPP!",
                               "version":"Prueba","docs":"/docs",
                               "endpoints":{"campos_info":"/campos_info","paquete_info":"/paquete_info","auth_login":"/auth/login"}}
    


