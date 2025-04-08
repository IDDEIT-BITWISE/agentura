FROM python:3.11-slim as builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    torch==2.3.1+cpu \
    torchaudio==2.3.1+cpu \
    --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir openai-whisper==20240930


FROM python:3.11-slim

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y iputils-ping

WORKDIR /app
COPY . .

RUN find /usr/local -depth \
    \( \
    \( -type d -a \( -name test -o -name tests -o -name __pycache__ \) \) \
    -o \
    \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
    \) -exec rm -rf '{}' +

ENV PYTHONUNBUFFERED=1
ENV TORCH_CUDA_VERSION="cpu"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
