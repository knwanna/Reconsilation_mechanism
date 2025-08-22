from typing import Dict, List
from core.domain.models import MatchResult

class ReconciliationEntrypoint:
    def __init__(self, service):
        self.service = service

    def reconcile(self, query_data: Dict) -> List[MatchResult]:
        query = query_data.get('query', '')
        limit = query_data.get('limit', 3)
        return self.service.reconcile(query, limit)
