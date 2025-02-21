import pytest

from getgot.llm_api.openai.openai_client import OpenAIClient
from getgot.memory_types.main.main_context import MainContext
from getgot.schemas.openai.chat_completion_request import UserMessage, AssistantMessage

'''
We want to test that 
- we can create a main context object
- we can add a message to the main context
- summarization works as expected
- we can get the messages from the main context
'''

capacity = 5

@pytest.fixture
def llm():
    return OpenAIClient()

@pytest.fixture
def main_context(llm):
    # Setup
    context = MainContext(llm=llm, system_prompt="You are a helpful assistant.", capacity=capacity)
    # Provide the fixture
    yield context
    # Cleanup after each test
    context.clear()  # Assuming your MainContext class has a clear() method

def test_create_main_context(main_context: MainContext):
    assert main_context is not None

def test_add_message_to_main_context(main_context: MainContext):
    message = UserMessage(content="Hey there, what's up?")
    main_context.add(message)
    assert len(main_context) == 2

def test_get_messages_from_main_context(main_context: MainContext):
    message = UserMessage(role="user", content="Hey there, what's up?")
    main_context.add(message)
    messages = main_context.get()
    print(messages)
    assert len(messages) == 3
    assert messages[0].role == "system"
    assert messages[0].content == "You are a helpful assistant."

def test_summarize_messages(main_context: MainContext):
    messages = [
        UserMessage(content="Hey there, what's up?"),
        AssistantMessage(content="I'm doing well, thanks for asking!"),
        UserMessage(content="What is a cool bar in SF?"),
        AssistantMessage(content="I recommend the Mission. It's a great neighborhood with a lot of cool bars."),
        UserMessage(content="Nice, I went to Bar Part Time last weekend and it was pretty cool."),
        AssistantMessage(content="Cool! That's a pretty good one. If you want some niche shit though, I'd try out Cafe Bazaar. It's a coffee shop in Inner Richmond but they have small concerts pretty often."),
        # Change topics 
        UserMessage(content="I'll check it out. What are some cool music artists from SF?"),
        AssistantMessage(content="Hmm... My favorite is probably LSD and the Search for God. They're a shoegaze band from SF. Not sure if that's your thing, but they're really good."),
        UserMessage(content="Hell yeah ok. Will do. I like Death Grips"),
        AssistantMessage(content="Omg slay. I also love DG! Did you hear they recent news? :("),
        UserMessage(content="No.. what happened"),
        AssistantMessage(content="Some dm got leaked with Andy and he said they're breaking up")
    ]
    for i, message in enumerate(messages):
        main_context.add(message)
        assert len(main_context) == min(i + 2, capacity+1)

    messages = main_context.get()
    print(messages)