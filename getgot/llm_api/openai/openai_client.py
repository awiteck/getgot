from openai import OpenAI
import os
from typing import Optional, List

from getgot.log import get_logger
from getgot.llm_api.base import BaseLLM
from getgot.schemas.openai.chat_completion_request import ChatCompletionRequest, ChatMessage
from getgot.schemas.openai.chat_completion_response import ChatCompletionResponse
from getgot.settings import model_settings

logger = get_logger(__name__)

class OpenAIClient(BaseLLM):
    def __init__(self, api_key: Optional[str] = None):
        if not api_key:
            try: 
                api_key = model_settings.OPENAI_API_KEY
            except Exception as e:
                logger.error(f"Error getting OpenAI API key: {e}")
                raise e
        self.client = OpenAI(api_key=api_key)

    def chat(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        payload = request.model_dump()
        chat_completion = self.client.chat.completions.create(**payload)
        return ChatCompletionResponse(**chat_completion.model_dump())