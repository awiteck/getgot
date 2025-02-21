from typing import List, Optional
from datetime import datetime

from getgot.models.message import Message
from getgot.schemas.openai.chat_completion_request import UserMessage
from getgot.prompts.main.recent_messages import recent_messages_prompt
from getgot.log import logger

class RecentMessages:
    '''
    Organized like this:
    [
        [summary],
        [oldest_message],
        [2nd_oldest_message],
        ...
        [newest_message]
    ]   
    '''
    def __init__(self, llm, capacity: int = 20):
        self.capacity = capacity
        self.messages: List[Message] = []
        self.summary: Message = Message(
            role="system", 
            content="This conversation has just started! The entire history is here.",
            timestamp=datetime.now()
        )
        self.llm = llm


    def add(self, message: Message) -> None:
        """Add a new message to the queue. If queue exceeds max_size, update summary.
        
        Args:
            content: The message content
            msg_type: Type of message ('user', 'agent', 'system', 'function')
            metadata: Optional metadata for the message
        """
        self.messages.append(message)

        if len(self.messages) >= self.capacity:
            self._update_summary()
            self.messages.pop(0)

    def _update_summary(self) -> None:
        """Update the summary message"""
        oldest_message = self.messages[0]
        
        # Determine if oldest message is worth adding to the summary
        if self._is_worth_adding_to_summary(oldest_message):
            new_summary = self._generate_new_summary(oldest_message)
            self.summary = new_summary

        self.summary.content = self.llm.generate_summary(self.messages)

    def _is_worth_adding_to_summary(self, message: Message) -> bool:
        """Determine if the oldest message is worth adding to the summary
        TODO: Use LLM as a judge for this
        """
        return True
    
    def _generate_new_summary(self, message: Message) -> Message:
        """
        Generate a new summary message
        Don't do any function calling here, just parse the output
        """

        # TODO: add retry logic if response not parsed correctly
        try:
            prompt = recent_messages_prompt["user"].format(
                summary=self.summary.content,
                message=message.content
            )

            response = self.llm.chat(
                messages=[UserMessage(content=prompt)],
                system=recent_messages_prompt["system"]
            )

            try: 
                summary = response.split("<summary>")[1].split("</summary>")[0]
                return Message(role="system", content=summary, timestamp=datetime.now())
            except Exception as e:
                logger.error(f"Error parsing new summary: {e}. Returning original summary.")
                return self.summary

        except Exception as e:
            logger.error(f"Error generating new summary: {e}")
            return self.summary

    def clear(self) -> None:
        """Clear the recent messages"""
        self.messages = []
        self.summary = Message(role="system", content="This conversation has just started! The entire history is here.", timestamp=datetime.now())
