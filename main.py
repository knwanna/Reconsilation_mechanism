import uvicorn
from adapters.entrypoints.fastapi_app import create_app
from core.matching.exact_match_strategy import ExactMatchStrategy
from core.matching.starts_with_strategy import StartsWithStrategy
from core.matching.fuzzy_jaro_winkler_strategy import FuzzyJaroWinklerStrategy
from core.domain.services import ReconciliationService
from adapters.repositories.csv_repository import CsvRepository
import argparse

def main():
    parser = argparse.ArgumentParser(description="Run the Reconciliation API")
    parser.add_argument('--port', type=int, default=8000, help="Port to run the server on")
    args = parser.parse_args()

    repository = CsvRepository('data/literary_works.csv')
    strategies = [
        ExactMatchStrategy(),
        StartsWithStrategy(),
        FuzzyJaroWinklerStrategy(min_score=0.8)
    ]
    reconciliation_service = ReconciliationService(strategies, repository)
    app = create_app(reconciliation_service)
    
    uvicorn.run(app, host="0.0.0.0", port=args.port)

if __name__ == "__main__":
    main()
