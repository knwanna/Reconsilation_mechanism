# Data Reconciliation API
A Flask-based API for reconciling data against various data sources, compliant with OpenRefine reconciliation protocols.

## Features
- OpenRefine-compliant reconciliation service
- Hexagonal Architecture for modular and testable code
- Fuzzy matching using Jaro-Winkler similarity metric
- Support for multiple data sources
- Interactive Swagger API documentation
- Comprehensive test suite with pytest
- CI/CD integration with GitHub Actions

## Architecture
The API follows a Hexagonal Architecture (Ports and Adapters pattern), ensuring separation of concerns and easy swapping of data sources or matching strategies. See the [architecture diagram](https://github.com/user/data-reconciliation-api/blob/main/docs/architectur.mmd) for details.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/user/data-reconciliation-api.git
   cd data-reconciliation-api
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   flask run
   ```
   The API will be available at `http://localhost:5000`.

## Usage
### Simple GET Request
Query the reconciliation endpoint with a single query string:
```bash
curl "http://localhost:5000/reconcile?query=George%20Orwell"
```
Example response:
```json
[
  {"name": "George Orwell", "score": 0.95, "match_type": "exact"},
  {"name": "Eric Arthur Blair", "score": 0.85, "match_type": "alias"}
]
```

### OpenRefine-compliant POST Request
Send a batch of queries following the OpenRefine reconciliation protocol:
```bash
curl -X POST http://localhost:5000/reconcile \
  -H "Content-Type: application/json" \
  -d '{
    "queries": {
      "q0": {"query": "Jane Austen", "limit": 3},
      "q1": {"query": "Tolkien", "type": "author"}
    }
  }'
```
Example response:
```json
{
  "q0": {
    "results": [
      {"name": "Jane Austen", "score": 0.98, "match_type": "exact"},
      {"name": "J. Austen", "score": 0.90, "match_type": "alias"}
    ]
  },
  "q1": {
    "results": [
      {"name": "J.R.R. Tolkien", "score": 0.92, "match_type": "exact"}
    ]
  }
}
```

## API Documentation
Interactive Swagger documentation is available at `/api-docs` when the server is running. Access it at `http://localhost:5000/api-docs`.

## Development
1. Run tests using pytest:
   ```bash
   pytest --cov=app tests/
   ```
2. Run linting with flake8:
   ```bash
   flake8 app/ tests/
   ```

## CI/CD
[![CI Status](https://github.com/user/data-reconciliation-api/workflows/CI/badge.svg)](https://github.com/user/data-reconciliation-api/actions)
