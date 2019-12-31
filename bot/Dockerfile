FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends wget 

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh \
    && bash miniconda.sh -b -p /opt/conda \
    && rm miniconda.sh
    
ENV PATH="/opt/conda/bin:${PATH}"

COPY environment.yml .

RUN conda env create -f environment.yml

RUN conda install -n ai_bot -c conda-forge python=3.11

WORKDIR /bot

ENV PATH="/opt/conda/envs/ai_bot/bin:${PATH}"

COPY . . 

CMD ["python", "bot.py"]