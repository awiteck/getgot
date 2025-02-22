from openai import OpenAI
import os
from dotenv import load_dotenv

from getgot.memory.basic_agent_memory import GetGot
from getgot.schemas.openai.chat_completion_request import UserMessage, AssistantMessage

load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def chat_loop():
    memory = GetGot(working_capacity=5)
    print("Starting chat...")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "q", "bye"]:
            break
        user_message = UserMessage(content=user_input)
        memory.add_message(user_message)
        messages = memory.construct_messages()
        response = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
        print(f"Assistant: {response.choices[0].message.content}")
        assistant_message = AssistantMessage(content=response.choices[0].message.content)
        memory.add_message(assistant_message)

if __name__ == "__main__":
    chat_loop()