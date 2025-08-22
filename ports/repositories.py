from abc import ABC, abstractmethod
from typing import List, Dict

class Repository(ABC):
    @abstractmethod
    def search(self, query: str, limit: int = 3) -> List[Dict]:
        pass
