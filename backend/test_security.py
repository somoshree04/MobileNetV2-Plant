import pytest
import io
from fastapi import HTTPException, UploadFile
from starlette.datastructures import Headers
from app.core.security import validate_uploaded_image

def test_security_blocks_invalid_file_type():
    """Verifies that the filter catches and drops non-image file formats immediately."""
    fake_file = UploadFile(
        filename="malware.txt",
        file=io.BytesIO(b"import os; os.system('echo hacked')"),
        headers=Headers({"content-type": "text/plain"})
    )
    
    with pytest.raises(HTTPException) as exc_info:
        validate_uploaded_image(fake_file)
        
    assert exc_info.value.status_code == 400
    assert "Only JPEG, JPG, and PNG are allowed" in exc_info.value.detail


def test_security_blocks_oversized_payloads():
    """Verifies that files exceeding our rigid 5MB boundary are dropped before model execution."""
    huge_payload = b"\x00" * (6 * 1024 * 1024) # Simulated 6MB file
    
    fake_file = UploadFile(
        filename="huge_leaf_4k.png",
        file=io.BytesIO(huge_payload),
        headers=Headers({"content-type": "image/png"})
    )
    
    with pytest.raises(HTTPException) as exc_info:
        validate_uploaded_image(fake_file)
        
    assert exc_info.value.status_code == 413
    assert "Maximum size boundary is 5MB" in exc_info.value.detail


def test_security_blocks_corrupted_images():
    """Verifies that an image file that is broken or corrupted is stopped from entering PyTorch."""
    fake_file = UploadFile(
        filename="corrupted_leaf.jpg",
        file=io.BytesIO(b"This is just random corrupted plain text data inside an image wrapper"),
        headers=Headers({"content-type": "image/jpeg"})
    )
    
    with pytest.raises(HTTPException) as exc_info:
        validate_uploaded_image(fake_file)
        
    assert exc_info.value.status_code == 400
    assert "corrupted or structurally malicious" in exc_info.value.detail