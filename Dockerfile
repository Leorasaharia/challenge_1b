FROM python:3.10-slim

WORKDIR /app

# 1) Install deps
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
 && pip install --no-cache-dir -r requirements.txt \
 && rm -rf /var/lib/apt/lists/*

# 2) Download Flan-T5-base at build time
COPY download_flan_t5_base.py .
RUN python download_flan_t5_base.py

# 3) Copy remaining code & data
COPY run_inference.py .
COPY collection1/ ./collection1/
COPY collection2/ ./collection2/
COPY collection3/ ./collection3/

# 4) Run offline
ENTRYPOINT ["python","run_inference.py"]
