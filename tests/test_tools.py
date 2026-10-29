from money_copilot import tools
from money_copilot.agent.types import ToolCall


def test_run_tool_returns_error_on_tool_exception(monkeypatch, tmp_path):
    monkeypatch.setattr(tools, "DB_PATH", str(tmp_path / "missing" / "money.db"))
    call = ToolCall(
        id="1", name="get_monthly_spending", arguments={"year": 2026, "month": 9}
    )
    res = tools.run_tool(call)
    assert res.startswith("Error: ")


def test_run_tool_returns_error_on_bad_argument():
    call = ToolCall(id="1", name="add", arguments={"x": 1})
    assert tools.run_tool(call).startswith("Error: ")
