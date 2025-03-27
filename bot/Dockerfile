FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY environment.yml .

RUN pip install --no-cache-dir conda && \
    conda env create -f environment.yml

ENV PATH /opt/conda/envs/ai_agents/bin:$PATH
RUN echo "conda activate ai_agents" >> ~/.bashrc

COPY . .

#EXPOSE 8443

CMD ["python", "bot.py"]