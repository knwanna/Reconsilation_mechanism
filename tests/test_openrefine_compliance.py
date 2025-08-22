import pytest
from fastapi.testclient import TestClient
from adapters.entrypoints.fastapi_app import create_app
from core.domain.services import ReconciliationService
from core.matching.exact_match_strategy import ExactMatchStrategy
from core.matching.starts_with_strategy import StartsWithStrategy
from core.matching.fuzzy_jaro_winkler_strategy import FuzzyJaroWinklerStrategy
from adapters.repositories.csv_repository import CsvRepository

@pytest.fixture
def client():
    repository = CsvRepository('data/literary_works.csv')
    strategies = [
        ExactMatchStrategy(),
        StartsWithStrategy(),
        FuzzyJaroWinklerStrategy(min_score=0.8)
    ]
    reconciliation_service = ReconciliationService(strategies, repository)
    app = create_app(reconciliation_service)
    return TestClient(app)

@pytest.mark.parametrize("dataset", [
    "data/literary_works.csv",
    "data/synthetic_literary_works.csv"
])
def test_get_request_with_query(client: TestClient, dataset: str, monkeypatch):
    # Patch repository to use different datasets
    def mock_repository():
        return CsvRepository(dataset)
    monkeypatch.setattr("adapters.entrypoints.fastapi_app.CsvRepository", mock_repository)
    
    response = client.get('/reconcile?query=George%20Orwell')
    assert response.status_code == 200
    data = response.json()
    assert 'result' in data
    assert isinstance(data['result'], list)
    for item in data['result']:
        assert all(key in item for key in ['id', 'name', 'score', 'type'])

def test_post_request_with_queries(client: TestClient):
    payload = {
        "queries": {
            "q0": {"query": "George Orwell", "limit": 3},
            "q1": {"query": "Lord of", "limit": 3}
        }
    }
    response = client.post('/reconcile', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert 'q0' in data
    assert 'q1' in data
    assert isinstance(data['q0']['result'], list)
    assert isinstance(data['q1']['result'], list)
    for item in data['q0']['result'] + data['q1']['result']:
        assert all(key in item for key in ['id', 'name', 'score', 'type'])

def test_get_request_missing_query(client: TestClient):
    response = client.get('/reconcile')
    assert response.status_code == 400
    data = response.json()
    assert data == {"error": "Missing 'query' parameter"}
