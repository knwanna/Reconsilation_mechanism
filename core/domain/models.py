from dataclasses import dataclass
from typing import List

@dataclass
class MatchResult:
    id: str
    name: str
    score: float
    match: bool
    type: List[str]
