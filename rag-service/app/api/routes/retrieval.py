from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.domain.retrieval import RetrievalRequest, RetrievalResponse
from app.services.retrieval_service import RetrievalService

router = APIRouter(prefix="/v1/retrieval", tags=["retrieval"])


@router.post("", response_model=RetrievalResponse)
async def retrieve(
    request: RetrievalRequest,
    db: Session = Depends(get_db),
):
    service = RetrievalService(db)

    chunks = await service.retrieve(
        query=request.query,
        top_k=request.top_k,
    )

    return RetrievalResponse(chunks=chunks)