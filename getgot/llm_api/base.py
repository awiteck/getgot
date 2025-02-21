from abc import ABC, abstractmethod
from typing import List
from src.getgot.models.message import Message


class BaseLLM(ABC):
    @abstractmethod
    def generate_episodic_memory(self, messages: List[Message]) -> Message:
        pass

    @abstractmethod
    def generate_semantic_memory(self, messages: List[Message]) -> Message:
        pass
