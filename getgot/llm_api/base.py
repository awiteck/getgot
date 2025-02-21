from abc import ABC, abstractmethod
from getgot.schemas.openai.chat_completion_request import ChatCompletionRequest
from getgot.schemas.openai.chat_completion_response import ChatCompletionResponse

class BaseLLM(ABC):
    @abstractmethod
    def chat(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        pass
