from abc import ABC, abstractmethod

class MatchingStrategy(ABC):
    @abstractmethod
    def get_match_score(self, query: str, target: str) -> float:
        """Returns a similarity score between 0.0 and 1.0 for the given query and target strings."""
        pass
