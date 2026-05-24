
# 🧠 ML Training Pipeline — Plant Disease Classifier

End-to-end training pipeline for a 38-class plant disease classifier built on **MobileNetV2** transfer learning, implemented in `model_training.ipynb`.

---

## Pipeline Overview

```
🌐 Data Ingestion → 🧼 Preprocessing → ✂️ Model Surgery → ⚡ Training Loop → 💾 Serialization
```

---

## How It Works

### 1 — Data Ingestion
Streams a 200 MB archive of the [PlantVillage Dataset](https://github.com/spMohanty/PlantVillage-Dataset) directly from GitHub using `requests`:

```
https://github.com/spMohanty/PlantVillage-Dataset/archive/refs/heads/master.zip
```

A dynamic `os.walk()` traversal locates the target folder by detecting the directory with **> 30 subfolders** (the 38-class root), avoiding brittle hardcoded paths.

### 2 — Preprocessing
Images are passed through a `torchvision.transforms` pipeline:
- **Resize** to `224×224`
- **Normalize** using ImageNet stats (`mean=[0.485, 0.456, 0.406]`, `std=[0.229, 0.224, 0.225]`)
- **80/20 split** via `random_split` across ~7,000 images
- **Batched loading** with `DataLoader(batch_size=32, shuffle=True)`

### 3 — Transfer Learning & Model Surgery
Loads a pre-trained `MobileNetV2` and freezes all base layers (`requires_grad = False`). The default 1,000-class output head is replaced with a fresh `nn.Linear` layer mapped to **38 disease classes**.

```python
model.classifier[1] = nn.Linear(in_features, num_classes)
model = model.to(device)  # CUDA GPU
```

### 4 — Training Loop
Runs **5 epochs** with `Adam` (lr=`0.001`) + `CrossEntropyLoss`. Each batch follows a 4-step cycle:

1. `optimizer.zero_grad()` — clear old gradients
2. `model(images)` — forward pass
3. `criterion(outputs, labels)` — compute loss
4. `loss.backward()` + `optimizer.step()` — backpropagate & update

| Epoch | Loss |
|-------|------|
| **Epoch 1** | 1.5861 |
| **Epoch 5** | 0.2400 |

> **84.9% loss reduction** across 5 epochs confirming stable convergence.

### 5 — Serialization
Two files are saved and transferred to the production server:

| File | Description |
|------|-------------|
| `plant_model.pth` | Trained weight dictionary (~9 MB) |
| `classes.json` | Integer → disease label map (e.g. index `20` → `Potato___Early_blight`) |

---

## Tech Stack

| | |
|---|---|
| Framework | PyTorch & Torchvision |
| Base Model | MobileNetV2 |
| Compute | CUDA GPU |
| Optimizer | Adam (`lr=0.001`) |
| Loss | CrossEntropyLoss |
| Dataset | PlantVillage Subset (38 classes, ~8,750 total images) (7,000 train + ~1,750 validation) |