# ---------------------------
# Streamlit Frontend Dockerfile
# ---------------------------
FROM python:3.10-slim

WORKDIR /app

# System dependencies (optional but good for images/fonts)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend application
COPY . .

# Streamlit defaults to port 8501
EXPOSE 8501

# Disable usage stats (optional)
ENV STREAMLIT_BROWSER_GATHERUSAGESTATS=false

# Run Streamlit
CMD ["streamlit", "run", "Login.py", "--server.address=0.0.0.0", "--server.port=8501"]
