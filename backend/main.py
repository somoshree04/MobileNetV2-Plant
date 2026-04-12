import io
import json
import torch
import torch.nn as nn
from torchvision import models,transforms
from PIL import Image
from fastapi import FastAPI,File,UploadFile
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],

)

with open("classes.json" , "r") as f:
    class_name=json.load(f)

device=torch.device("cpu")

model=models.mobilenet_v2()

num_classes = len(class_name)
model.classifier[1] = nn.Linear(model.last_channel, num_classes)

model.load_state_dict(torch.load("plant_model .pth", map_location=device))
model.eval()

def transform_image(image_bytes):
    transform = transforms.Compose([
        transforms.Resize((224, 224)), 
        transforms.ToTensor(),        
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return transform(image).unsqueeze(0)

@app.post("/predict") 
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    
    tensor = transform_image(image_bytes)
    
    with torch.no_grad():
        outputs = model(tensor) 
        _, predicted = torch.max(outputs, 1) 
        
    prediction = class_name[predicted.item()]
    
    return {"prediction": prediction}


if __name__ == "__main__":
    import uvicorn
    # This actually starts the engine on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)