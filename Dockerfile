FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app
WORKDIR /app

ADD requirements.txt .
RUN pip install -U -r requirements.txt
ADD . .
