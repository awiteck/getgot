# src/getgot/memory/base.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.getgot.models.message import Message


class BaseMemory(ABC):
    @abstractmethod
    def add(self, message: Message) -> None:
        pass

    @abstractmethod
    def get(self, **kwargs) -> List[Message]:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass
