import csv
from typing import List
from ports.repositories import PublicationRepository
from core.domain.models import Publication
from core.domain.services import DatasetLoadError

class CSVPublicationRepository(PublicationRepository):
    def __init__(self, csv_path: str):
        self.data = []
        try:
            with open(csv_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.data.append(Publication(
                        id=row['id'],
                        title=row['title'],
                        authors=row['author'],
                        publication_year=int(row['year']) if 'year' in row else None,
                        canonical_id=row.get('canonical_id')
                    ))
        except Exception as e:
            raise DatasetLoadError(f"Failed to load CSV: {str(e)}")
    
    def get_all(self) -> List[Publication]:
        return self.data
