

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

@router.post("/predict")
@limiter.limit("5/minute")
def predict_plant_disease(request: Request, file: UploadFile = File(...)):
    #  Execute the security firewall verification pass
    # (Must Not re-assign 'file =' to this call!)
    validate_uploaded_image(file)
    
    # Extract the file's raw multi-part binary data stream pointer
    image_stream = file.file
    
    # Process the file cache lifecycle workspace smoothly
    temp_file_path = f"temp_{file.filename}"
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(image_stream, buffer)
            
        # Trigger PyTorch inference engine pipeline
        prediction_payload = predict_leaf_disease(temp_file_path)
        return prediction_payload
        
    finally:
        # Guaranteed clean-up pass to wipe local storage caches
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)