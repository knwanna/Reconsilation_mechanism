from adapters.repositories.csv_repository import CSVPublicationRepository
from adapters.entrypoints.fastapi_app import create_fastapi_app
import uvicorn

app = create_fastapi_app(
    CSVPublicationRepository("data/literary_works.csv")
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)  # Localhost only
