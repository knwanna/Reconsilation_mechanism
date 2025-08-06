from abc import ABC, abstractmethod
from typing import List
from core.domain.models import Publication

class PublicationRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Publication]:
        pass
