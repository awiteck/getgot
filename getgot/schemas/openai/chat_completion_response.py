'''
Copied from https://github.com/letta-ai/letta/blob/main/letta/schemas/openai/chat_completion_response.py
'''

import datetime
from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel

# class ToolCallFunction(BaseModel):
#     name: str
#     arguments: str


class CompletionTokensDetails(BaseModel):
    accepted_prediction_tokens: int = 0
    audio_tokens: int = 0
    reasoning_tokens: int = 0
    rejected_prediction_tokens: int = 0

class PromptTokensDetails(BaseModel):
    audio_tokens: int = 0
    cached_tokens: int = 0

class CompletionUsage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
    completion_tokens_details: CompletionTokensDetails
    prompt_tokens_details: PromptTokensDetails

class ChatCompletionMessage(BaseModel):
    content: Optional[str]
    role: str
    refusal: Optional[str] = None
    audio: Optional[str] = None
    function_call: Optional[dict] = None
    tool_calls: Optional[List[dict]] = None

class Choice(BaseModel):
    finish_reason: str
    index: int
    logprobs: Optional[dict] = None
    message: ChatCompletionMessage

class ChatCompletionResponse(BaseModel):
    id: str
    choices: List[Choice]
    created: int
    model: str
    object: Literal["chat.completion"]
    service_tier: str = "default"
    system_fingerprint: str
    usage: CompletionUsage

    class Config:
        from_attributes = True

    @property
    def content(self) -> Optional[str]:
        """Helper to get the content of the first message"""
        return self.choices[0].message.content


class FunctionCallDelta(BaseModel):
    # arguments: Optional[str] = None
    name: Optional[str] = None
    arguments: str
    # name: str


class ToolCallDelta(BaseModel):
    index: int
    id: Optional[str] = None
    # "Currently, only function is supported"
    type: Literal["function"] = "function"
    # function: ToolCallFunction
    function: Optional[FunctionCallDelta] = None


class MessageDelta(BaseModel):
    """Partial delta stream of a Message

    Example ChunkResponse:
    {
        'id': 'chatcmpl-9EOCkKdicNo1tiL1956kPvCnL2lLS',
        'object': 'chat.completion.chunk',
        'created': 1713216662,
        'model': 'gpt-4-0613',
        'system_fingerprint': None,
        'choices': [{
            'index': 0,
            'delta': {'content': 'User'},
            'logprobs': None,
            'finish_reason': None
        }]
    }
    """

    content: Optional[str] = None
    reasoning_content: Optional[str] = None
    tool_calls: Optional[List[ToolCallDelta]] = None
    role: Optional[str] = None
    function_call: Optional[FunctionCallDelta] = None  # Deprecated


class ChunkChoice(BaseModel):
    finish_reason: Optional[str] = None  # NOTE: when streaming will be null
    index: int
    delta: MessageDelta
    logprobs: Optional[dict] = None


class ChatCompletionChunkResponse(BaseModel):
    """https://platform.openai.com/docs/api-reference/chat/streaming"""

    id: str
    choices: List[ChunkChoice]
    created: Union[datetime.datetime, str]
    model: str
    # system_fingerprint: str  # docs say this is mandatory, but in reality API returns None
    system_fingerprint: Optional[str] = None
    # object: str = Field(default="chat.completion")
    object: Literal["chat.completion.chunk"] = "chat.completion.chunk"