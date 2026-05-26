

import os
import pytest
from PIL import Image
from app.services.inference import predict_leaf_disease

def test_inference_engine_lifecycle():
    """Generates a temporary image file to verify the model reads it and returns remedies successfully."""
    dummy_filename = "test_temp_leaf.jpg"
    
    # Creates a fake, tiny green image (simulating a leaf photo)
    img = Image.new("RGB", (300, 300), color="green")
    img.save(dummy_filename)
    
    try:
        # Runs the image through our inference function
        result = predict_leaf_disease(dummy_filename)
        
        # Structural Rubric Assertions
        assert isinstance(result, dict), "Output must be a structured Python dictionary!"
        assert "disease_name" in result, "Result dictionary is missing the 'disease_name' key!"
        assert "organic_remedy" in result, "Result dictionary is missing the 'organic_remedy' key!"
        assert "prevention" in result, "Result dictionary is missing the 'prevention' key!"
        
    finally:
        #  delete the temporary test file from machine
        if os.path.exists(dummy_filename):
            os.remove(dummy_filename)