import logging
import pandas as pd
from typing import List
from ..ports.repositories import Repository
from ..core.domain.models import Record

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CsvRepository(Repository):
    """Repository adapter that reads records from a CSV file."""

    def __init__(self, file_path: str) -> None:
        """Initialize the repository with the path to the CSV file.

        Args:
            file_path: Path to the CSV file containing records.
        """
        self.file_path = file_path

    def get_all_records(self) -> List[Record]:
        """Retrieve all records from the CSV file.

        Returns:
            A list of Record objects.

        Raises:
            FileNotFoundError: If the CSV file is not found.
            Exception: For other errors during CSV processing.
        """
        try:
            df = pd.read_csv(self.file_path)
            records = [
                Record(id=row['id'], title=row['title'], author=row['author'], 
                       year=row['year'], canonical_id=row['canonical_id'])
                for _, row in df.iterrows()
            ]
            return records
        except FileNotFoundError:
            logger.error(f"CSV file not found: {self.file_path}")
            raise
        except Exception as e:
            logger.error(f"Error reading CSV file: {str(e)}")
            raise
