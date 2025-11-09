from fastapi.testclient import TestClient

from psylab.webapp import app


client = TestClient(app)


def test_index_lists_instruments():
    response = client.get("/")
    assert response.status_code == 200
    assert "PHQ-9" in response.text
