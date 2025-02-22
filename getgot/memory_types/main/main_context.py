# src/getgot/memory/working.py
from typing import List, Optional

from getgot.memory_types.base import BaseMemory
from getgot.schemas.openai.chat_completion_request import SystemMessage, ChatMessage
from getgot.log import get_logger
from getgot.memory_types.main.recent_messages import RecentMessages

logger = get_logger(__name__)

class MainContext(BaseMemory):
    def __init__(self, llm, system_prompt: str, capacity: int = 20):
        self.system_prompt = SystemMessage(content=system_prompt)
        self.recent_messages = RecentMessages(llm=llm, capacity=capacity)

    def add(self, message: ChatMessage) -> None:
        self.recent_messages.add(message)
        logger.debug(self.__str__())

    def get(self) -> List[ChatMessage]:
        """
        Get the recent messages, with the system prompt at the front.
        """
        recent_messages = self.recent_messages.get()
        return [self.system_prompt] + recent_messages
    
    def get_last_user_message(self) -> Optional[ChatMessage]:
        """
        Get the last user message.
        """
        return self.recent_messages.get_last_user_message()

    def clear(self) -> None:
        """
        Clear the recent messages.
        """
        self.recent_messages.clear()

    def __str__(self) -> str:
        return f"MainContext(system_prompt={self.system_prompt}, recent_messages={self.recent_messages})"
    
    def __len__(self) -> int:
        return len(self.recent_messages)
