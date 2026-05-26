

FROM python:3.11-slim

WORKDIR /app

# Installing necessary operating system utilities for image processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copying list of dependencies 
COPY requirements.txt .

# Installing all the Python libraries directly inside the box
RUN pip install --no-cache-dir -r requirements.txt

# Copying rest of  the backend code, files, and AI model weights 
COPY . .

# the network port that FastAPI runs on
EXPOSE 8000

# The command that runs automatically when the container wakes up
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]