FROM python:3.10 AS builder
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN apt update
RUN apt install -y ffmpeg

WORKDIR /app
COPY / .

CMD ["python","main.py"]