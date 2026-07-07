from abc import ABC, abstractmethod


class ChatProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        pass