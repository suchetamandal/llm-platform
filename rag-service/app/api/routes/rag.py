from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.domain.rag import RagRequest, RagResponse
from app.services.rag_service import RagService

router = APIRouter(prefix="/v1/rag", tags=["rag"])


@router.post("", response_model=RagResponse)
async def rag(
    request: RagRequest,
    db: Session = Depends(get_db),
):
    service = RagService(db)

    answer, chunks = await service.answer(
        query=request.query,
        top_k=request.top_k,
    )

    return RagResponse(
        answer=answer,
        chunks=chunks,
    )