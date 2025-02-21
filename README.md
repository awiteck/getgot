# getgot

A super lightweight memory system for on-device AI agents. Inspired by [MemGPT](https://arxiv.org/abs/2310.08560) and the [CoALA framework](https://arxiv.org/abs/2309.02427).

## Code examples for how this should be used

Basic usage:
```python
from getgot import GetGot
from openai import OpenAI

class MyAgent:
    def __init__(self):
        self.llm = OpenAI()
        self.memory = GetGot()
    
    def chat(self, message: str) -> str:
        self.memory.add_message(UserMessage(message))
        messages = self.memory.construct_messages()
        response = self.llm.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        self.memory.add_message(AgentMessage(response.choices[0].message.content))
        return response.choices[0].message.content
```


## Things I want to implement

- Semantic memory
  - Efficient semantic memory consolidation
- Procedural memory
  - RLHF for procedural memory


## Related repos

- https://github.com/chisasaw/redcache-ai/tree/master
