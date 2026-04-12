# PlantScan AI 🌿

An end-to-end Deep Learning application that detects diseases in plant leaves using Computer Vision. This project features a high-performance Python backend and a modern, responsive React frontend.

## 🚀 Features
- **Instant Diagnosis**: Upload a leaf image and get an immediate classification.
- **Confidence Scoring**: Uses Softmax probabilities to show how certain the AI is.
- **Treatment Recommendations**: Provides actionable advice based on the detected disease.
- **Modular Architecture**: Clean separation between AI logic, API handling, and UI components.

## 🛠️ Tech Stack
- **Frontend**: React.js (Vite), Tailwind CSS, Axios
- **Backend**: FastAPI (Python), Uvicorn
- **AI/ML**: PyTorch, Torchvision, PIL
- **Dataset**: PlantVillage Dataset (Trained on 38 different plant/disease classes)

## 📂 Project Structure
```text
Plant-Detection/
├── backend/
│   ├── main.py            # API Gateway & Routes
│   ├── model_logic.py     # PyTorch Inference Logic
│   ├── metadata.py        # Disease database & treatments
│   └── plant_model.pth    # Trained Weights
├── frontend/
│   ├── src/
│   │   ├── App.jsx        # Main UI Logic
│   │   └── index.css      # Tailwind Styles
│   └── tailwind.config.js
└── research/              # Jupyter Notebooks & Data Exploration


##  ⚙️Installation & Setup

```text

1. Backend Setup
cd backend
pip install -r requirements.txt
python main.py

2. Frontend Setup

cd frontend
npm install
npm run dev

