from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from ..core.domain.services import ReconciliationService

app = FastAPI(title="Reconciliation API", 
              description="OpenRefine-compliant reconciliation service",
              docs_url="/docs")

class QueryPayload(BaseModel):
    query: str
    limit: int = 10

class BatchQueryPayload(BaseModel):
    queries: Dict[str, QueryPayload]

def create_app(reconciliation_service: ReconciliationService):
    @app.get("/reconcile")
    async def reconcile_get(query: str | None = None):
        if not query:
            raise HTTPException(status_code=400, detail={"error": "Missing 'query' parameter"})
        try:
            results = reconciliation_service.reconcile(query)
            return {"result": results}
        except Exception as e:
            raise HTTPException(status_code=500, detail={"error": f"Internal server error: {str(e)}"})

    @app.post("/reconcile")
    async def reconcile_post(payload: BatchQueryPayload):
        if not payload.queries:
            raise HTTPException(status_code=400, detail={"error": "Missing 'queries' in payload"})
        try:
            response = {}
            for query_key, query_data in payload.queries.items():
                results = reconciliation_service.reconcile(query_data.query)
                response[query_key] = {"result": results[:query_data.limit]}
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail={"error": f"Internal server error: {str(e)}"})

    return app
