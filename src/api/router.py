import uuid

from fastapi import APIRouter, HTTPException, Request

from src.api.schemas import QueryRequest, QueryResponse
from src.core.orchestrator import OrchestratorAgent

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def process_query(payload: QueryRequest, request: Request):
    orchestrator: OrchestratorAgent | None = getattr(
        request.app.state, "orchestrator", None
    )
    if orchestrator is None:
        raise HTTPException(status_code=500, detail="System not initialized")

    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Request cannot be empty")

    _ = request.headers.get("X-Request-ID", str(uuid.uuid4()))

    try:
        result = await orchestrator.arun(payload.query)
        return QueryResponse(status="success", query=payload.query, result=result)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}"
        )
