from typing import Any

from pydantic import BaseModel


class Usage(BaseModel):
    input_tokens: int
    output_tokens: int


class Message(BaseModel):
    role: str
    content: str


class ToolCall(BaseModel):
    tool: str


class Response(BaseModel):
    text: str
    tools: list
    price: float


class ToolCall(BaseModel):
    id: str
    name: str
    arguments: dict[str, Any]
