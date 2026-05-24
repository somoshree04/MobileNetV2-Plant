

from fastapi import APIRouter, UploadFile, File, Request, status
from app.core.security import validate_uploaded_image
from app.services.inference import predict_leaf_disease
from slowapi import Limiter
from slowapi.util import get_remote_address
import shutil
import os

# Initializing the route controller and the IP rate limiter
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/predict", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute") # Restricts any single IP to 5 hits per minute
def predict_plant_disease(request: Request, file: UploadFile = File(...)):
    
    image_stream = validate_uploaded_image(file)
    
    # Saves stream to a temporary file locally on disk so Pillow/PyTorch can digest it safely
    temp_file_path = f"temp_{file.filename}"
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(image_stream, buffer)
            
        #  Passes the file path into PyTorch inference service
        remedy_payload = predict_leaf_disease(temp_file_path)
        return remedy_payload
        
    finally:
        #  Ensures that the temporary image is deleted from disk even if the model errors out
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)