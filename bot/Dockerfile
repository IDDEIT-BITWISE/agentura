FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends 

RUN apt-get update && apt-get install -y iputils-ping

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /bot

COPY . . 

CMD ["python", "bot.py"]