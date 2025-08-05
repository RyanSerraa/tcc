FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
