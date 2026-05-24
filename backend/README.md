
# ⚙️ Plant Disease Classifier — Backend

This directory houses the enterprise-grade **FastAPI** backend microservice for the 38-class Plant Disease Classifier. It abstracts the underlying PyTorch machine learning logic behind structured, asynchronous web channels—hardened with file sanitation headers, API rate limit safeguards, and decoupled modular layer logic.
---

## Folder Structure

```
📁 plant-disease-backend/
│
├── 📁 app/
│   ├── 📁 api/
│   │   └── v1_predict.py       # POST /predict endpoint
│   ├── 📁 core/
│   │   ├── config.py           # CORS policies & global config
│   │   └── security.py         # File sanitization middleware
│   └── 📁 services/
│       └── inference.py        # PyTorch weight loading & inference logic
│
├── 🧠 plant_model.pth          # Serialized MobileNetV2 weights (~9 MB)
├── 📑 classes.json             # Integer → disease label map
├── 📑 remedies.json            # Disease → treatment lookup
├── ⚙️  main.py                 # App entry point
├── 📄 requirements.txt         # Dependencies
├── 🐳 Dockerfile               # Container definition
│
├── 🧪 test_inference.py        # Unit test: preprocessing & weight loading
├── 🧪 test_security.py         # Unit test: malicious file & size limits
└── 🧪 test_api.py              # Unit test: endpoint performance & rate limits
```

---

## Architecture

### 1 — Service Layer Decoupling (`app/services/inference.py`)
ML inference is fully isolated from HTTP routing. On startup, `inference.py` re-instantiates the MobileNetV2 graph with a 38-node output head and loads the trained weights under `torch.no_grad()`.

Prediction results are resolved through a two-stage lookup:
- `classes.json` — translates the model's integer output to a disease label
- `remedies.json` — maps that label to structured treatment data (chemical, organic, and preventative recommendations)

### 2 — Input Sanitization (`app/core/security.py`)
Every upload is validated before reaching the model:

| Check | Rule |
|---|---|
| MIME type | Must be `image/jpeg` or `image/png` |
| File size | Hard cap at **5 MB** |
| Pixel integrity | PIL color conversion verified before tensor generation |

### 3 — Rate Limiting & CORS
Uses `slowapi` to prevent API abuse and runaway cloud compute costs:
- **5 requests / minute** per unique client IP
- Returns `HTTP 429` on breach
- CORS restricted to an explicit domain whitelist

### 4 — Container Deployment (`Dockerfile`)
The app ships as a self-contained Docker image, guaranteeing consistent execution across local dev, PowerShell, AWS EC2, and Google Cloud Run — single command to run anywhere.

```bash
docker build -t plant-disease-backend .
docker run -p 8000:8000 plant-disease-backend
```

---

## API

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/predict` | Upload a leaf image, returns disease label + remedy |

**Request:** `multipart/form-data` with an image file  
**Response:**
```json
{
  "disease": "Tomato___Late_blight",
  "confidence": 0.97,
  "remedy": { "chemical": "...", "organic": "...", "prevention": "..." }
}
```

---

## Tech Stack

| | |
|---|---|
| Framework | FastAPI |
| ML Runtime | PyTorch (`torch.no_grad()`) |
| Base Model | MobileNetV2 (38-class head) |
| Rate Limiting | slowapi |
| Image Handling | Pillow (PIL) |
| Deployment | Docker |