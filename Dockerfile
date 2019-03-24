FROM python:3.6-alpine

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

RUN mkdir -p /app/data
EXPOSE 5000
ENTRYPOINT realpath ./server.py
ENTRYPOINT ["python", "./server.py"]
