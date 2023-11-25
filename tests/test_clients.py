import pytest
from fastapi.testclient import TestClient
from main import app


def test_get_all_clients(temp_db):
    """Тест для получения всех клиентов"""
    with TestClient(app) as client:
        response = client.get("/clients/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == []


def test_create_client(temp_db):
    """Тест создания клиента"""
    client_data = {
        "document": "123AAAAAAA",
        "lastname": "Иванова",
        "firstname": "Анна",
        "midname": "Ивановна",
        "birthday": "2003-12-25",
    }
    with TestClient(app) as client:
        response = client.post("/clients/", json=client_data)
    assert response.status_code == 200
    assert "id" in response.json()

    # Проверим, что клиент действительно создан
    with TestClient(app) as client:
        response = client.get(f"/clients/{response.json()['id']}")
    assert response.status_code == 200
    assert response.json() == {**client_data, "id": response.json()["id"]}


def test_doc_validating(temp_db):
    """# Тест валидации документа при создании клиента"""
    client_data = {
        "document": "123AAAAAAA",
        "lastname": "Иванова",
        "firstname": "Анна",
        "midname": "Ивановна",
        "birthday": "2003-12-25",
    }
    with TestClient(app) as client:
        response = client.post("/clients/", json=client_data)
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'String should have at least 10 characters'


def test_birthday_validating(temp_db):
    """# Тест валидации даты рождения при создании клиента"""
    client_data = {
        "document": "123AAAAAAA",
        "lastname": "Иванова",
        "firstname": "Анна",
        "midname": "Ивановна",
        "birthday": "2003-12-25",
    }
    with TestClient(app) as client:
        response = client.post("/clients/", json=client_data)
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Value error, Age must be between 18 and 100.'


def test_update_client(temp_db):
    """Тест обновления клиента"""
    # создание клиента для обновления
    client_data = {
        "document": "123AAAAAAA",
        "lastname": "Иванова",
        "firstname": "Анна",
        "midname": "Ивановна",
        "birthday": "2003-12-25",
    }
    with TestClient(app) as client:
        response = client.post("/clients/", json=client_data)
    assert response.status_code == 200
    client_id = response.json()["id"]

    # обновление данных клиента
    new_client_data = {
        "document": "123AAAAAAA",
        "lastname": "Петрова",
        "firstname": "Анна",
        "midname": "Михайловна",
        "birthday": "2003-12-25",
    }
    with TestClient(app) as client:
        response = client.put(f"/clients/{client_id}", json=new_client_data)
    assert response.status_code == 200
    assert response.json() == {**new_client_data, "id": client_id}


def test_delete_client(temp_db):
    """Тест удаления клиента"""

    # создание клиента для удаления
    client_data = {
        "document": "123AAAAAAA",
        "lastname": "Иванова",
        "firstname": "Анна",
        "midname": "Ивановна",
        "birthday": "2003-12-25",
    }
    with TestClient(app) as client:
        response = client.post("/clients/", json=client_data)
    assert response.status_code == 200
    client_id = response.json()["id"]

    # удаление клиента
    with TestClient(app) as client:
        response = client.delete(f"/clients/{client_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted"}

    # Проверим, что клиента удален
    with TestClient(app) as client:
        response = client.get(f"/clients/{client_id}")
    assert response.status_code == 404


if __name__ == '__main__':
    pytest.main(['-v'])
