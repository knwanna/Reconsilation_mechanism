from abc import ABC, abstractmethod
from typing import List
from ..domain.models import Record

class Repository(ABC):
    @abstractmethod
    def get_all_records(self) -> List[Record]:
        """Retrieve all records from the data source.

        Returns:
            A list of Record objects.
        """
        pass
