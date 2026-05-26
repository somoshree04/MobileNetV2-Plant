
import io
from fastapi import HTTPException
from PIL import Image

def validate_uploaded_image(file) -> bool:
    """
    Secures the application boundaries by sanitizing uploaded file types,
    enforcing maximum size constraints, and verifying structural integrity via Pillow.
    """
    # Validate MIME format extensions
    allowed_extensions = ["image/jpeg", "image/jpg", "image/png"]
    if file.content_type not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file format. Only JPEG, JPG, and PNG are allowed!"
        )
        
    # Enforce absolute file size boundary constraints (5MB Maximum limit)
    MAX_FILE_SIZE = 5 * 1024 * 1024 # 5 Megabytes in bytes
    
    # Read bytes to calculate length, then rewind the internal file stream pointer
    file_bytes = file.file.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Payload Too Large. Maximum size boundary is 5MB!"
        )
    file.file.seek(0) # Crucial: Reset the stream pointer back to byte zero
    
    # Structural Integrity Deep-Scan ( which is to Catch malicious scripts masquerading as images)
    try:
        # Wrap bytes in an in-memory stream buffer and pass it to Pillow
        img = Image.open(io.BytesIO(file_bytes))
        img.verify() # Checks if the underlying file structure is corrupted
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is corrupted or structurally malicious!"
        )
        
    return True