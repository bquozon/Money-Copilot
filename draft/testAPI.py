import os

from dotenv import load_dotenv
from openai import OpenAI

OpenAI_Model = "gpt-5-nano-2025-08-07"
load_dotenv()

tools = [
    {
        "type": "function",
        "name": "add",
        "description": "adds two integers",
        "parameters": {
            "x": {"type": "number", "description": "first integer"},
            "y": {"type": "number", "description": "second integer"},
        },
        "required": ["x", "y"],
        "additionalProperties": False,
    }
]


def add(x, y):
    return x + y


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
response = client.responses.create(
    model=OpenAI_Model,
    tools=tools,
    input="Hey, how are you ? add 5 and 6 tgth",
    tool_choice="required",
)

for item in response.output:
    print(f"{item} \n")

print(response.input_tokents)
