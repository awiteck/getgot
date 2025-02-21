import numpy as np
from pathlib import Path
from typing import List, Optional
from vlite import VLite
from getgot.memory_types.base import BaseMemory
from getgot.models.message import Message


class SemanticMemory:
    def __init__(self):
        self.vdb = VLite()
        self._init_store()

    def _init_store(self):
        pass

    def add(self, message: Message):
        self.vdb.add(message.content, metadata=...)
        # Embed message and store in database
        pass

    def search(self, query: str, top_k: int = 5) -> List[Message]:
        # Search for similar messages in the database
        pass

    def clear(self) -> None:
        # Clear the semantic memory
        pass
