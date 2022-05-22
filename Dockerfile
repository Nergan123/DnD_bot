FROM python:3.10 AS builder

WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN apt update
RUN apt install -y ffmpeg

COPY / .

CMD ["python","main.py"]