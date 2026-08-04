from fastapi.testclient import TestClient

from app.main import app, _tasks

client = TestClient(app)


def setup_function():
    """Limpa o estado em memória antes de cada teste."""
    _tasks.clear()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task():
    response = client.post("/tasks", json={"title": "Estudar Jenkins"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Estudar Jenkins"
    assert data["status"] == "PENDING"
    assert "id" in data


def test_create_task_sem_titulo_falha():
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422


def test_list_tasks():
    client.post("/tasks", json={"title": "Tarefa 1"})
    client.post("/tasks", json={"title": "Tarefa 2"})

    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_task_existente():
    criada = client.post("/tasks", json={"title": "Tarefa"}).json()

    response = client.get(f"/tasks/{criada['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == criada["id"]


def test_get_task_inexistente_404():
    response = client.get("/tasks/9999")
    assert response.status_code == 404


def test_update_task_status():
    criada = client.post("/tasks", json={"title": "Tarefa"}).json()

    response = client.patch(f"/tasks/{criada['id']}", json={"status": "DONE"})
    assert response.status_code == 200
    assert response.json()["status"] == "DONE"


def test_delete_task():
    criada = client.post("/tasks", json={"title": "Tarefa"}).json()

    response = client.delete(f"/tasks/{criada['id']}")
    assert response.status_code == 204

    response = client.get(f"/tasks/{criada['id']}")
    assert response.status_code == 404
