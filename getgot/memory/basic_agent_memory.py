from typing import Any, Dict, Optional, List

from getgot.prompts.semantic_context import semantic_context_prompt
from getgot.memory_types.main.main_context import MainContext
from getgot.memory_types.external.semantic_memory import SemanticMemory
from getgot.schemas.openai.chat_completion_request import ChatMessage, SystemMessage
from getgot.log import get_logger
from getgot.llm_api.base import BaseLLM

logger = get_logger(__name__)

class GetGot:
    def __init__(self, working_capacity: int = 20, llm: Optional[BaseLLM] = None):
        self._init_llm(llm)
        self.main_context = MainContext(capacity=working_capacity, llm=self.llm, system_prompt = "You are a helpful assistant.")
        self.semantic_memory = SemanticMemory() 

        
        # self.episodic_memory = EpisodicMemory()  

    def _init_llm(self, llm: Optional[BaseLLM] = None):
        if llm:
            self.llm = llm
        else:
            try:
                from getgot.llm_api.openai.openai_client import OpenAIClient
                self.llm = OpenAIClient()
            except Exception as e:
                logger.error(f"Error initializing LLM: {e}")
                raise e
            

    def add_message(self, message: ChatMessage):
        # Add message to main context
        self.main_context.add(message)
        self._process_messages()
    
    def construct_messages(self) -> List[Dict[str, Any]]:
        # Construct context for the LLM
        # Get main context
        main_context = self.main_context.get()

        # For now, just get the semantic memories based off the last user message
        last_user_message = self.main_context.get_last_user_message()
        semantic_context = self._get_semantic_context(last_user_message)

        # Convert ChatMessage objects to dicts that OpenAI expects
        messages = [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in main_context
        ]
        
        # Add semantic context as a system message
        if semantic_context:
            messages.append({
                "role": "system",
                "content": semantic_context.content
            })

        return messages

    def _get_semantic_context(self, query: str) -> SystemMessage:
        # Get semantic memories based off the last user message
        semantic_memories = self.semantic_memory.get(query)
        # Format the memories into a string
        semantic_context = semantic_context_prompt.format(context=semantic_memories)
        return SystemMessage(content=semantic_context)

    def _process_messages(self):
        pass

        # # Process messages and create new episodic memory if necessary

        # # Get working memory
        # working_context = self.working_memory.get()

        # # Generate episodic memory if appropriate
        # episodic_memory = self.llm.generate_episodic_memory(working_context)
        # if episodic_memory:
        #     self.episodic_memory.add(episodic_memory)

        # # Generate semantic memories if appropriate
        # semantic_memories = self.llm.generate_semantic_memory(working_context)
        # for memory in semantic_memories:
        #     self.semantic_memory.add(memory)

    def get_relevant_semantic_memories(
        self, query: str, k: Optional[int] = None
    ) -> List[ChatMessage]:
        return self.semantic_memory.get(query)

    def get_working_memory(self, n: Optional[int] = None) -> List[ChatMessage]:
        """Get the n most recent messages from working memory."""
        return self.working_memory.get(n)

    def clear_working_memory(self) -> None:
        """Clear working memory while preserving other memories."""
        self.working_memory.clear()

    @property
    def summary(self) -> Dict[str, Any]:
        """Get a summary of current memory state."""
        return {
            "working_memory_size": len(self.get_working_memory()),
            "episodic_memory_count": self.episodic_memory.count(),
            "semantic_memory_count": self.semantic_memory.count(),
        }
