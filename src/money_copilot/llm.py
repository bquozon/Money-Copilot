from typing import Protocol

from money_copilot.agent.types import Message, Response, ToolCall


# Interface
class LLMClient(Protocol):
    def complete(self, messages: list[Message]) -> Response: ...


class FakeLLM:
    def complete(self, messages, tools, tool_choice):
        tool_call = ToolCall(
            id="c1",
            name="get_monthly_spending",
            arguments={"month": 9, "year": 2026},
        )
        response = Response(
            text="",
            tool_calls=[tool_call],
        )
        return response
