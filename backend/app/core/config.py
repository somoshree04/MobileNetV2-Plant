
import os

class Settings:
    PROJECT_NAME: str = "Plant Disease Classifier API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",  # Standard React local development port
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Standard Vite local development port
        "*"                      
    ]

settings = Settings()