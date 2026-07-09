from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.domain.rag import RagRequest, RagResponse
from fastapi.responses import StreamingResponse
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

@router.post("/stream")
async def rag_stream(
    request: RagRequest,
    db: Session = Depends(get_db),
):
    service = RagService(db)

    async def event_generator():
        async for token in service.stream_answer(
            query=request.query,
            top_k=request.top_k,
        ):
            yield f"data: {token}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )