from abc import ABC, abstractmethod

class MatchingStrategy(ABC):
    @abstractmethod
    def match(self, query: str, target: str) -> float:
        pass
