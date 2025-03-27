# bot/Dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget \
    bzip2 \
    && rm -rf /var/lib/apt/lists/*

# Установка Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh \
    && bash miniconda.sh -b -p /opt/conda \
    && rm miniconda.sh

ENV PATH="/opt/conda/bin:${PATH}"
RUN conda install -n base -y -c conda-forge mamba

WORKDIR /bot

COPY environment.yml .
RUN mamba env create -f environment.yml

ENV PATH="/opt/conda/envs/bot_env/bin:${PATH}"

COPY . .

RUN mkdir -p /temp
VOLUME /temp

CMD ["python", "bot.py"]