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
    

def test_apply_job(client):
    
    client.post('/add_job', 
        json={
            "id": "102",
            "fullname": "Ricky mamon",
            "job_title": "project manager",
            "description": "developer",
            "department": "IT",
            "address": "palawan"
        })

    response = client.post('/apply_job', 
            json={
                "candidate_name": "robert",
                "id": "78"
            })
    assert response.status_code == 404


def test_apply_nonexistent_job(client):
    response = client.post('/apply_job', 
        json={
            "candidate_name": "jeizer",
            "job_id": "88"
        })
    assert response.status_code == 404