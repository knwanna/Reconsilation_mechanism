import csv
from typing import List
from core.domain.models import Publication
from core.domain.services import DatasetLoadError

class CSVPublicationRepository:
    def __init__(self, csv_path: str):
        self.data = []
        try:
            with open(csv_path, newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.data.append(Publication(
                        id=row['id'].strip(),
                        title=row['title'].strip(),
                        authors=row['author'].strip(),
                        publication_year=int(row['year']) if row.get('year') else None,
                        canonical_id=row.get('canonical_id', '').strip()
                    ))
        except Exception as e:
            raise DatasetLoadError(f"Failed to load CSV: {str(e)}")

    def get_all(self) -> List[Publication]:
        return self.data
