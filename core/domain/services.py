from typing import List, Dict
from ..ports.matching_strategy import MatchingStrategy
from ..domain.models import Record

class ReconciliationService:
    """Core orchestrator for the reconciliation process, coordinating strategies and repository."""

    def __init__(self, strategies: List[MatchingStrategy], repository: 'Repository') -> None:
        """Initialize the service with a list of matching strategies and a repository.

        Args:
            strategies: List of MatchingStrategy instances to evaluate queries.
            repository: Repository instance providing access to records.
        """
        self.strategies = strategies
        self.repository = repository

    def reconcile(self, query: str) -> List[Dict]:
        """Reconcile a query string against records using all available strategies.

        Args:
            query: The input query string to match against records.

        Returns:
            A sorted list of dictionaries containing match results with id, name, score, and match_type.
        """
        normalized_query = query.lower().strip()
        records = self.repository.get_all_records()
        results = []

        for record in records:
            max_score = 0.0
            best_strategy = None

            for strategy in self.strategies:
                score = strategy.get_match_score(normalized_query, record.title)
                if score > max_score:
                    max_score = score
                    best_strategy = strategy

            if max_score > 0:
                results.append({
                    "id": record.canonical_id,
                    "name": record.title,
                    "score": max_score,
                    "match": max_score > 0.9,
                    "type": [best_strategy.__class__.__name__]
                })

        return sorted(results, key=lambda x: x["score"], reverse=True)
