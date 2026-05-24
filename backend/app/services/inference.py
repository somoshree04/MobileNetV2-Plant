
import os
import json
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Rebuilding the MobileNetV2 architecture frame, from the Colab
model = models.mobilenet_v2(weights=None)
in_features = model.classifier[1].in_features
model.classifier[1] = nn.Linear(in_features, 38) 

# Loading the trained weights safely from the backend root folder
# also checking if the current folder and the parent folder are there easily
MODEL_PATH = "plant_model.pth"
if not os.path.exists(MODEL_PATH) and os.path.exists("../plant_model.pth"):
    MODEL_PATH = "../plant_model.pth"

if os.path.exists(MODEL_PATH):
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))

model.to(device)
model.eval() # Freeze the model into Evaluation Mode

CLASSES_PATH = "classes.json" if os.path.exists("classes.json") else "../classes.json"
REMEDIES_PATH = "remedies.json" if os.path.exists("remedies.json") else "../remedies.json"

with open(CLASSES_PATH, "r") as f:
    class_indices = json.load(f)

with open(REMEDIES_PATH, "r") as f:
    remedies_db = json.load(f)

# Preprocessing transforms conveyor belt
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def predict_leaf_disease(image_path: str) -> dict:
    # Opening the image using Pillow and converting it to standard RGB color space
    img = Image.open(image_path).convert("RGB")
    
    # Run the image through transforms and add a batch dimension (unsqueeze)
    tensor = transform(img).unsqueeze(0).to(device)
    
    # Turn off tracking gradients to save speed and CPU memory
    with torch.no_grad():
        outputs = model(tensor)
        _, predicted_index = torch.max(outputs, 1)
        idx = predicted_index.item()
    
    # Translate numeric index back to the flat array text label
    string_label = class_indices[idx]
    
    # remedies database using that label
    advice = remedies_db.get(string_label, {
        "disease_name": string_label,
        "chemical_treatment": "Consult local agricultural extension office.",
        "organic_remedy": "Prune affected leaves immediately.",
        "prevention": "Ensure proper field drainage and crop spacing."
    })
    
    return advice