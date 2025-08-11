from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from core.domain.services import ReconciliationService, DatasetLoadError
from core.domain.models import MatchType
from ports.repositories import PublicationRepository
from fastapi.middleware.cors import CORSMiddleware

class ReconciliationRequest(BaseModel):
    """
    Request payload for publication reconciliation.
    
    Examples:
        ```json
        {
            "query": "George Orwell",
            "limit": 3,
            "strict": false
        }
        ```
    """
    query: str = Field(..., min_length=1, max_length=200, example="Hobbit",
                      description="Text to match against publication titles")
    limit: int = Field(default=5, ge=1, le=100, example=5,
                     description="Maximum number of results to return (1-100)")
    strict: bool = Field(default=False, description="If true, only exact matches will be returned")

class MatchResultResponse(BaseModel):
    """Detailed reconciliation result with confidence scoring"""
    id: str = Field(..., example="1", description="Internal publication ID")
    title: str = Field(..., example="The Hobbit", description="Full publication title")
    authors: str = Field(..., example="J.R.R. Tolkien", description="Author name(s)")
    publication_year: Optional[int] = Field(None, example=1937,
                                          description="Year of publication if available")
    score: float = Field(..., ge=0.0, le=1.0, example=1.0,
                        description="Match confidence (1.0=exact, 0.9=starts with, 0.8=partial)")
    match_type: str = Field(..., example="exact",
                           description="One of: exact, starts_with, partial")
    match_details: str = Field(..., example="Exact match found",
                             description="Human-readable match explanation")
    canonical_id: Optional[str] = Field(None, example="tolkien-1",
                                      description="External reference ID if available")

def create_app(repo: PublicationRepository) -> FastAPI:
    """Factory function to create configured FastAPI application instance"""
    
    app = FastAPI(
        title="Publication Reconciliation Service API",
        description="""
        ## Hexagonal Architecture Implementation
        
        Provides standardized reconciliation of publication references against
        canonical datasets using three-tier matching:
        
        - **Exact Matches** (score=1.0)
        - **Starts-With Matches** (score=0.9)
        - **Partial Substring Matches** (score=0.8)
        
        [GitHub Repository](https://github.com/your/repo)
        """,
        version="1.0.0",
        openapi_tags=[{
            "name": "reconciliation",
            "description": "Publication reference matching operations"
        }],
        license_info={
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT",
        },
    )

    # Enable CORS for web applications
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get(
        "/",
        summary="API Root",
        response_description="Service metadata",
        tags=["service-info"]
    )
    async def root():
        """Return basic service information and available endpoints"""
        return {
            "service": "Publication Reconciliation Service",
            "architecture": "Hexagonal",
            "endpoints": {
                "reconcile": {
                    "method": "POST",
                    "path": "/reconcile",
                    "description": "Match publication references against canonical data"
                },
                "documentation": [
                    {"type": "interactive", "path": "/docs"},
                    {"type": "alternative", "path": "/redoc"}
                ]
            },
            "repository": "https://github.com/your/repo"
        }

    @app.post(
        "/reconcile",
        response_model=List[MatchResultResponse],
        status_code=status.HTTP_200_OK,
        summary="Reconcile Publication References",
        description="""
        Match a query string against known publications using three-tier matching:
        
        1. **Exact Match**: Full title match (score=1.0)
        2. **Starts-With**: Title begins with query (score=0.9)
        3. **Partial Match**: Query appears anywhere in title (score=0.8)
        """,
        tags=["reconciliation"],
        responses={
            status.HTTP_200_OK: {
                "description": "Successful reconciliation",
                "content": {
                    "application/json": {
                        "examples": {
                            "exact_match": {
                                "summary": "Exact match result",
                                "value": [{
                                    "id": "1",
                                    "title": "The Hobbit",
                                    "authors": "J.R.R. Tolkien",
                                    "publication_year": 1937,
                                    "score": 1.0,
                                    "match_type": "exact",
                                    "match_details": "Exact match found",
                                    "canonical_id": "tolkien-1"
                                }]
                            },
                            "partial_match": {
                                "summary": "Partial match result",
                                "value": [{
                                    "id": "4",
                                    "title": "The Adventures of Tom Sawyer",
                                    "authors": "Mark Twain",
                                    "score": 0.8,
                                    "match_type": "partial",
                                    "match_details": "Query found within title"
                                }]
                            }
                        }
                    }
                }
            },
            status.HTTP_400_BAD_REQUEST: {
                "description": "Invalid request parameters",
                "content": {
                    "application/json": {
                        "example": {"detail": "Query parameter is required"}
                    }
                }
            },
            status.HTTP_500_INTERNAL_SERVER_ERROR: {
                "description": "Dataset loading error",
                "content": {
                    "application/json": {
                        "example": {"detail": "Failed to load CSV: File not found"}
                    }
                }
            }
        }
    )
    async def reconcile_publications(request: ReconciliationRequest):
        """
        Perform publication reference reconciliation against canonical dataset.
        
        Returns a list of potential matches sorted by match confidence score.
        """
        try:
            service = ReconciliationService(repo)
            results = service.reconcile(
                query=request.query,
                limit=request.limit
            )
            
            return [
                MatchResultResponse(
                    id=result.publication.id,
                    title=result.publication.title,
                    authors=result.publication.authors,
                    publication_year=result.publication.publication_year,
                    score=result.score,
                    match_type=result.match_type.value,
                    match_details=result.match_details,
                    canonical_id=result.publication.canonical_id
                ) for result in results
            ]
            
        except DatasetLoadError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Dataset unavailable: {str(e)}"
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    return app