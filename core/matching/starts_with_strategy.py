from ..ports.matching_strategy import MatchingStrategy

class StartsWithStrategy(MatchingStrategy):
    """A matching strategy that checks if the target starts with the query."""

    def get_match_score(self, query: str, target: str) -> float:
        """Returns 0.9 if the target starts with the query, else 0.0.

        Args:
            query: The query string to compare.
            target: The target string to compare against.

        Returns:
            A float (0.9 for starts-with match, 0.0 otherwise).
        """
        normalized_query = query.lower().strip()
        normalized_target = target.lower().strip()
        return 0.9 if normalized_target.startswith(normalized_query) else 0.0
