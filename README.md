# Publication Reconciliation Service

## Overview
Hexagonal Architecture service for reconciling publication references using:
- Exact matches (score = 1.0)
- Starts-with matches (score = 0.9)
- Partial matches (score = 0.8)

## Project Structure
```
C:.
│   Create_Reconciliation_Structure.ps1
│   project_structure.txt
│
└───Reconciliation_mechanism
    │   .gitignore
    │   main.py
    │   project_structure.txt
    │   README.md
    │   requirements.txt
    │
    ├───adapters
    │   ├───entrypoints
    │   │       fastapi_app.py
    │   │
    │   └───repositories
    │           csv_repository.py
    │
    ├───core
    │   └───domain
    │           models.py
    │           services.py
    │
    ├───data
    │       literary_works.csv
    │
    ├───ports
    │       entrypoints.py
    │       repositories.py
    │
    └───tests
            test_csv.py
```

## Installation (Windows)

### Prerequisites
```powershell
python --version
winget install -e --id Git.Git
winget install -e --id Microsoft.VisualStudioCode
```

### Setup
```powershell
git clone https://github.com/your/repo.git
cd Reconciliation_mechanism

python -m venv .venv
.\.venv\Scriptsctivate
pip install -r requirements.txt

if (!(Test-Path "data")) { mkdir data }
@"
id,title,author,year,canonical_id
1,The Hobbit,J.R.R. Tolkien,1937,tolkien-1
2,1984,George Orwell,1949,orwell-1
3,To Kill a Mockingbird,Harper Lee,1960,lee-1
"@ | Out-File -FilePath "data/literary_works.csv" -Encoding utf8
```

## Running the Service
```powershell
python main.py
# or specify a port
python main.py --port 8001
```

## Testing

### Swagger UI
Open [http://localhost:8000/docs](http://localhost:8000/docs) and try:
```json
{
  "query": "George Orwell",
  "limit": 3
}
```

### PowerShell Test
```powershell
$response = Invoke-RestMethod -Uri "http://localhost:8000/reconcile" `
  -Method Post `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"query":"Hobbit"}'
$response | ConvertTo-Json -Depth 4
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| ModuleNotFoundError | pip install -r requirements.txt |
| AddressAlreadyInUse | python main.py --port 8001 |
| DatasetLoadError | Ensure data/literary_works.csv exists |
| 404 Not Found | Use POST /reconcile |

## Example Data
```csv
id,title,author,year,canonical_id
1,The Hobbit,J.R.R. Tolkien,1937,tolkien-1
2,1984,George Orwell,1949,orwell-1
3,To Kill a Mockingbird,Harper Lee,1960,lee-1
```
