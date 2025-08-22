import pytest
from core.domain.services import ReconciliationService
from core.domain.models import Record
from core.matching.exact_match_strategy import ExactMatchStrategy
from core.matching.starts_with_strategy import StartsWithStrategy
from core.matching.fuzzy_jaro_winkler_strategy import FuzzyJaroWinklerStrategy

class MockRepository:
    def get_all_records(self):
        return [
            Record(id=1, title="The Hobbit", author="J.R.R. Tolkien", year=1937, canonical_id="tolkien-1"),
            Record(id=2, title="1984", author="George Orwell", year=1949, canonical_id="orwell-1")
        ]

def test_reconciliation_service():
    strategies = [ExactMatchStrategy(), StartsWithStrategy(), FuzzyJaroWinklerStrategy(min_score=0.8)]
    repo = MockRepository()
    service = ReconciliationService(strategies, repo)

    results = service.reconcile("Hobbit")
    assert len(results) > 0
    assert results[0]["name"] == "The Hobbit"
    assert results[0]["score"] == 1.0
    assert results[0]["match_type"] == "ExactMatchStrategy"
