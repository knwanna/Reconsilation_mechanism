from dataclasses import dataclass

@dataclass
class Record:
    id: int
    title: str
    author: str
    year: int
    canonical_id: str
