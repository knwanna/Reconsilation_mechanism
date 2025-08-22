from ports.matching_strategy import MatchingStrategy
from jaro import jaro_winkler_metric

class FuzzyJaroWinklerStrategy(MatchingStrategy):
    def match(self, query: str, target: str) -> float:
        return jaro_winkler_metric(query.lower(), target.lower())
