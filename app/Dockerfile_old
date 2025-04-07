FROM python:3.11-slim as builder

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg wget 

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh \
    && bash miniconda.sh -b -p /opt/conda \
    && rm miniconda.sh
    
ENV PATH="/opt/conda/bin:${PATH}"

COPY environment.yml .

RUN conda env create -f environment.yml

RUN conda install -n ai_agents -c conda-forge python=3.11

WORKDIR /app

ENV PATH="/opt/conda/envs/ai_agents/bin:${PATH}"


# RUN find /opt/conda/ -type f -name '*.a' -delete \
#     && find /opt/conda/ -type f -name '*.pyc' -delete \
#     && find /opt/conda/ -path '*/__pycache__/*' -delete

COPY . .

CMD ["uvicorn", "main:app", "--reload"]
