import pytest
import json
from flask import Flask
from adapters.entrypoints.flask_app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_openrefine_get(client):
    response = client.get('/reconcile?query=1984')
    data = json.loads(response.data)
    assert 'result' in data
    assert len(data['result']) > 0
    assert all(key in data['result'][0] for key in ['id', 'name', 'score', 'match', 'type'])

def test_openrefine_post(client):
    payload = {
        'queries': {
            'q0': {'query': 'Tolkien', 'limit': 2}
        }
    }
    response = client.post('/reconcile', json=payload)
    data = json.loads(response.data)
    assert 'q0' in data
    assert 'result' in data['q0']
    assert len(data['q0']['result']) <= 2
