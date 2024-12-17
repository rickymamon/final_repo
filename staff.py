import pytest
from app import app  
from staff import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
def test_add_client(client):
    response = client.post('/add_client', 
        json={
            "client_name": "",
            "start_date": "2024-12-15",
            "job_department": "IT"
        })
    assert response.status_code == 404
    
def test_add_client_invalid_date(client):
    response = client.post('/add_client', 
        json={
            "client_name": "Jane Doe",
            "start_date": "15-12-2024",
            "job_department": "HR"
        })
    assert response.status_code == 404