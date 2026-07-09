from abc import ABC, abstractmethod
from collections.abc import AsyncIterator


class ChatProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        pass

    @abstractmethod
    async def stream(self, prompt: str) -> AsyncIterator[str]:
        pass