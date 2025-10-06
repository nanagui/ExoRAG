# syntax=docker/dockerfile:1.7
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3.11 \
        python3.11-venv \
        python3-pip \
        git \
        curl \
        build-essential \
        libffi-dev \
        && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3.11 /usr/local/bin/python \
    && ln -s /usr/bin/pip3 /usr/local/bin/pip

WORKDIR /workspace

COPY requirements.txt ./
RUN python -m venv /opt/venv \
    && . /opt/venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH=/workspace/src

COPY src ./src
COPY .env.example ./.env.example

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
