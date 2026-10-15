from money_copilot.agent.types import Message, Response


class FakeClient:
    def __init__(self, responses: list[Response]):
        self.responses = responses
        self.calls: list[list[Message]] = []  # to record what the client received

    def complete(self, messages: list[Message]) -> Response:
        self.calls.append(messages)
        return self.responses.pop(0)
