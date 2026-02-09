from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_roll():
    response = client.post(
        "/rolls/", 
        json={"length": 15.0, "weight": 7.5}
    )
    # Проверяем результат
    assert response.status_code == 200
    data = response.json()
    assert data["length"] == 15.0
    assert "id" in data

def test_get_rolls_list():
    response = client.get("/rolls/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)