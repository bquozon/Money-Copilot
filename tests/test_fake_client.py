from money_copilot.agent.types import Message, Response
from tests.fakes import FakeClient


def make_response(text: str) -> Response:
    return Response(text=text, tools=[])


def test_fake_returns_responses():
    client = FakeClient([make_response("first"), make_response("second")])
    msgs = [Message(role="user", content="hi")]

    assert client.complete(msgs).text == "first"
    assert client.complete(msgs).text == "second"
    assert len(client.calls) == 2
    
