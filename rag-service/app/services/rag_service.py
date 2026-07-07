from sqlalchemy.orm import Session

from app.providers.ollama_chat_provider import OllamaChatProvider
from app.services.context_builder import ContextBuilder
from app.services.prompt_builder import PromptBuilder
from app.services.retrieval_service import RetrievalService


class RagService:
    def __init__(self, db: Session):
        self.retrieval_service = RetrievalService(db)
        self.context_builder = ContextBuilder()
        self.prompt_builder = PromptBuilder()
        self.chat_provider = OllamaChatProvider()

    async def answer(
        self,
        query: str,
        top_k: int = 5,
    ):
        chunks = await self.retrieval_service.retrieve(
            query=query,
            top_k=top_k,
        )

        context = self.context_builder.build(chunks)

        prompt = self.prompt_builder.build(
            query=query,
            context=context,
        )

        answer = await self.chat_provider.generate(prompt)

        return answer, chunks