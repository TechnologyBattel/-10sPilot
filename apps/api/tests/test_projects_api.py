"""Project API integration tests."""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_project_crud_api() -> None:
    payload = {
        "name": "API Integration Test",
        "domain": "api-integration-test.example",
        "country": "US",
        "language": "en",
    }

    create_response = client.post("/api/v1/projects", json=payload)

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["name"] == payload["name"]
    assert created["domain"] == payload["domain"]
    assert created["id"]

    project_id = created["id"]

    list_response = client.get("/api/v1/projects")
    assert list_response.status_code == 200
    projects = list_response.json()
    assert any(project["id"] == project_id for project in projects)

    get_response = client.get(f"/api/v1/projects/{project_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == project_id

    delete_response = client.delete(f"/api/v1/projects/{project_id}")
    assert delete_response.status_code == 204

    missing_response = client.get(f"/api/v1/projects/{project_id}")
    assert missing_response.status_code == 404
