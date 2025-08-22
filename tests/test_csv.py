import pytest
from adapters.repositories.csv_repository import CsvRepository

def test_csv_repository_search():
    repo = CsvRepository('data/literary_works.csv')
    results = repo.search('Tolkien', limit=2)
    assert len(results) <= 2
    assert all('Tolkien' in result['author'] for result in results)
