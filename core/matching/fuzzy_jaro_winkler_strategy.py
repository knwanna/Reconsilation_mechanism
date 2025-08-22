from ..ports.matching_strategy import MatchingStrategy
from jaro_winkler import jaro_winkler_similarity

class FuzzyJaroWinklerStrategy(MatchingStrategy):
    """A matching strategy that uses the Jaro-Winkler similarity metric for string comparison."""
    
    def __init__(self, min_score: float = 0.8) -> None:
        """Initialize the Jaro-Winkler strategy with a minimum score threshold.
        
        Args:
            min_score: The minimum similarity score to accept as a valid match (default: 0.8).
        """
        self.min_score = min_score

    def get_match_score(self, query: str, target: str) -> float:
        """Calculates the Jaro-Winkler similarity score between query and target strings.
        
        Args:
            query: The query string to compare.
            target: The target string to compare against.
            
        Returns:
            A float between 0.0 and 1.0 representing the similarity score.
            Returns 0.0 if the score is below the minimum threshold.
        """
        normalized_query = query.lower().strip()
        normalized_target = target.lower().strip()
        score = jaro_winkler_similarity(normalized_query, normalized_target)
        return score if score >= self.min_score else 0.0
