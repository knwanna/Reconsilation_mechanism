from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from core.domain.services import ReconciliationService, DatasetLoadError
from core.domain.models import MatchType

class ReconciliationRequest(BaseModel):
    query: str
    limit: int = 5
    strict: bool = False

class MatchResultResponse(BaseModel):
    id: str
    title: str
    authors: str
    publication_year: Optional[int]
    score: float
    match_type: str
    match_details: str
    canonical_id: Optional[str]

def create_app(repo: PublicationRepository) -> FastAPI:
    app = FastAPI(
        title="Data Reconciliation Service",
        description="Hexagonal Architecture implementation"
    )
    
    service = ReconciliationService(repo)
    
    @app.post("/reconcile", response_model=List[MatchResultResponse])
    async def reconcile(request: ReconciliationRequest):
        try:
            results = service.reconcile(request.query, request.limit)
            return [
                MatchResultResponse(
                    id=r.publication.id,
                    title=r.publication.title,
                    authors=r.publication.authors,
                    publication_year=r.publication.publication_year,
                    score=r.score,
                    match_type=r.match_type.value,
                    match_details=r.match_details,
                    canonical_id=r.publication.canonical_id
                ) for r in results
            ]
        except DatasetLoadError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    return app
