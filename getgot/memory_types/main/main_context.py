# src/getgot/memory/working.py
from collections import deque
from typing import List, Optional

from getgot.memory_types.base import BaseMemory
from getgot.models.message import Message
from getgot.log import logger
from getgot.memory_types.main.recent_messages import RecentMessages

class MainContext(BaseMemory):
    def __init__(self, llm,system_prompt: str, capacity: int = 20):
        self.system_prompt = system_prompt
        self.recent_messages = RecentMessages(llm=llm, capacity=capacity)

    def add(self, message: Message) -> None:
        self.recent_messages.add(message)

    def get(self, n: Optional[int] = None) -> List[Message]:
        """
        Get the last n messages from the recent messages.
        """
        if n is None:
            return list(self.recent_messages.messages)
        return self.recent_messages.messages[-n:]

    def clear(self) -> None:
        """
        Clear the recent messages.
        """
        self.recent_messages.clear()