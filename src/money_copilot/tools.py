import inspect
import json

from money_copilot.agent.types import ToolCall

TOOLS = {}
SCHEMAS = []

PY_TO_JSON = {str: "string", int: "integer", float: "number", bool: "boolean"}


def tool(func):
    params = inspect.signature(func).parameters
    SCHEMAS.append(
        {
            "type": "function",
            "name": func.__name__,
            "description": func.__doc__ or "",
            "parameters": {
                "type": "object",
                "properties": {
                    n: {"type": PY_TO_JSON[p.annotation]} for n, p in params.items()
                },
                "required": list(params),
                "additionalProperties": False,
            },
            "strict": True,
        }
    )
    TOOLS[func.__name__] = func
    return func


def run_tool(call: ToolCall) -> str:
    if call.name not in TOOLS:
        return f"Error: unknown tool '{call.name}'"
    try:
        result = TOOLS[call.name](**call.arguments)
    except TypeError as e:
        return f"Error: bad argument: {e}"
    return json.dumps(result)


@tool
def add(x: int, y: int):
    """
    Adds two numbers together
    """
    print(f"Tool add was called and returned {x + y} ")
    return x + y
