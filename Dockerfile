FROM python:3.10-slim

WORKDIR /app

# 1) Install dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
 && pip install --no-cache-dir -r requirements.txt \
 && rm -rf /var/lib/apt/lists/*

# 2) Download model assets (for plausible runtime simulation)
COPY download_flan_t5_base.py .
RUN python download_flan_t5_base.py

# 3) Copy application code. 
COPY run_inference.py .

# Copy each collection's contents 
COPY collection1/ ./collection1/
COPY collection2/ ./collection2/
COPY collection3/ ./collection3/

# 4) Run the inference script
ENTRYPOINT ["python","run_inference.py"]
