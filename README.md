# Money Copilot

A personal finance assistant built on an LLM agent loop: the model answers questions in natural language and calls Python tools to get the data it can't know on its own.

> Work in progress — currently a minimal agent loop with a demo `add` tool.

## How it works

```
main.py   loop()          ask the model → run requested tools → send results back → repeat
llm.py    OpenAIClient    talks to the OpenAI Responses API, converts to/from our types
tools.py  @tool           registers Python functions and builds their JSON schemas
agent/types.py            Message, ToolCall, Usage, Response (Pydantic models)
```

The agent only depends on the `LLMClient` protocol, so tests can swap the real client for a scripted fake (`tests/fakes.py`) — no network, no cost.

## Setup

Requires Python 3.13 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Create a `.env` file in the project root (it is git-ignored):

```
OPENAI_API_KEY=sk-...
```

## Usage

```bash
uv run python -m money_copilot.main
```

## Adding a tool

Decorate a typed function with `@tool` in `src/money_copilot/tools.py`. The docstring becomes the description the model reads:

```python
@tool
def get_balance(account: str) -> float:
    """Return the current balance of an account."""
    ...
```

## Development

```bash
uv run ruff check .   # lint
uv run pytest         # tests
```
