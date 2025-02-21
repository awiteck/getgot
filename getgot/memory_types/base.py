# src/getgot/memory/base.py
from abc import ABC, abstractmethod
from typing import List, Optional
from getgot.schemas.openai.chat_completion_request import ChatMessage

class BaseMemory(ABC):
    @abstractmethod
    def add(self, message: ChatMessage) -> None:
        pass

    @abstractmethod
    def get(self, **kwargs) -> List[ChatMessage]:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass
