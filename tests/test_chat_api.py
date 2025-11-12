import json
import pytest
from app import create_app, db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # disable CSRF for testing
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_chat_api(client):
    response = client.post(
        "/api/chat",
        data=json.dumps({"message": "Explain GDP in simple terms"}),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "reply" in data
    print("\nAI Reply:", data["reply"])
