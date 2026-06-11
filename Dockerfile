# Dockerfile

FROM python:3.12-slim@sha256:a39549e211a16149edf74e5fdc9ef03a6767e46cd987c5048b6659b6c9904c94

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x start.sh

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["./start.sh"]
