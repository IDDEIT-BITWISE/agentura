FROM python:3.11-slim as builder

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg 
    
COPY requirements.txt .

RUN pip install -r requirements.txt



WORKDIR /app

ENV PATH="/opt/conda/envs/ai_agents/bin:${PATH}"


# RUN find /opt/conda/ -type f -name '*.a' -delete \
#     && find /opt/conda/ -type f -name '*.pyc' -delete \
#     && find /opt/conda/ -path '*/__pycache__/*' -delete

COPY . .

CMD ["uvicorn", "main:app", "--reload"]
