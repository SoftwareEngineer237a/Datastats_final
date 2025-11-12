import pytest
from unittest.mock import patch

@patch("app.api.chat.openai.chat.completions.create")
def test_chat_api(mock_openai, client):
    mock_openai.return_value = {"choices": [{"message": {"content": "Mocked response"}}]}
    
    response = client.post(
        "/api/chat",
        json={"message": "Explain GDP in simple terms"}
    )

    assert response.status_code == 200
    assert b"Mocked response" in response.data
