from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@patch("main.s3.put_object")
@patch("main.s3.generate_presigned_url")
def test_generate_qr(mock_presigned_url, mock_put_object):
    mock_presigned_url.return_value = "https://qr-app-local-s3.s3.amazonaws.com/qr_codes/example.com.png?presigned=true"
    
    url = "http://example.com"
    response = client.post("/generate-qr/", params={"url": url})

    assert response.status_code == 200
    assert "qr_code_url" in response.json()

def test_generate_qr_invalid_url():
    response = client.post("/generate-qr/")

    assert response.status_code == 422  # FastAPI validation error