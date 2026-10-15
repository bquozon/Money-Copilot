import json
import os
from typing import Protocol

from dotenv import load_dotenv
from openai import OpenAI

from money_copilot.agent.types import Message, Response, ToolCall

OPENAI_MODEL = "gpt-5-nano-2025-08-07"
PRICE_PER_INPUT_TOKEN = 0.25 / 1e6
PRICE_PER_OUTPUT_TOKEN = 1.5 / 1e6

# To relocate later in entry point
load_dotenv()


# Interface
class LLMClient(Protocol):
    def complete(self, messages: list[Message]) -> Response: ...


# Real LLM (OPEN_AI)
class OpenAIClient:
    def __init__(self, model: str = OPENAI_MODEL):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = model

    def complete(self, messages: list[Message]):
        input = [{"role": m.role, "content": m.content} for m in messages]
        llm_res = self.client.responses.create(model=self.model, input=input)
        tools = []
        for item in llm_res.output:
            if item.type == "function_call":
                tool = ToolCall(
                    id=item.call_id,
                    name=item.name,
                    arguments=json.loads(item.arguments),
                )
                tools.append(tool)

        response = Response(
            text=llm_res.output_text,
            tools=tools,
            price=llm_res.usage.input_tokens * PRICE_PER_INPUT_TOKEN
            + llm_res.usage.output_tokens * PRICE_PER_OUTPUT_TOKEN,
        )
        return response


class FakeLLM:
    def complete(self, messages):
        response = Response(
            text="Hello! This is just an automatic answer for testing purpose",
            tool_calls=[],
        )
        return response


# client = OpenAIClient()
# message = Message(role="user", content="My name is John Doe")
# res = client.complete([message])
# print(f"{res.text}, {res.price}")
