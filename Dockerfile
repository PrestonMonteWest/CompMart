FROM python:3.7-slim-stretch
USER root

# Necessary for Python packages in requirements file.
RUN apt update && \
apt -y install libpq-dev build-essential libssl-dev libffi-dev python3-dev libjpeg-dev zlib1g-dev

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
