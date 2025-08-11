from dataclasses import dataclass
from enum import Enum
from typing import Optional  # <-- Add this import

class MatchType(str, Enum):
    EXACT = "exact"
    STARTS_WITH = "starts_with"
    PARTIAL = "partial"
    NONE = "none"

@dataclass
class Publication:
    id: str
    title: str
    authors: str
    publication_year: Optional[int] = None
    canonical_id: Optional[str] = None

@dataclass
class MatchResult:
    publication: Publication
    score: float
    match_type: MatchType
    match_details: str