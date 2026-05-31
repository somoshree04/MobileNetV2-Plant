

# 🍃 Green Guard — AI Plant Disease Scanner

Green Guard is a full-stack deep learning web app that diagnoses plant leaf diseases from uploaded images. Powered by a custom-trained **MobileNetV2** neural network, it returns instant disease identification alongside organic remedies, chemical treatments, and preventative care plans.

---

## How It Works

Upload a photo of a plant leaf → the model classifies it across **38 disease categories** → the backend returns a structured treatment plan in real time.

---

## Modules

| Directory | Role |
|---|---|
| `/research` | Data ingestion, MobileNetV2 training pipeline, model export |
| `/backend` | FastAPI production server — rate limiting, validation, inference |
| `/frontend` | React + TypeScript dashboard — upload UI, results display |

---

## Features

- **Instant AI Diagnosis** — real-time leaf classification via an optimized MobileNetV2 vision model
- **Structured Remediation** — results include condition name, organic remedy, chemical treatment, and prevention guidelines
- **Rate Limiting** — `slowapi` enforces per-IP request caps to protect server resources
- **Type-Safe Stack** — TypeScript interfaces on the client, Pydantic models on the server

---

## Getting Started

### Prerequisites
- Python `3.10+`
- Node.js `v18+`
- npm or yarn

---

### 1 — Backend

```bash
cd backend

# Create & activate virtual environment
python -m venv venv
.\venv\Scripts\Activate   # Windows
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 2 — Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | React 18, TypeScript, Vite, Tailwind CSS |
| Backend | FastAPI, Uvicorn, Slowapi, Pydantic |
| ML | PyTorch, MobileNetV2, Jupyter Notebook |

---

## Dataset

The training pipeline uses the **PlantVillage Dataset** maintained by [Sharada Mohanty](https://github.com/spMohanty/PlantVillage-Dataset) — a collection of high-resolution, multi-class plant leaf images spanning healthy and diseased biological classifications.

The archive is streamed, unpacked, and normalized directly inside the research pipeline:

```
https://github.com/spMohanty/PlantVillage-Dataset/archive/refs/heads/master.zip
```