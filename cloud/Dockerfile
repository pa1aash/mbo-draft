# Reproducible `main` env (synthetic grid + calibration arm). Ships in the supplement.
# Design-Bench (db) and design-baselines (baselines) are NOT in here — their legacy
# deps don't containerize cleanly; cloud/setup.sh provisions them as conda envs.
#   docker build -f cloud/Dockerfile -t offline-mbo .
#   docker run --rm offline-mbo python code/mbo.py
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY code/ code/
COPY results/ results/
CMD ["python", "code/mbo.py"]
