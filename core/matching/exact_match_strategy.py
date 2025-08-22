from ports.matching_strategy import MatchingStrategy

class ExactMatchStrategy(MatchingStrategy):
    def match(self, query: str, target: str) -> float:
        return 1.0 if query.lower() == target.lower() else 0.0
