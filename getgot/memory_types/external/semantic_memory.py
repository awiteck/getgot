from typing import List
from getgot.memory_types.base import BaseMemory
from getgot.schemas.openai.chat_completion_request import ChatMessage

class SemanticMemory(BaseMemory):
    def __init__(self):
        pass

    def add(self, message: ChatMessage) -> None:
        pass

    def get(self) -> List[ChatMessage]:
        pass
