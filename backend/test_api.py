
import pytest
from fastapi.testclient import TestClient
from PIL import Image
import io
from main import app

client = TestClient(app)

def test_api_predict_endpoint_success_flow():
    """Validates a perfect user request flow through the entire API network pipeline."""
    img = Image.new("RGB", (224, 224), color="green")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    
    response = client.post(
        "/api/v1/predict",
        files={"file": ("test_leaf.png", img_byte_arr, "image/png")}
    )
    
    assert response.status_code == 200
    json_data = response.json()
    assert "disease_name" in json_data
    assert "chemical_treatment" in json_data


def test_api_rate_limiter_blocks_floods():
    """Spams the secure endpoint repeatedly to verify the rate limiter blocks traffic bursts."""
    img = Image.new("RGB", (224, 224), color="green")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    
    status_codes = []
    # Spam 6 times instantly
    for _ in range(6):
        img_byte_arr.seek(0)
        response = client.post(
            "/api/v1/predict",
            files={"file": ("spam_leaf.png", img_byte_arr, "image/png")}
        )
        status_codes.append(response.status_code)
        
    # The 6th request must trigger an HTTP 429 Too Many Requests status code
    assert 429 in status_codes, "Rate limiter failed to intercept and drop high-velocity traffic flood!"