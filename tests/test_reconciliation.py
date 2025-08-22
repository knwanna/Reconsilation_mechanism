import pytest
from core.domain.models import MatchResult

def test_reconciliation_exact_match(service):
    results = service.reconcile('The Hobbit', limit=1)
    assert len(results) == 1
    assert results[0].name == 'The Hobbit'
    assert results[0].score == 1.0
    assert results[0].match is True

def test_reconciliation_partial_match(service):
    results = service.reconcile('Hobb', limit=2)
    assert len(results) > 0
    assert any(result.score >= 0.8 and result.score < 1.0 for result in results)
