FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3-pip unzip coreutils

RUN pip install --no-cache-dir wheel kaggle pandas scikit-learn tensorflow

WORKDIR /app

COPY . /app