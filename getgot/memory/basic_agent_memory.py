from typing import Any, Dict, Optional, List

from getgot.memory_types.main.main_context import MainContext
from getgot.memory_types.external.semantic_memory import SemanticMemory
from getgot.llm_api.base import DefaultLLM
from getgot.schemas.openai.chat_completion_request import ChatMessage
from getgot.log import logger

logger = logger.get_logger(__name__)

class GetGot:
    def __init__(self, working_capacity: int = 20):
        self.main_context = MainContext(capacity=working_capacity)
        self.semantic_memory = SemanticMemory() 
        # self.episodic_memory = EpisodicMemory()  
        self.llm = DefaultLLM()

    def add_message(self, message: ChatMessage):
        # Add message to working memory
        self.working_memory.add(message)
        self._process_messages()
    
    def construct_context(self, query: str) -> str:
        # Construct context for the LLM
        pass


    def _process_messages(self):
        # Process messages and create new episodic memory if necessary

        # Get working memory
        working_context = self.working_memory.get()

        # Generate episodic memory if appropriate
        episodic_memory = self.llm.generate_episodic_memory(working_context)
        if episodic_memory:
            self.episodic_memory.add(episodic_memory)

        # Generate semantic memories if appropriate
        semantic_memories = self.llm.generate_semantic_memory(working_context)
        for memory in semantic_memories:
            self.semantic_memory.add(memory)

    def get_relevant_semantic_memories(
        self, query: str, k: Optional[int] = None
    ) -> List[ChatMessage]:
        return self.semantic_memory.search(query, k)

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
