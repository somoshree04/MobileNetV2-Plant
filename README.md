
# 🍃 Green Guard: AI-Powered Plant Disease Scanner

Green Guard is a full-stack deep learning web application that allows agriculturalists, researchers, and home gardeners to upload images of plant leaves and receive instant, actionable health diagnoses. Powered by a custom-trained **MobileNetV2** neural network, the system detects leaf anomalies and returns automated organic remedies, chemical treatments, and preventative care plans.

---

## 🏗️ System Architecture

The application is split into three decoupled modules:
1. **Research Pipeline (`/research`)**: Data processing, training, and export scripts for the MobileNetV2 computer vision model.
2. **Backend API (`/backend`)**: A robust FastAPI production server wrapped with client rate-limiting and structured data validation.
3. **Frontend Dashboard (`/frontend`)**: A responsive, lightning-fast TypeScript React dashboard stylized with Tailwind CSS.

---

## ✨ Features

* **Instant AI Diagnosis**: Real-time evaluation of leaf geometry using an optimized computer vision model.
* **Comprehensive Remediation Plans**: Delivers structured advice broken into Condition Names, Organic Remedies, Chemical Treatments, and Prevention Guidelines.
* **API Rate Limiting**: Built-in traffic defense using `slowapi` to prevent server resource exhaustion.
* **Type-Safe Endpoints**: Strict data models using TypeScript interfaces on the client and Pydantic on the server to prevent data schema mismatches.

---

## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* Node.js v18+
* npm or yarn

---

### 🎛️ 1. Backend Server Setup

Navigate to the backend directory, spin up your virtual environment, install the modules, and boot the server:

```bash
cd backend

# Create and activate the virtual environment
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the production server
uvicorn main:app --reload --host 127.0.0.1 --port 8000

### 🎛️ 2. Frontend Interface Setup

Navigate to the frontend folder, install the node modules, and launch the Vite development server:

```bash
cd frontend

# Install UI modules
npm install

# Start Vite server
npm run dev

## 🛠️ Technology Stack

* **Frontend**: React 18, TypeScript, Vite, Tailwind CSS
* **Backend**: FastAPI , Uvicorn, Slowapi (Rate Limiter), Pydantic
* **Machine Learning**: PyTorch , MobileNetV2, Jupyter Notebook


* **Dataset**: The model training pipeline leverages the **PlantVillage Dataset**, specifically utilizing the standardized web distribution hosted by Sharada Mohanty. 

* **Source Repository**: [spMohanty/PlantVillage-Dataset](https://github.com/spMohanty/PlantVillage-Dataset)
* **Direct Data Stream Link**: [PlantVillage Master Zip Archive](https://github.com/spMohanty/PlantVillage-Dataset/archive/refs/heads/master.zip)

The subset contains thousands of high-resolution, multiclass plant leaf images categorized across distinct healthy and diseased biological classifications, which are streamed, unpacked, and normalized directly inside our research pipeline
