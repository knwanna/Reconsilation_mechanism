from abc import ABC, abstractmethod
from .models import Publication, MatchResult, MatchType
from typing import List

class Normalizer(ABC):
    @abstractmethod
    def normalize(self, text: str) -> str:
        pass

class BasicNormalizer(Normalizer):
    def normalize(self, text: str) -> str:
        return text.lower().strip()

class ReconciliationService:
    def __init__(self, repository: 'PublicationRepository', normalizer: Normalizer = BasicNormalizer()):
        self.repo = repository
        self.normalizer = normalizer
    
    def reconcile(self, query: str, limit: int = 5) -> List[MatchResult]:
        if not query:
            return []
            
        norm_query = self.normalizer.normalize(query)
        publications = self.repo.get_all()
        results = []
        
        for pub in publications:
            if not pub.title:
                continue
                
            norm_title = self.normalizer.normalize(pub.title)
            score, match_type, details = self._calculate_match(norm_query, norm_title)
            
            if score > 0:
                results.append(MatchResult(
                    publication=pub,
                    score=score,
                    match_type=match_type,
                    match_details=details
                ))
        
        return sorted(results, key=lambda x: x.score, reverse=True)[:limit]
    
    def _calculate_match(self, query: str, title: str) -> tuple:
        if query == title:
            return (1.0, MatchType.EXACT, "Exact match found")
        if title.startswith(query):
            return (0.9, MatchType.STARTS_WITH, f"Title starts with '{query}'")
        if query in title:
            return (0.8, MatchType.PARTIAL, f"Query found within title")
        return (0.0, MatchType.NONE, "No match found")

class DatasetLoadError(Exception):
    pass
