import httpx

from app.core.config import settings
from app.providers.chat_provider import ChatProvider


class OllamaChatProvider(ChatProvider):
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_chat_model

    async def generate(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["response"]