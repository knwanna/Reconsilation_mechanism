import pytest
from fastapi.testclient import TestClient
from adapters.entrypoints.fastapi_app import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_repositories(monkeypatch):
    def mock_youtube_search(query):
        return [{"title": "Test Video"}]
        
    monkeypatch.setattr(
        "adapters.repositories.youtube.YouTubeRepository.search",
        mock_youtube_search
    )