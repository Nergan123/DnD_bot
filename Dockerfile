# # First stage
# FROM python:3.10 AS builder
# ENV Token
#
# WORKDIR /app
# RUN touch .env
# RUN echo "Token=$Token" > .env


# Final stage
FROM python:3.10
ENV Token=
WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN apt update
RUN apt-get install -y ffmpeg

COPY .. .

CMD ["python","main.py"]