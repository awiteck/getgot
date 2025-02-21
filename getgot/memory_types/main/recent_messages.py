from typing import List, Optional
from datetime import datetime

from getgot.schemas.openai.chat_completion_request import UserMessage, ChatMessage, SystemMessage
from getgot.prompts.main.recent_messages import recent_messages_prompt
from getgot.schemas.openai.chat_completion_request import ChatCompletionRequest
from getgot.llm_api.base import BaseLLM
from getgot.settings import model_settings
from getgot.log import get_logger

logger = get_logger(__name__)

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
    def __init__(self, llm: BaseLLM, capacity: int = 20):
        self.capacity = capacity
        self.messages: List[ChatMessage] = []
        self.summary: ChatMessage = SystemMessage(
            role="system", 
            content="This conversation has just started! The entire history is here.",
            timestamp=datetime.now()
        )
        self.llm = llm

    def __len__(self) -> int:
        # 1 for the summary
        return 1 + len(self.messages)


    def add(self, message: ChatMessage) -> None:
        """Add a new message to the queue. If queue exceeds max_size, update summary.
        
        Args:
            content: The message content
            msg_type: Type of message ('user', 'agent', 'system', 'function')
            metadata: Optional metadata for the message
        """
        self.messages.append(message)

        if len(self.messages) > self.capacity:
            self._update_summary()
            self.messages.pop(0)

    def get(self) -> List[ChatMessage]:
        """Get the recent messages, with the summary at the front"""
        return [self.summary] + self.messages
    
    def _update_summary(self) -> None:
        """Update the summary message"""
        oldest_message = self.messages[0]
        
        # Determine if oldest message is worth adding to the summary
        if self._is_worth_adding_to_summary(oldest_message):
            new_summary = self._generate_new_summary(oldest_message)
            self.summary = new_summary

    def _is_worth_adding_to_summary(self, message: ChatMessage) -> bool:
        """Determine if the oldest message is worth adding to the summary
        TODO: Use LLM as a judge for this
        """
        return True
    
    def _generate_new_summary(self, message: ChatMessage) -> SystemMessage:
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
            messages = [
                SystemMessage(content=recent_messages_prompt["system"]),
                UserMessage(content=prompt)
            ]

            response = self._call_llm(messages)


            try: 
                print(f"response: {response}")
                summary = response.choices[0].message.content.split("<summary>")[1].split("</summary>")[0]
                return SystemMessage(content=summary, timestamp=datetime.now())
            except Exception as e:
                logger.error(f"Error parsing new summary: {e}. Returning original summary.")
                return self.summary

        except Exception as e:
            logger.error(f"Error generating new summary: {e}")
            return self.summary
        
    def _call_llm(self, messages: List[ChatMessage]) -> str:
        """Call the LLM with the prompt"""
        request = ChatCompletionRequest(
            model=model_settings.OPENAI_MODEL,
            messages=messages,
            system=recent_messages_prompt["system"]
        )
        return self.llm.chat(request)

    def clear(self) -> None:
        """Clear the recent messages"""
        self.messages = []
        self.summary = SystemMessage(content="This conversation has just started! The entire history is here.", timestamp=datetime.now())

