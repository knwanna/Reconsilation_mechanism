import pandas as pd
from ports.repositories import Repository

class CsvRepository(Repository):
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)

    def search(self, query, limit=3):
        results = []
        for _, row in self.df.iterrows():
            if query.lower() in row['title'].lower() or query.lower() in row['author'].lower():
                results.append({
                    'id': row['canonical_id'],
                    'name': row['title'],
                    'author': row['author'],
                    'year': row['year']
                })
        return results[:limit]
