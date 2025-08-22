from typing import List, Dict
from core.domain.models import MatchResult
from ports.repositories import Repository
from core.matching.exact_match_strategy import ExactMatchStrategy
from core.matching.starts_with_strategy import StartsWithStrategy
from core.matching.fuzzy_jaro_winkler_strategy import FuzzyJaroWinklerStrategy

class ReconciliationService:
    def __init__(self, repository: Repository):
        self.repository = repository
        self.strategies = [
            ExactMatchStrategy(),
            StartsWithStrategy(),
            FuzzyJaroWinklerStrategy()
        ]

    def reconcile(self, query: str, limit: int = 3) -> List[MatchResult]:
        results = []
        records = self.repository.search(query, limit * 2)  # Overfetch to allow strategy filtering
        for record in records:
            for strategy in self.strategies:
                score = strategy.match(query, record['name'])
                if score >= 0.8:
                    results.append(MatchResult(
                        id=record['id'],
                        name=record['name'],
                        score=score,
                        match=score == 1.0,
                        type=[strategy.__class__.__name__]
                    ))
        return sorted(results, key=lambda x: x.score, reverse=True)[:limit]
