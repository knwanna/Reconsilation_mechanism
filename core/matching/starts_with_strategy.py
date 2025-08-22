from ports.matching_strategy import MatchingStrategy

class StartsWithStrategy(MatchingStrategy):
    def match(self, query: str, target: str) -> float:
        return 0.9 if target.lower().startswith(query.lower()) else 0.0
