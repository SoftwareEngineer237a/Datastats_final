import pytest
from openai import OpenAI

# -----------------------
# Mock OpenAI response
# -----------------------
class MockChatResponse:
    def __init__(self, content="Hello from mock!"):
        self.choices = [type("obj", (), {"message": {"content": content}})]


def test_chat_api(monkeypatch):
    client = OpenAI()

    # Monkeypatch the completions.create method
    def mock_create(*args, **kwargs):
        return MockChatResponse("Mocked response")

    monkeypatch.setattr(client.chat.completions, "create", mock_create)

    # Now calling it will use the fake response
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello?"}]
    )

    assert response.choices[0].message["content"] == "Mocked response"
