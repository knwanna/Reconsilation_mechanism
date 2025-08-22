import pytest
from core.domain.services import ReconciliationService
from adapters.repositories.csv_repository import CsvRepository

@pytest.fixture
def service():
    repository = CsvRepository('data/literary_works.csv')
    return ReconciliationService(repository)
