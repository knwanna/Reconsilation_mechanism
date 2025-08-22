Publication Reconciliation Service
A Flask-based reconciliation service compliant with the OpenRefine protocol, built using Hexagonal Architecture for entity resolution of publication references. This project supports advanced database techniques for your thesis, providing a production-ready implementation with an Electron desktop client, comprehensive testing, and CI/CD.
Features

OpenRefine-compliant reconciliation API with GET and POST /reconcile endpoints.
Hexagonal Architecture for modularity and testability.
Matching strategies: Exact (score=1.0), StartsWith (score=0.9), Fuzzy Jaro-Winkler (score≥0.8).
CSV-based data repository with curated and synthetic datasets.
Electron-based desktop client for Windows, Linux, and macOS.
Comprehensive test suite with 95% coverage and load testing (p95 = 112ms).
Interactive Swagger-like API testing via browser or cURL.
CI/CD pipeline with GitHub Actions for automated testing and building.
Prototype evaluation in proto_v1 for thesis comparison.

Architecture
The service follows Hexagonal Architecture, separating business logic (core) from infrastructure (adapters) via ports. The ReconciliationService orchestrates matching strategies, with CsvRepository for data access and Flask for HTTP endpoints. An Electron desktop client provides user-friendly access. See architecture diagram.
Project Structure
Reconsilation_mechanism/
│   .gitignore
│   main.py
│   requirements.txt
│   README.md
│
├───.github/workflows/
│       ci.yml
├───adapters/
│   ├───entrypoints/
│   │       flask_app.py
│   ├───repositories/
│   │       csv_repository.py
├───core/
│   ├───domain/
│   │       models.py
│   │       services.py
│   ├───matching/
│   │       exact_match_strategy.py
│   │       starts_with_strategy.py
│   │       fuzzy_jaro_winkler_strategy.py
├───ports/
│       entrypoints.py
│       repositories.py
│       matching_strategy.py
├───data/
│       literary_works.csv
│       synthetic_literary_works.csv
├───tests/
│       test_csv.py
│       test_reconciliation.py
│       test_openrefine_compliance.py
│       locustfile.py
│       conftest.py
├───scripts/
│       generate_synthetic_data.py
├───desktop_client/
│       package.json
│       main.js
│       preload.js
│       index.html
│       renderer.js
├───docs/
│       overview.md
│       test_report.md
│       datasets.md
│       load_test_results.csv
│       architecture.mmd
├───proto_v1/
│   ├───data/
│   │       literary_works.csv
│   ├───evaluation_results/
│   │       match_accuracy.csv
│   │       response_times.csv
│   test_evaluation.py

Installation
Prerequisites

Windows machine with PowerShell 5.1+.
Git, Python 3.11, Node.js v18+.
Internet access for cloning and dependencies.

API Setup
git clone https://github.com/knwanna/Reconsilation_mechanism.git
cd Reconsilation_mechanism
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/generate_synthetic_data.py

Desktop Client Setup
cd desktop_client
npm install
npm run build:win  # Windows
npm run build:linux  # Linux
npm run build:mac  # macOS

Builds are output to desktop_client/dist/.
Running the Service
# Run API
python main.py
# or specify a port
python main.py 8001

Access the API at http://localhost:8000. Test endpoints using a browser or cURL.
Usage
API: Single Query (GET)
Invoke-RestMethod -Uri "http://localhost:8000/reconcile?query=George%20Orwell" -Method Get

Response:
{
  "result": [
    {"id": "orwell-1", "name": "1984", "score": 1.0, "match": true, "type": ["ExactMatchStrategy"]},
    {"id": "orwell-2", "name": "Animal Farm", "score": 0.9, "match": false, "type": ["StartsWithStrategy"]}
  ]
}

API: Batch Query (POST)
$body = @{
    queries = @{
        q0 = @{ query = "Hobbit"; limit = 3 }
        q1 = @{ query = "Tolkien"; limit = 3 }
    }
} | ConvertTo-Json -Depth 4
Invoke-RestMethod -Uri "http://localhost:8000/reconcile" -Method Post -ContentType "application/json" -Body $body

Response:
{
  "q0": {
    "result": [
      {"id": "tolkien-1", "name": "The Hobbit", "score": 1.0, "match": true, "type": ["ExactMatchStrategy"]}
    ]
  },
  "q1": {
    "result": [
      {"id": "tolkien-2", "name": "Lord of the Rings", "score": 0.9, "match": false, "type": ["StartsWithStrategy"]}
    ]
  }
}

Desktop Client
Run the built executable from desktop_client/dist/ or:
cd desktop_client
npm start

Testing
# Unit and integration tests
pytest --cov=core --cov=adapters
# Linting
flake8 core/ adapters/ tests/
# Load tests
locust -f tests/locustfile.py

Access Locust UI at http://localhost:8089 to simulate 50 users and verify p95 = 112ms.
CI/CD
The ci.yml runs tests and builds the desktop client on push/pull requests.
Deployment
Deploy the API to Railway:

Push the repository to GitHub.
Create a Railway project and link it to the repository.
Set environment variable PORT=8000.
Deploy, and access at the provided URL (e.g., https://your-api-hosted-url.railway.app).
Update desktop_client/preload.js with the deployed URL (replace http://localhost:8000).

Troubleshooting



Error
Solution



ModuleNotFoundError
Run pip install -r requirements.txt


AddressAlreadyInUse
Use python main.py 8001


DatasetLoadError
Ensure data/literary_works.csv exists


404 Not Found
Use POST or GET /reconcile


Electron Errors
Run npm install in desktop_client/


Datasets

data/literary_works.csv: Curated dataset with 30 records and ambiguities.
data/synthetic_literary_works.csv: 1,000 records with controlled noise.
proto_v1/data/literary_works.csv: Prototype dataset for evaluation.See docs/datasets.md for details.



About
Advanced Database Techniques, reconciliation search patterns. Includes prototype evaluation (proto_v1) .﻿
