from concurrent.futures import ThreadPoolExecutor
from datetime import date

from money_copilot.agent.types import Message
from money_copilot.finance.db import connect
from money_copilot.finance.importer import import_csv
from money_copilot.llm import FakeLLM, LLMClient
from money_copilot.openai_client import OpenAIClient
from money_copilot.tools import DB_PATH, SCHEMAS, run_tool

MAX_ITER = 5


def setup_db(csv_path: str) -> None:
    conn = connect(DB_PATH)
    try:
        added = import_csv(conn, csv_path)
        print(f"Imported {added} new transactions")
    finally:
        conn.close()


def loop(
    client: LLMClient, input: str, sys_prompt: str = "", verbose: bool = False
) -> str:
    msg = []
    sys_msg = Message(role="system", content=sys_prompt)
    usr_msg = Message(role="user", content=input)
    msg.append(sys_msg)
    msg.append(usr_msg)

    for i in range(MAX_ITER):
        res = client.complete(
            msg, tools=SCHEMAS, tool_choice="required" if i == 0 else "auto"
        )
        if not res.tools:  # When res.tools is an empty list
            return res.text

        msg.append(Message(role="assistant", content=res.text, tool_calls=res.tools))

        # Debugging lines
        if verbose:
            print(res)

        with ThreadPoolExecutor() as pool:
            results = list(pool.map(run_tool, res.tools))
        for call, result in zip(res.tools, results):
            new_msg = Message(role="tool", content=result, tool_call_id=call.id)
            msg.append(new_msg)
            if verbose:
                print(new_msg)

    return f"Error: no final answer after {MAX_ITER} rounds"


if __name__ == "__main__":
    setup_db("tests/fixtures/transactions_sample.csv")
    OPENAI_MODEL = "gpt-5-nano-2025-08-07"
    client = OpenAIClient(OPENAI_MODEL)

    fake_client = FakeLLM()
    print(
        loop(
            client,
            "On what months did I spend the most ?",
            sys_prompt="You are a finantial assistant. "
            "You have access to all the transactions via the tools."
            "Answer questions from the users and advise him on how to manage his/her money using the data."
            f"today is {date.today().isoformat()}",
            verbose=False,
        )
    )
