from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_upload_and_chat():
    with open("sample.csv", "rb") as f:
        response = client.post("/Upload", files={"file": ("sample.csv", f, "text/csv")})
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    session_id = data["session_id"]
    
    response = client.post("/chat", json={"session_id": session_id, "message": "what are the columns in this csv?"})
    assert response.status_code == 200
    assert len(response.text) > 0
    print("Test passed! Response:")
    print(response.text)

if __name__ == "__main__":
    test_upload_and_chat()
