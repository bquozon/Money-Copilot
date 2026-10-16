from concurrent.futures import ThreadPoolExecutor

from money_copilot.agent.types import Message
from money_copilot.llm import FakeLLM, LLMClient, OpenAIClient
from money_copilot.tools import run_tool

MAX_ITER = 5


def loop(client: LLMClient, input: str, sys_prompt: str = "") -> str:
    msg = []
    sys_msg = Message(role="system", content=sys_prompt)
    usr_msg = Message(role="user", content=input)
    msg.append(sys_msg)
    msg.append(usr_msg)

    for _ in range(MAX_ITER):
        res = client.complete(msg)
        if not res.tools:  # When res.tools is an empty list
            return res.text

        msg.append(Message(role="assistant", content=res.text, tool_calls=res.tools))

        with ThreadPoolExecutor() as pool:
            results = list(pool.map(run_tool, res.tools))
        for call, result in zip(res.tools, results):
            new_msg = Message(role="tool", content=result, tool_call_id=call.id)
            msg.append(new_msg)

    return f"Error: no final answer after {MAX_ITER} rounds"


OPENAI_MODEL = "gpt-5-nano-2025-08-07"
client = OpenAIClient(OPENAI_MODEL)

fake_client = FakeLLM()
print(loop(client, "How are you? What is 2+5?"))
