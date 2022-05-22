FROM python:3.10
ENV Token=
WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN apt update
RUN apt-get install -y ffmpeg

COPY . .

CMD ["python","main.py"]
