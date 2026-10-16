
from typing import Protocol



from money_copilot.agent.types import Message, Response, ToolCall



# Interface
class LLMClient(Protocol):
    def complete(self, messages: list[Message]) -> Response: ...

class FakeLLM:
    def complete(self, messages):
        response = Response(
            text="Hello! This is just an automatic answer for testing purpose",
            tool_calls=[],
        )
        return response


