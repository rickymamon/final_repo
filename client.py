import pytest
from app import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_add_job(client):
    response = client.post('/add_job',
        json={
            "id": "101",
            "fullname": "Ricky mamon",
            "job_title": "Software Engineer",
            "description": "Develop and maintain software applications.",
            "department": "IT",
            "address": "Palawan"
        })
    assert response.status_code == 404