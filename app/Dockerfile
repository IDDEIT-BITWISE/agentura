FROM python:3.11-slim as builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    wget \
    bzip2 \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh \
    && bash miniconda.sh -b -p /opt/conda \
    && rm miniconda.sh

ENV PATH="/opt/conda/bin:${PATH}"
RUN conda install -n base -y -c conda-forge mamba

WORKDIR /app

COPY environment.yml .
RUN mamba env create -f environment.yml \
    && mamba clean -a -y

FROM python:3.11-slim

COPY --from=builder /opt/conda /opt/conda
COPY --from=builder /app /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/opt/conda/envs/app_env/bin:${PATH}"

WORKDIR /app

RUN find /opt/conda/ -type f -name '*.a' -delete \
    && find /opt/conda/ -type f -name '*.pyc' -delete \
    && find /opt/conda/ -path '*/__pycache__/*' -delete

VOLUME /temp

CMD ["uvicorn", "app:main", "--host", "0.0.0.0", "--port", "80"]