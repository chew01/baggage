from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

def test_main():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {'Hello': 'World'}
