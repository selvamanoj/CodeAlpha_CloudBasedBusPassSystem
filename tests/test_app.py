import os, tempfile
import pytest

@pytest.fixture()
def client(monkeypatch):
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    import app as bus_app
    monkeypatch.setattr(bus_app, "DATABASE_PATH", path)
    bus_app.app.config.update(TESTING=True)
    with bus_app.app.test_client() as test_client:
        yield test_client
    os.unlink(path)

def test_homepage_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Apply for a pass" in response.data

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"

def test_application_submission(client):
    response = client.post("/apply", data={
        "full_name":"Test Student", "email":"student@example.com",
        "phone":"9876543210", "route_name":"Central - College",
        "pass_type":"Student", "start_date":"2030-01-01"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Student" in response.data
